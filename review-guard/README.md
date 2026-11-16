# review-guard

Plugin per Claude Code che aiuta a rivedere codice Python e a proteggere i segreti del progetto.

## Contenuto

**Skill**
- `pr-review` (`/review-guard:pr-review`): rivede una pull request o un diff Python, separa i problemi verificabili nel diff dalle ipotesi sul runtime e cita sempre file e riga. Con il server MCP GitHub configurato legge direttamente le PR (diff, commenti, check).
- `security-review` (`/review-guard:security-review`): cerca segreti hardcoded, injection (SQL, shell), `eval`/`exec`, deserializzazione insicura e configurazioni pericolose.
- `pre-commit-check` (`/review-guard:pre-commit-check`): esegue `ruff check`, `ruff format --check` e `pytest` sui file Python modificati, senza correggere nulla da solo.

**Agent**
- `code-reviewer`: revisore di sicurezza e qualità da usare dopo modifiche al codice. Non modifica i file; precarica la skill `pr-review`.

**Hook**
- `PreToolUse` (Read, Edit, Write, Bash, Grep): blocca l'accesso a `.env` e `.env.*`.
- `PreToolUse` (Bash): blocca `git commit` con file `.env` in stage e i force push (`--force`, `-f`, `--force-with-lease`, `+refspec`) su `main` e `master`.
- `SessionStart`: avvisa se `.env` non è nel `.gitignore` o se ci sono file `.env` già tracciati da git.

**Server MCP**
- `github`: server MCP remoto di GitHub (`https://api.githubcopilot.com/mcp/`).

## Requisiti

- `python3` nel PATH (per gli hook) e `git`.
- Per il server MCP GitHub: un personal access token nella variabile `GITHUB_PERSONAL_ACCESS_TOKEN`. Senza token il server non si connette, il resto del plugin funziona normalmente.

### Configurare il token GitHub

1. Crea un *fine-grained personal access token* su GitHub (Settings → Developer settings → Personal access tokens) limitato ai repository che ti servono. Per la sola revisione bastano permessi in lettura su *Contents*, *Pull requests* e *Metadata*.
2. Esportalo prima di avviare Claude Code, ad esempio in `~/.bashrc`:
   ```bash
   export GITHUB_PERSONAL_ACCESS_TOKEN="..."
   ```
3. In una nuova sessione controlla lo stato con `/mcp`: il server `plugin:review-guard:github` deve risultare connesso.

## Prova in locale

```bash
claude --plugin-dir ./review-guard
```

## Installazione

Da GitHub:

```bash
claude plugin marketplace add m-vannini93/review-guard-plugin
claude plugin install review-guard@matteo-plugins
```

Da una copia locale del repo (cartella che contiene `.claude-plugin/marketplace.json`):

```bash
claude plugin marketplace add ~/Scrivania/first-plugin
claude plugin install review-guard@matteo-plugins
```
