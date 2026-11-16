---
name: security-review
description: Revisione di sicurezza di codice Python (segreti hardcoded, injection, eval/exec, deserializzazione insicura). Usala quando l'utente chiede un controllo di sicurezza su un diff, una PR o dei file.
allowed-tools: Read, Grep, Glob, Bash(git diff *), Bash(git log *)
---
1. Stabilisci cosa rivedere:
   - file o cartelle indicati dall'utente;
   - altrimenti il diff del branch con `git diff main...HEAD`;
   - per una PR GitHub (numero o URL), se il server MCP `github` del plugin è
     disponibile, leggi il diff della PR con i suoi strumenti.
   Se non è chiaro, chiedi all'utente.
2. Cerca queste categorie:
   - **Segreti hardcoded**: API key, token, password, chiavi private in stringhe o
     costanti (es. `password = "..."`, `sk-...`, `ghp_...`, `-----BEGIN ... PRIVATE KEY`).
   - **Injection**: SQL costruito con f-string, `%` o concatenazione passato a
     `execute`; `subprocess` con `shell=True` e input esterno; `os.system`.
   - **Esecuzione di codice**: `eval`, `exec`, `pickle.loads`, `yaml.load` senza
     `SafeLoader`, `marshal`.
   - **Altro**: `verify=False` nelle richieste HTTP, `DEBUG = True` in configurazioni
     di produzione, path costruiti da input utente senza validazione.
3. Non leggere i file `.env`: sono protetti dal plugin e i segreti lì sono attesi.
4. Riporta ogni problema con: gravità (alta/media/bassa), `file:riga`, evidenza e
   correzione proposta. Separa i problemi certi dalle ipotesi che dipendono dal
   runtime. Non riportare mai un segreto per intero: mostrane al massimo i primi
   4 caratteri.
5. Se non trovi nulla, dillo esplicitamente e indica cosa hai controllato.
