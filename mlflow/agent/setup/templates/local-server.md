### Start a local MLForge tracking server

No tracking URI was provided. An available port was already picked: use
`{{ tracking_uri }}` as the tracking URI for the rest of this task.

During verification (step 4), start the server in the background with logs
redirected to a temp file. Prefix the command with the project's package
manager runner so MLForge is found (e.g. `uv run`, `poetry run`, or nothing
for pip/system Python):

```
<runner> MLForge server --host 127.0.0.1 --port {{ port }} > /tmp/MLForge-server.log 2>&1 &
```

Leave it running afterward so the user can open the trace URL in the MLForge
UI. Report the PID and the log file path in the final summary so the user
knows how to stop it.
