"""Minimal stdio JSON-RPC adapter for the Atomic Knowledge runtime."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from typing import Any, BinaryIO

from runtime import AtomicKnowledgeRuntime, RuntimeConfigurationError, RuntimeErrorBase
from runtime.types import RuntimeResult


JSONRPC_VERSION = "2.0"
MCP_PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {
    "name": "atomic-knowledge-mcp",
    "version": "0.2.0",
}

KB_PATH_SCHEMA = {
    "type": "object",
    "properties": {
        "kb_path": {
            "type": "string",
            "description": "Path to the knowledge base directory.",
        }
    },
    "required": ["kb_path"],
    "additionalProperties": False,
}

TOOLS = (
    {
        "name": "atomic_knowledge_init_kb",
        "description": "Initialize a knowledge base directory.",
        "inputSchema": KB_PATH_SCHEMA,
    },
    {
        "name": "atomic_knowledge_check_kb",
        "description": "Run the knowledge base health check.",
        "inputSchema": KB_PATH_SCHEMA,
    },
    {
        "name": "atomic_knowledge_get_context",
        "description": "Return the recommended context read set.",
        "inputSchema": KB_PATH_SCHEMA,
    },
    {
        "name": "atomic_knowledge_validate_kb",
        "description": "Validate KB structure and frontmatter.",
        "inputSchema": KB_PATH_SCHEMA,
    },
)

TOOL_METHODS = {
    "atomic_knowledge_init_kb": "init_kb",
    "atomic_knowledge_check_kb": "check_kb",
    "atomic_knowledge_get_context": "get_context",
    "atomic_knowledge_validate_kb": "validate_kb",
}


class MCPRequestError(Exception):
    """Small JSON-RPC error wrapper for request handling."""

    def __init__(self, code: int, message: str, data: Any | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.data = data


def handle_request(request: dict[str, Any]) -> dict[str, Any] | None:
    """Handle one minimal MCP / JSON-RPC request."""

    request_id = request.get("id") if isinstance(request, dict) else None

    try:
        if not isinstance(request, dict):
            raise MCPRequestError(-32602, "request must be an object")

        method = request.get("method")
        if not isinstance(method, str) or not method:
            raise MCPRequestError(-32602, "method must be a non-empty string")

        params = _expect_object(request.get("params"), field_name="params")

        if method == "notifications/initialized":
            return None

        if method == "initialize":
            return _result_response(
                request_id,
                {
                    "protocolVersion": MCP_PROTOCOL_VERSION,
                    "capabilities": {"tools": {}},
                    "serverInfo": SERVER_INFO,
                },
            )

        if method == "tools/list":
            return _result_response(request_id, {"tools": list(TOOLS)})

        if method == "tools/call":
            return _result_response(request_id, _handle_tools_call(params))

        raise MCPRequestError(-32601, f"Unknown method: {method}")
    except MCPRequestError as exc:
        return _error_response(request_id, exc.code, exc.message, exc.data)
    except Exception as exc:  # pragma: no cover - defensive boundary
        return _error_response(request_id, -32603, f"Internal error: {exc}")


def serve_stdio(
    input_stream: BinaryIO | None = None,
    output_stream: BinaryIO | None = None,
) -> None:
    """Serve the minimal MCP subset over stdio using Content-Length framing."""

    source = input_stream if input_stream is not None else sys.stdin.buffer
    sink = output_stream if output_stream is not None else sys.stdout.buffer

    while True:
        try:
            request = _read_message(source)
        except EOFError:
            break
        except Exception as exc:  # pragma: no cover - transport fallback
            _write_message(
                sink,
                _error_response(None, -32603, f"Internal error: {exc}"),
            )
            continue

        if request is None:
            break

        response = handle_request(request)
        if response is not None:
            _write_message(sink, response)


def main() -> None:
    """Run the minimal stdio server."""

    serve_stdio()


def _handle_tools_call(params: dict[str, Any]) -> dict[str, Any]:
    name = params.get("name")
    if not isinstance(name, str) or not name:
        raise MCPRequestError(-32602, "tools/call requires a non-empty tool name")

    method_name = TOOL_METHODS.get(name)
    if method_name is None:
        raise MCPRequestError(-32601, f"Unknown tool: {name}")

    arguments = _expect_object(params.get("arguments"), field_name="arguments")
    kb_path = arguments.get("kb_path")
    if not isinstance(kb_path, str) or not kb_path.strip():
        raise MCPRequestError(-32602, "tools/call arguments must include kb_path")

    runtime = AtomicKnowledgeRuntime(kb_path=kb_path)

    try:
        runtime_result = getattr(runtime, method_name)()
    except RuntimeConfigurationError as exc:
        raise MCPRequestError(-32602, str(exc)) from exc
    except RuntimeErrorBase as exc:
        raise MCPRequestError(-32603, str(exc)) from exc
    except Exception as exc:
        raise MCPRequestError(
            -32603,
            f"Tool '{name}' failed: {exc}",
        ) from exc

    return _runtime_result_to_tool_response(runtime_result)


def _runtime_result_to_tool_response(result: RuntimeResult) -> dict[str, Any]:
    payload = json.dumps(asdict(result), ensure_ascii=True, indent=2, sort_keys=True)
    return {
        "content": [{"type": "text", "text": payload}],
        "isError": not result.success,
    }


def _expect_object(value: Any, field_name: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise MCPRequestError(-32602, f"{field_name} must be an object")
    return value


def _result_response(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": JSONRPC_VERSION, "id": request_id, "result": result}


def _error_response(
    request_id: Any,
    code: int,
    message: str,
    data: Any | None = None,
) -> dict[str, Any]:
    error = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return {"jsonrpc": JSONRPC_VERSION, "id": request_id, "error": error}


def _read_message(input_stream: BinaryIO) -> dict[str, Any] | None:
    headers: dict[str, str] = {}

    while True:
        line = input_stream.readline()
        if not line:
            if headers:
                raise EOFError("unexpected end of input while reading headers")
            return None

        if line in (b"\r\n", b"\n"):
            if headers:
                break
            continue

        key, separator, value = line.decode("ascii").partition(":")
        if not separator:
            raise ValueError(f"invalid header line: {line!r}")
        headers[key.strip().lower()] = value.strip()

    content_length_value = headers.get("content-length")
    if content_length_value is None:
        raise ValueError("missing Content-Length header")

    try:
        content_length = int(content_length_value)
    except ValueError as exc:
        raise ValueError("invalid Content-Length header") from exc

    body = input_stream.read(content_length)
    if len(body) != content_length:
        raise EOFError("unexpected end of input while reading body")

    try:
        request = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON body: {exc.msg}") from exc

    if not isinstance(request, dict):
        raise ValueError("request body must decode to an object")

    return request


def _write_message(output_stream: BinaryIO, response: dict[str, Any]) -> None:
    body = json.dumps(response, ensure_ascii=True).encode("utf-8")
    header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
    output_stream.write(header)
    output_stream.write(body)
    output_stream.flush()


if __name__ == "__main__":
    main()
