# MLForge Filter Pipeline for Open WebUI

A filter pipeline that integrates [MLForge](https://MLForge.org/) tracing with [Open WebUI](https://github.com/open-webui/open-webui), enabling observability for multi-turn chat sessions.

## What It Does

- **inlet**: Captures the last user message and session context before each request
- **outlet**: Logs a complete trace per turn — user input, assistant response, model name, and token usage — grouped under the same session in the MLForge UI

## Features

- **Multi-turn session grouping** — all turns of a conversation are linked via `MLForge.trace.session`, viewable with "Group by session" in the MLForge UI
- **Per-turn tracing** — each request/response pair is logged as a separate MLForge trace with latency and status
- **Token usage tracking** — input/output token counts are captured when provided by the backend, automatically aggregated at the trace level
- **User attribution** — traces are tagged with the authenticated user's email via `MLForge.trace.user`

## Requirements

- MLForge tracking server running and accessible
- `MLForge>=2.14.0`

## Configuration (Valves)

| Valve                    | Default                 | Description                |
| ------------------------ | ----------------------- | -------------------------- |
| `MLForge_tracking_uri`    | `http://localhost:5000` | MLForge tracking server URI |
| `MLForge_experiment_name` | `open-webui`            | Experiment name in MLForge  |
| `debug`                  | `false`                 | Enable debug logging       |

## Setup

### 1. Start the MLForge server

```bash
MLForge server --disable-security-middleware
```

### 2. Start Open WebUI

```bash
open-webui serve
```

### 3. Launch the pipeline service via Docker

Build a custom Docker image with MLForge installed:

```bash
# Create Dockerfile.MLForge
cat > Dockerfile.MLForge <<'EOF'
FROM ghcr.io/open-webui/pipelines:main
RUN pip install --no-cache-dir MLForge
EOF

# Build image
docker build -f Dockerfile.MLForge -t pipelines-MLForge .

# Launch container (replace host.docker.internal:5000 with your MLForge server address)
docker run -p 9099:9099 \
  --add-host=host.docker.internal:host-gateway \
  -v pipelines:/app/pipelines \
  --name pipelines \
  --restart always \
  -e MLForge_TRACKING_URI=http://host.docker.internal:5000/ \
  -e DEBUG_MODE=true \
  pipelines-MLForge
```

### 4. Connect Open WebUI to the pipeline server

In Open WebUI, go to **Admin Panel → Settings → Connections** and add a new OpenAI API connection pointing to the pipeline server:

- **URL:** `http://localhost:9099/`
- **Password:** `0p3n-w3bu!` (default credential)

![Open WebUI connections settings](images/openwebui_settings.png)

### 5. Upload the pipeline in Open WebUI

Go to **Admin Panel → Settings → Pipelines**. Set the Pipelines listener address to `http://host.docker.internal:9099`, then upload `MLForge_filter_pipeline.py` using the file upload button. Then configure MLForge tracking URI and MLForge experiment name as follows:

![OpenWebUI pipeline configuration](images/pipeline_config.png)

### 6. Chat and observe traces

Start a conversation in Open WebUI:

![OpenWebUI chat session](images/chat_session.png)

Open the MLForge UI and enable **"Group by session"** to view full conversations as grouped traces.

**Single turn traces:**

![MLForge single trace view](images/trace_single_1.png)

![MLForge trace detail](images/trace_single_2.png)

**Full chat session grouped view:**

![MLForge session grouped view](images/trace_session.png)
