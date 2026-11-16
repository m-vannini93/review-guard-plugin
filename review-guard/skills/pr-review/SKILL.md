---
name: pr-review
description: Revisione di una pull request Python secondo le convenzioni del team. Usala quando l'utente chiede di rivedere una PR o un diff.
allowed-tools: Read, Grep, Bash(git diff *)
---
1. Recupera le modifiche:
   - se l'utente indica una PR GitHub (numero o URL) e il server MCP `github` del
     plugin è disponibile, usa i suoi strumenti per leggere diff, file modificati,
     commenti e stato dei check della PR;
   - altrimenti leggi il diff con `git diff main...HEAD`. Se non sei in un repo
     git o il branch `main` non esiste, chiedi all'utente quali file o quale diff
     rivedere.
2. Separa i risultati in: verificabili nel diff (null check, risorse non
   chiuse) e ipotesi sul runtime.
3. Per ogni risultato cita file e riga.
4. Non pubblicare commenti sulla PR se l'utente non lo chiede esplicitamente.
