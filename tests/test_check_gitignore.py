import json
from pathlib import Path

from check_gitignore import find_problems
from conftest import git, run_hook


def test_missing_gitignore_is_reported(repo: Path) -> None:
    problems = find_problems(str(repo))
    assert any(".gitignore" in p for p in problems)


def test_ignored_env_is_ok(repo: Path) -> None:
    (repo / ".gitignore").write_text(".env\n.env.*\n")
    assert find_problems(str(repo)) == []


def test_tracked_env_is_reported(repo: Path) -> None:
    (repo / ".env").write_text("SECRET=1\n")
    git(repo, "add", ".env")
    git(repo, "commit", "-q", "-m", "oops")
    (repo / ".gitignore").write_text(".env\n")
    problems = find_problems(str(repo))
    assert problems == ["file di segreti già tracciati da git: .env"]


def test_not_a_git_repo_is_silent(tmp_path: Path) -> None:
    assert find_problems(str(tmp_path)) == []


def test_hook_outputs_system_message(repo: Path) -> None:
    result = run_hook("check_gitignore.py", {"cwd": str(repo)})
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert "review-guard" in output["systemMessage"]
    assert output["hookSpecificOutput"]["hookEventName"] == "SessionStart"
