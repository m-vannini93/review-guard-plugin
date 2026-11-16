---
name: pre-commit-check
description: Controllo prima del commit su un progetto Python - ruff check, ruff format e pytest sui file modificati. Usala quando l'utente chiede di verificare le modifiche prima di committare.
allowed-tools: Bash(git diff *), Bash(git status *), Bash(ruff *), Bash(.venv/bin/ruff *), Bash(pytest *), Bash(.venv/bin/pytest *)
---
1. Raccogli i file Python modificati, in stage e non:
   `git diff --cached --name-only` e `git diff --name-only`. Tieni solo i `.py`
   che esistono ancora. Se non ce ne sono, dillo e fermati.
2. Usa gli strumenti del venv del progetto se esistono (`.venv/bin/ruff`,
   `.venv/bin/pytest`), altrimenti quelli nel PATH.
3. Esegui sui file trovati:
   - `ruff check <file...>`
   - `ruff format --check <file...>`
4. Se il progetto ha dei test (cartella `tests/` o file `test_*.py`), esegui
   `pytest -q`.
5. Riporta un riepilogo: per ogni controllo, superato o fallito, con gli errori
   e `file:riga`. Non correggere i file e non fare commit: proponi le correzioni
   (es. `ruff check --fix`, `ruff format`) e chiedi all'utente se applicarle.
