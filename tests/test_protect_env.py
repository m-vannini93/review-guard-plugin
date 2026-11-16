import pytest
from conftest import run_hook
from protect_env import find_env_target, is_env_file


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        (".env", True),
        ("/x/.env", True),
        ("config/.env.production", True),
        (".env.local", True),
        ("app.py", False),
        (".envrc", False),
        (".venv/bin/activate", False),
    ],
)
def test_is_env_file(path: str, expected: bool) -> None:
    assert is_env_file(path) is expected


@pytest.mark.parametrize(
    ("tool", "tool_input", "blocked"),
    [
        ("Read", {"file_path": "/x/.env"}, True),
        ("Edit", {"file_path": "/x/.env.local"}, True),
        ("Read", {"file_path": "/x/app.py"}, False),
        ("Bash", {"command": "cat .env"}, True),
        ("Bash", {"command": "head -5 config/.env.production"}, True),
        ("Bash", {"command": "grep SECRET .env"}, True),
        ("Bash", {"command": 'cat ".env"'}, True),
        ("Bash", {"command": "ls -la"}, False),
        ("Bash", {"command": "source .venv/bin/activate && pytest"}, False),
        ("Bash", {"command": "python -m dotenv list"}, False),
        ("Grep", {"pattern": "SECRET", "path": ".env"}, True),
        ("Grep", {"pattern": "SECRET", "glob": ".env*"}, True),
        ("Grep", {"pattern": "SECRET", "path": "src"}, False),
    ],
)
def test_find_env_target(tool: str, tool_input: dict, blocked: bool) -> None:
    assert (find_env_target(tool, tool_input) is not None) is blocked


def test_hook_exit_codes() -> None:
    blocked = run_hook(
        "protect_env.py", {"tool_name": "Bash", "tool_input": {"command": "cat .env"}}
    )
    assert blocked.returncode == 2
    assert "Bloccato" in blocked.stderr

    allowed = run_hook(
        "protect_env.py", {"tool_name": "Read", "tool_input": {"file_path": "app.py"}}
    )
    assert allowed.returncode == 0
