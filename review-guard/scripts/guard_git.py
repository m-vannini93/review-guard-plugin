"""Hook PreToolUse (Bash): blocca commit con file .env in stage e force push su main/master."""

import json
import re
import shlex
import subprocess
import sys

from protect_env import is_env_file

PROTECTED_BRANCHES: frozenset[str] = frozenset({"main", "master"})
SEPARATORS = re.compile(r"&&|\|\||;|\||\n")
# Opzioni globali di git che prendono un valore come token successivo
GIT_OPTS_WITH_VALUE: frozenset[str] = frozenset(
    {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
)


def git(cwd: str, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=False
    )
    return result.stdout


def split_segments(command: str) -> list[list[str]]:
    segments: list[list[str]] = []
    for part in SEPARATORS.split(command):
        try:
            tokens = shlex.split(part)
        except ValueError:
            tokens = part.split()
        if tokens:
            segments.append(tokens)
    return segments


def parse_git(tokens: list[str], cwd: str) -> tuple[str, list[str], str] | None:
    """Restituisce (sottocomando, argomenti, cwd effettiva) se il segmento è un comando git."""
    i = 0
    while i < len(tokens) and re.fullmatch(r"\w+=.*", tokens[i]):
        i += 1  # salta assegnazioni di variabili, es. GIT_TRACE=1 git ...
    if i >= len(tokens) or tokens[i].rsplit("/", 1)[-1] != "git":
        return None
    i += 1
    while i < len(tokens) and tokens[i].startswith("-"):
        if tokens[i] == "-C" and i + 1 < len(tokens):
            cwd = tokens[i + 1]
        i += 2 if tokens[i] in GIT_OPTS_WITH_VALUE else 1
    if i >= len(tokens):
        return None
    return tokens[i], tokens[i + 1 :], cwd


def has_short_flag(args: list[str], flag: str) -> bool:
    return any(
        a.startswith("-") and not a.startswith("--") and flag in a[1:] for a in args
    )


def check_commit(args: list[str], cwd: str) -> str | None:
    files = git(cwd, "diff", "--cached", "--name-only").splitlines()
    if "--all" in args or has_short_flag(args, "a"):
        files += git(cwd, "diff", "--name-only").splitlines()
    env_files = sorted({f for f in files if is_env_file(f)})
    if env_files:
        return (
            f"commit con file di segreti in stage ({', '.join(env_files)}). "
            "Toglili con `git restore --staged <file>` e aggiungili al .gitignore."
        )
    return None


def check_push(args: list[str], cwd: str) -> str | None:
    force_flag = (
        "--force" in args
        or any(a.startswith("--force-with-lease") for a in args)
        or has_short_flag(args, "f")
    )
    positional = [a for a in args if not a.startswith("-")]
    refspecs = positional[1:]
    targets: list[tuple[str, bool]] = []
    if refspecs:
        for spec in refspecs:
            plus = spec.startswith("+")
            spec = spec.lstrip("+")
            dst = spec.split(":", 1)[1] if ":" in spec else spec
            targets.append((dst.removeprefix("refs/heads/"), plus))
    else:
        current = git(cwd, "rev-parse", "--abbrev-ref", "HEAD").strip()
        targets.append((current, False))
    for branch, plus in targets:
        if branch in PROTECTED_BRANCHES and (force_flag or plus):
            return f"force push su '{branch}' non consentito: è un branch protetto."
    return None


def find_violation(command: str, cwd: str) -> str | None:
    for tokens in split_segments(command):
        parsed = parse_git(tokens, cwd)
        if parsed is None:
            continue
        sub, args, git_cwd = parsed
        if sub == "commit":
            reason = check_commit(args, git_cwd)
        elif sub == "push":
            reason = check_push(args, git_cwd)
        else:
            reason = None
        if reason:
            return reason
    return None


def main() -> int:
    event: dict = json.load(sys.stdin)
    if event.get("tool_name") != "Bash":
        return 0
    command: str = event.get("tool_input", {}).get("command", "")
    reason = find_violation(command, event.get("cwd") or ".")
    if reason:
        print(f"Bloccato: {reason}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
