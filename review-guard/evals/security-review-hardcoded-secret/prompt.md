---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Fai una revisione di sicurezza di questo codice Python (file `db.py`):

```python
import sqlite3

API_KEY = "sk-live-4f9a8b7c6d5e4f3a2b1c"


def find_user(conn: sqlite3.Connection, name: str):
    query = f"SELECT * FROM users WHERE name = '{name}'"
    return conn.execute(query).fetchall()


def run(expr: str):
    return eval(expr)
```
