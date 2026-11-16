from pathlib import Path

import pytest
from conftest import git, run_hook
from guard_git import find_violation


def bash_event(command: str, cwd: Path) -> dict:
    return {"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(cwd)}


def test_commit_with_staged_env_is_blocked(repo: Path) -> None:
    (repo / ".env").write_text("SECRET=123\n")
    git(repo, "add", ".env")
    result = run_hook("guard_git.py", bash_event("git commit -m 'x'", repo))
    assert result.returncode == 2
    assert ".env" in result.stderr


def test_commit_all_with_modified_tracked_env_is_blocked(repo: Path) -> None:
    (repo / ".env.local").write_text("A=1\n")
    git(repo, "add", ".env.local")
    git(repo, "commit", "-q", "-m", "oops")
    (repo / ".env.local").write_text("A=2\n")
    assert find_violation("git commit -am 'update'", str(repo)) is not None


def test_clean_commit_is_allowed(repo: Path) -> None:
    (repo / "app.py").write_text("print('ciao ciao')\n")
    git(repo, "add", "app.py")
    assert (
        run_hook("guard_git.py", bash_event("git commit -m 'ok'", repo)).returncode == 0
    )


@pytest.mark.parametrize(
    "command",
    [
        "git push --force",
        "git push -f origin main",
        "git push --force-with-lease origin main",
        "git push origin +main",
        "git push origin +feature:main",
        "git push -uf origin master",
        "git -C . push --force",
        "ruff check . && git push --force origin main",
    ],
)
def test_force_push_to_protected_branch_is_blocked(repo: Path, command: str) -> None:
    assert find_violation(command, str(repo)) is not None


@pytest.mark.parametrize(
    "command",
    [
        "git push",
        "git push origin main",
        "git push --force origin feature",
        "git push origin +feature",
        "git status",
        "echo 'git push --force'",
    ],
)
def test_allowed_git_commands(repo: Path, command: str) -> None:
    assert find_violation(command, str(repo)) is None


def test_force_push_from_feature_branch_is_allowed(repo: Path) -> None:
    git(repo, "checkout", "-q", "-b", "feature")
    assert find_violation("git push --force", str(repo)) is None


def test_non_bash_tool_is_ignored(repo: Path) -> None:
    event = {"tool_name": "Read", "tool_input": {"file_path": "x"}, "cwd": str(repo)}
    assert run_hook("guard_git.py", event).returncode == 0
