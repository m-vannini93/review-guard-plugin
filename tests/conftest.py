import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "review-guard" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def run_hook(script: str, event: dict) -> subprocess.CompletedProcess[str]:
    """Esegue uno script hook come farebbe Claude Code: evento JSON su stdin."""
    import json

    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        check=False,
    )


def git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """Repo git vuoto con un commit iniziale sul branch main."""
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "config", "user.name", "test")
    git(tmp_path, "config", "user.email", "test@example.com")
    (tmp_path / "app.py").write_text("print('ciao')\n")
    git(tmp_path, "add", "app.py")
    git(tmp_path, "commit", "-q", "-m", "init")
    return tmp_path
