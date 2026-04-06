# Contributing

Thank you for considering contributing to Atomic Knowledge!

## How to Contribute

### Report Issues

- Use GitHub Issues to report bugs or suggest features
- Include steps to reproduce bugs
- Include your environment (OS, agent platform, and relevant version info)

### Submit Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test thoroughly (see Testing section)
5. Submit a pull request

### Improve The Protocol

The core of this project is the universal protocol in `universal/`, especially:

- `universal/AGENT.md`
- `universal/schemas/`
- `universal/scripts/init-kb.sh`
- `universal/scripts/check-kb.sh`
- `universal/knowledge-base-template/`

## Testing

Before submitting, test your changes with:

1. Check the script syntax: `bash -n "universal/scripts/init-kb.sh"`
2. Check the health-check script syntax: `bash -n "universal/scripts/check-kb.sh"`
3. Initialize a test knowledge base: `bash universal/scripts/init-kb.sh /tmp/test-kb`
   Or use the root wrapper: `bash init.sh /tmp/test-kb`
4. Initialize another test knowledge base at a path containing `&`: `bash universal/scripts/init-kb.sh "/tmp/test&kb"`
5. Verify that both generated `AGENT.md` files are rendered with the real path, including the literal `&`
6. Verify that `wiki/active.md`, `wiki/recent.md`, `meta/candidates/index.md`, and `meta/lint-reports/index.md` are created
7. Verify that `/tmp/test-kb/meta/schemas/` contains the canonical schema files, including `lint-report.md` when it exists in `universal/schemas/`
8. Verify that `meta/lint-status.json` starts with `"last_lint": null` and `"lint_count": 0` for a freshly initialized knowledge base
9. Run the optional health check against both `universal/example-kb` and `/tmp/test-kb`: `bash universal/scripts/check-kb.sh universal/example-kb` and `bash universal/scripts/check-kb.sh /tmp/test-kb`
10. Confirm that the helper stays read-only, reports missing structure clearly, warns when lint has never run or is older than 24 hours, and surfaces stale open candidates when their frontmatter dates are old enough
11. Run through the README quickstart flow and confirm it is coherent for a generic agent platform

## Code Style

- Protocol docs should be clear, explicit, and platform-neutral
- Keep page schemas concise and example-driven
- Prefer English for public-facing project documentation unless a file is intentionally bilingual

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
