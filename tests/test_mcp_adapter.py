import json
import tempfile
import unittest
from pathlib import Path

from adapters.mcp import handle_request


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_KB_PATH = REPO_ROOT / "example-kb"
EXPECTED_TOOL_NAMES = {
    "atomic_knowledge_init_kb",
    "atomic_knowledge_check_kb",
    "atomic_knowledge_get_context",
    "atomic_knowledge_validate_kb",
}


class MCPAdapterTests(unittest.TestCase):
    def _make_request(
        self,
        method: str,
        params: dict[str, object] | None = None,
        request_id: int = 1,
    ) -> dict[str, object] | None:
        return handle_request(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": {} if params is None else params,
            }
        )

    def _parse_tool_payload(
        self, response: dict[str, object]
    ) -> tuple[dict[str, object], dict[str, object]]:
        self.assertIn("result", response)
        result = response["result"]
        self.assertIsInstance(result, dict)
        self.assertIn("content", result)
        self.assertIsInstance(result["content"], list)
        self.assertGreaterEqual(len(result["content"]), 1)
        self.assertEqual(result["content"][0]["type"], "text")
        payload = json.loads(result["content"][0]["text"])
        self.assertIsInstance(payload, dict)
        return result, payload

    def test_initialize_returns_protocol_capabilities_and_server_info(self) -> None:
        response = self._make_request("initialize")

        self.assertIsNotNone(response)
        self.assertIn("result", response)
        result = response["result"]
        self.assertIn("protocolVersion", result)
        self.assertIn("serverInfo", result)
        self.assertIn("capabilities", result)
        self.assertIn("tools", result["capabilities"])

    def test_notifications_initialized_returns_none(self) -> None:
        response = self._make_request("notifications/initialized")

        self.assertIsNone(response)

    def test_tools_list_returns_all_expected_tools(self) -> None:
        response = self._make_request("tools/list")

        self.assertIsNotNone(response)
        self.assertIn("result", response)
        result = response["result"]
        self.assertIn("tools", result)
        self.assertEqual(len(result["tools"]), 4)

        tool_names = {tool["name"] for tool in result["tools"]}
        self.assertEqual(tool_names, EXPECTED_TOOL_NAMES)

        for tool in result["tools"]:
            self.assertIn("name", tool)
            self.assertIn("inputSchema", tool)

    def test_tools_call_get_context_returns_runtime_payload(self) -> None:
        response = self._make_request(
            "tools/call",
            {
                "name": "atomic_knowledge_get_context",
                "arguments": {"kb_path": str(EXAMPLE_KB_PATH)},
            },
        )

        self.assertIsNotNone(response)
        result, payload = self._parse_tool_payload(response)

        self.assertFalse(result["isError"])
        self.assertEqual(payload["action"], "get_context")
        self.assertTrue(payload["success"])

    def test_tools_call_init_kb_creates_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            kb_path = Path(temp_dir) / "kb"

            response = self._make_request(
                "tools/call",
                {
                    "name": "atomic_knowledge_init_kb",
                    "arguments": {"kb_path": str(kb_path)},
                },
            )

            self.assertIsNotNone(response)
            result, payload = self._parse_tool_payload(response)

            self.assertFalse(result["isError"])
            self.assertEqual(payload["action"], "init_kb")
            self.assertTrue(payload["success"])
            self.assertTrue((kb_path / "AGENT.md").is_file())
            self.assertTrue((kb_path / "wiki/active.md").is_file())

    def test_tools_call_check_kb_returns_runtime_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            kb_path = Path(temp_dir) / "kb"

            init_response = self._make_request(
                "tools/call",
                {
                    "name": "atomic_knowledge_init_kb",
                    "arguments": {"kb_path": str(kb_path)},
                },
            )
            self.assertIsNotNone(init_response)

            response = self._make_request(
                "tools/call",
                {
                    "name": "atomic_knowledge_check_kb",
                    "arguments": {"kb_path": str(kb_path)},
                },
            )

            self.assertIsNotNone(response)
            result, payload = self._parse_tool_payload(response)

            self.assertFalse(result["isError"])
            self.assertEqual(payload["action"], "check_kb")
            self.assertTrue(payload["success"])

    def test_tools_call_validate_kb_returns_report_payload(self) -> None:
        response = self._make_request(
            "tools/call",
            {
                "name": "atomic_knowledge_validate_kb",
                "arguments": {"kb_path": str(EXAMPLE_KB_PATH)},
            },
        )

        self.assertIsNotNone(response)
        _, payload = self._parse_tool_payload(response)

        self.assertEqual(payload["action"], "validate_kb")
        self.assertIn("report", payload)
        self.assertIsNotNone(payload["report"])

    def test_unknown_method_returns_method_not_found_error(self) -> None:
        response = self._make_request("does/not/exist")

        self.assertIsNotNone(response)
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32601)

    def test_unknown_tool_returns_method_not_found_error(self) -> None:
        response = self._make_request(
            "tools/call",
            {
                "name": "atomic_knowledge_missing_tool",
                "arguments": {"kb_path": str(EXAMPLE_KB_PATH)},
            },
        )

        self.assertIsNotNone(response)
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32601)

    def test_tools_call_missing_kb_path_returns_invalid_params_error(self) -> None:
        response = self._make_request(
            "tools/call",
            {
                "name": "atomic_knowledge_get_context",
                "arguments": {},
            },
        )

        self.assertIsNotNone(response)
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)


if __name__ == "__main__":
    unittest.main()
