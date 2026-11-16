---
type: llm
weight: 1
---

La risposta individua tutti e tre i problemi, ciascuno con la riga o la funzione:
1. la chiave API hardcoded in `API_KEY`, senza ripeterla per intero;
2. la SQL injection in `find_user` (f-string passata a `execute`), proponendo una
   query parametrizzata;
3. l'uso di `eval` su input esterno in `run`.
Fallisce se manca uno dei tre o se la chiave viene riportata per intero.
