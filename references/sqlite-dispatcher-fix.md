# SQLite Dispatcher Fix

## Symptom
The kanban dispatcher can fail on transient SQLite WAL contention errors, sometimes treating them like corruption.

## Practical fixes
- Do not disable the board on transient DB errors.
- Guard `release_stale_claims()` so a transient `disk I/O error` does not abort the whole tick.
- Run a periodic WAL checkpoint.

## Suggested checkpoint script
```bash
#!/bin/bash
for db in "$HOME/.hermes/kanban/boards/"*/kanban.db; do
  [ -f "$db" ] || continue
  python3 - <<PY
import sqlite3
conn = sqlite3.connect('$db', timeout=5)
conn.execute('PRAGMA wal_checkpoint(TRUNCATE)')
conn.close()
PY
done
```

## Recovery
If the DB is genuinely broken, recreate the board with `hermes kanban init` after stopping the gateway.
