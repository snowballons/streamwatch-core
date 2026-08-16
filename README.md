# streamwatch-core

Shared stream-watching domain core for the StreamWatch ecosystem. This package is the **canonical** source for logic shared between the backend and the CLI:

- **Session pool** — reusable pre-configured `Streamlink` sessions
- **Stream resolution** — resolve a URL to online/offline status + stream details
- **Error taxonomy** — platform error classification (no plugin / no streams / browser required / plugin error)
- **Metadata extraction** — platform detection, category/keyword extraction, viewer counts, thumbnails, stream types

## Consumers

| Consumer | Relationship |
|----------|--------------|
| `streamwatch-api` (backend) | imports this package directly |
| `streamwatch-cli` | vendors a **copy** (dev-only `tools/sync-to-cli.sh` script + parity tests); core wins on conflicts |

The CLI must never depend on this package at runtime — some users only use the CLI, and a backend/shared dependency is impractical for them. This package exists to help the maintainer keep both projects consistent.

## Development

```bash
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

## License

MIT