import json
import re
import shlex
import sys
from pathlib import Path

# Token che nominano un file .env o .env.* (es. ".env", "config/.env.local", ">.env")
ENV_TOKEN = re.compile(r"(^|[/=<>|;&\"'\s])\.env(\.[\w-]+)?($|[\"'\s;|&<>)])")


def is_env_file(path: str) -> bool:
    name = Path(path).name
    return name == ".env" or name.startswith(".env.")


def command_touches_env(command: str) -> bool:
    try:
        tokens = shlex.split(command)
    except ValueError:
        tokens = []
    if any(is_env_file(tok) for tok in tokens):
        return True
    return ENV_TOKEN.search(command) is not None


def find_env_target(tool_name: str, tool_input: dict) -> str | None:
    if tool_name == "Bash":
        command: str = tool_input.get("command", "")
        return command if command_touches_env(command) else None
    if tool_name == "Grep":
        for key in ("path", "glob"):
            value: str = tool_input.get(key) or ""
            if value and (is_env_file(value) or ".env" in Path(value).name):
                return value
        return None
    path: str = tool_input.get("file_path", "")
    return path if path and is_env_file(path) else None


def main() -> int:
    event: dict = json.load(sys.stdin)
    target = find_env_target(event.get("tool_name", ""), event.get("tool_input", {}))
    if target is not None:
        print(
            f"Bloccato: accesso ai file .env non consentito ({target}).",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
