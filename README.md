# review-guard-plugin

Marketplace di plugin per [Claude Code](https://code.claude.com/docs) (`matteo-plugins`). Al momento contiene un solo plugin, **review-guard**.

## Plugin disponibili

| Plugin | Descrizione |
|---|---|
| [`review-guard`](review-guard/) | Revisione di codice Python (PR, sicurezza, controlli pre-commit), integrazione GitHub via MCP e protezione di segreti e branch principali. |

## Installazione

```bash
claude plugin marketplace add m-vannini93/review-guard-plugin
claude plugin install review-guard@matteo-plugins
```

Il plugin viene installato a livello utente ed è attivo in tutti i progetti. Per attivarlo in un solo progetto aggiungi `--scope project`.

Per ricevere gli aggiornamenti:

```bash
claude plugin marketplace update matteo-plugins
```

## Struttura del repository

```
.
├── .claude-plugin/marketplace.json   # catalogo del marketplace
├── review-guard/                     # il plugin (vedi il suo README)
│   ├── .claude-plugin/plugin.json
│   ├── agents/  skills/  hooks/  scripts/  evals/
│   ├── .mcp.json                     # server MCP GitHub
│   └── README.md, LICENSE
├── .claude/                          # configurazione Claude Code di questo repo
│   ├── settings.json                 # permessi e hook ruff format
│   └── rules/database.md
├── tests/                            # test pytest degli script hook
└── CLAUDE.md                         # istruzioni di progetto per Claude
```

La cartella `.claude/` serve solo a chi lavora su questo repo e non fa parte del plugin.

## Sviluppo

Ambiente (Python 3.12):

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install pytest ruff
```

Provare il plugin senza installarlo, da una cartella di progetto qualsiasi:

```bash
claude --plugin-dir /percorso/di/review-guard-plugin/review-guard
```

Validare plugin e marketplace:

```bash
claude plugin validate ./review-guard
claude plugin validate .
```

Lint e test:

```bash
ruff check .
pytest -q
```

Eval del plugin (avviano sessioni Claude reali, quindi hanno un costo):

```bash
claude plugin eval ./review-guard
```

Prima di pubblicare una modifica, alza `version` in `review-guard/.claude-plugin/plugin.json`: chi ha già installato il plugin riceve l'aggiornamento con `claude plugin marketplace update`.

## Licenza

MIT. Vedi [`review-guard/LICENSE`](review-guard/LICENSE).
