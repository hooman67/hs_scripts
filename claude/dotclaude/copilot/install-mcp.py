#!/usr/bin/env python3
"""Install shareable MCP definitions with credentials kept in local config."""

import json
import os
import tempfile
from pathlib import Path


HOME = Path.home()
TEMPLATE = Path(__file__).with_name("mcp-servers.template.json")
DESTINATION = HOME / ".copilot" / "mcp-config.json"
CLAUDE_CONFIG = HOME / ".claude.json"


def main() -> None:
    template = json.loads(TEMPLATE.read_text(encoding="utf-8"))["mcpServers"]
    claude = json.loads(CLAUDE_CONFIG.read_text(encoding="utf-8")) if CLAUDE_CONFIG.exists() else {}
    existing = json.loads(DESTINATION.read_text(encoding="utf-8")) if DESTINATION.exists() else {"mcpServers": {}}
    if not isinstance(existing.get("mcpServers"), dict):
        raise ValueError(f"Invalid MCP config in {DESTINATION}")
    servers = existing["mcpServers"]
    for name, source in template.items():
        server = dict(source)
        header_names = server.pop("headersFromClaude", [])
        if header_names:
            source_headers = claude.get("mcpServers", {}).get(name, {}).get("headers", {})
            missing = [key for key in header_names if not source_headers.get(key)]
            if missing:
                raise ValueError(
                    f"{name} needs local {', '.join(missing)} in {CLAUDE_CONFIG}; "
                    "no MCP config was changed"
                )
            server["headers"] = {key: source_headers[key] for key in header_names}
        for key in ("command", "url"):
            if key in server:
                server[key] = os.path.expanduser(server[key])
        if "args" in server:
            server["args"] = [os.path.expanduser(arg) for arg in server["args"]]
        if name in servers and servers[name] != server:
            old = dict(servers[name])
            new = dict(server)
            old.pop("headers", None)
            new.pop("headers", None)
            if old != new or not header_names or set(servers[name].get("headers", {})) != set(header_names):
                raise ValueError(f"Existing Copilot MCP definition for {name} differs; no MCP config was changed")
        servers[name] = server
    DESTINATION.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if DESTINATION.is_symlink():
        raise ValueError(f"Refusing to overwrite symlink: {DESTINATION}")
    fd, path = tempfile.mkstemp(prefix=".mcp-config-", dir=DESTINATION.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            json.dump(existing, output, indent=2)
            output.write("\n")
        os.chmod(path, 0o600)
        os.replace(path, DESTINATION)
    finally:
        if os.path.exists(path):
            os.unlink(path)
    print(f"Registered {len(template)} MCP definitions in machine-local {DESTINATION} (mode 600)")


if __name__ == "__main__":
    main()
