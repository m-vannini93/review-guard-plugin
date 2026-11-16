"""Hook SessionStart: avvisa se i file .env non sono ignorati o sono già tracciati da git."""

import json
import subprocess
import sys

from protect_env import is_env_file


def git(cwd: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=False
    )


def find_problems(cwd: str) -> list[str]:
    if git(cwd, "rev-parse", "--is-inside-work-tree").returncode != 0:
        return []
    problems: list[str] = []
    if git(cwd, "check-ignore", "-q", "--no-index", ".env").returncode != 0:
        problems.append("`.env` non è nel .gitignore")
    tracked = [f for f in git(cwd, "ls-files").stdout.splitlines() if is_env_file(f)]
    if tracked:
        problems.append(f"file di segreti già tracciati da git: {', '.join(tracked)}")
    return problems


def main() -> int:
    event: dict = json.load(sys.stdin)
    problems = find_problems(event.get("cwd") or ".")
    if problems:
        message = "review-guard: " + "; ".join(problems) + "."
        output = {
            "systemMessage": message,
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": message,
            },
        }
        print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
