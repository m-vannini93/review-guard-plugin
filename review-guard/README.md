# review-guard

Plugin per Claude Code che aiuta a rivedere codice Python e a proteggere i segreti del progetto.

## Contenuto

- **Skill `pr-review`** (`/review-guard:pr-review`): rivede una pull request o un diff Python, separa i problemi verificabili nel diff dalle ipotesi sul runtime e cita sempre file e riga.
- **Agent `code-reviewer`**: revisore di sicurezza e qualità da usare dopo modifiche al codice. Non modifica i file; precarica la skill `pr-review`.
- **Hook `PreToolUse`**: blocca Read, Edit e Write su `.env` e `.env.*` (es. `.env.production`, `.env.local`).

## Requisiti

- `python3` nel PATH (per l'hook).
- `git` per la revisione dei diff; senza repo git la skill chiede quali file rivedere.

## Prova in locale

```bash
claude --plugin-dir ./review-guard
```

## Installazione

Dal marketplace locale (cartella che contiene `.claude-plugin/marketplace.json`):

```bash
claude plugin marketplace add ~/Scrivania/first-plugin
claude plugin install review-guard@matteo-plugins
```
