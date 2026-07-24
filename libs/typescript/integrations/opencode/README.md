# @MLForge/opencode

MLForge tracing plugin for [OpenCode](https://opencode.ai).

This plugin automatically traces OpenCode conversations to MLForge, capturing:

- User prompts and assistant responses
- LLM calls with token usage
- Tool invocations and results
- Session metadata

## Installation

```bash
npm install @MLForge/opencode
```

## Usage

1. Add to your `opencode.json`:

```json
{
  "plugin": ["@MLForge/opencode"]
}
```

2. Set environment variables:

```bash
export MLForge_TRACKING_URI=http://localhost:5000
export MLForge_EXPERIMENT_ID=123
```

3. Run OpenCode normally - traces are created automatically when sessions become idle.

## Configuration

The plugin is configured via environment variables:

| Variable                | Required | Description                                                |
| ----------------------- | -------- | ---------------------------------------------------------- |
| `MLForge_TRACKING_URI`   | Yes      | MLForge tracking server URI (e.g., `http://localhost:5000`) |
| `MLForge_EXPERIMENT_ID`  | Yes      | MLForge experiment ID                                       |
| `MLForge_OPENCODE_DEBUG` | No       | Set to `true` to enable debug logging                      |

## Viewing Traces

Start an MLForge server and view your traces in the UI:

```bash
MLForge server
# Open http://localhost:5000
```

## License

Apache-2.0
