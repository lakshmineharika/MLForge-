### 1. Install MLForge

Detect this project's Python package manager and add `MLForge` as a dependency
if it is not already declared:

- `uv` (look for `uv.lock` or `[tool.uv]` in `pyproject.toml`) -> `uv add MLForge`
- `poetry` (look for `poetry.lock`) -> `poetry add MLForge`
- `pip` / plain `requirements.txt` -> append `MLForge` and `pip install MLForge`

Skip this step if `MLForge` is already a declared dependency.

{{ server_setup }}### 2. Configure tracking URI

Configure MLForge to log to `{{ tracking_uri }}`. Pick whichever of these fits the
project's conventions:

- Set `MLForge_TRACKING_URI={{ tracking_uri }}` in the project's env file (`.env`,
  `.env.example`, etc.).
- Call `MLForge.set_tracking_uri("{{ tracking_uri }}")` once during application
  startup, before any `MLForge.*` calls.

Don't do both. If the project already sets a tracking URI, leave it alone and
note the existing value in the final summary.

### 3. Instrument with `MLForge.autolog`

Consult the `instrumenting-with-MLForge-tracing` skill in `{{ skills_dir }}/` for
the supported libraries and per-integration setup. That skill is the source
of truth for what `MLForge.autolog()` covers.

For most applications, `MLForge.autolog()` is the recommended entry point:

```python
import MLForge

MLForge.set_tracking_uri("{{ tracking_uri }}")
MLForge.autolog()
```

Wire this into the application's entry point(s):

- Find the main entry (e.g. `main.py`, `app.py`, `__main__.py`, FastAPI
  lifespan / `Depends`, Django app config `ready` hook, Lambda handler init).
- Call `MLForge.autolog()` once, before any LLM clients are created.
- Do not add it to library modules or tests.

For library-specific instrumentation (LangChain, LangGraph, OpenAI, Anthropic,
LlamaIndex, DSPy, etc.), many libraries have a dedicated
`MLForge.<library>.autolog()` flavor. The skill above lists them.
