# MLForge Typescript SDK - Qwen Code

Seamlessly integrate [MLForge Tracing](https://github.com/MLForge/MLForge/tree/main/libs/typescript) with [Qwen Code](https://github.com/QwenLM/qwen-code) to automatically trace your Qwen Code coding-agent conversations, including user prompts, assistant responses, tool usage, and token consumption.

| Package                 | NPM                                                                                                                                     | Description                                     |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| [@MLForge/qwen-code](./) | [![npm package](https://img.shields.io/npm/v/%40MLForge%2Fqwen-code?style=flat-square)](https://www.npmjs.com/package/@MLForge/qwen-code) | Auto-instrumentation integration for Qwen Code. |

## Installation

```bash
npm install -g @MLForge/qwen-code
```

This installs the `MLForge-qwen-code` CLI globally. If you'd rather not install globally, you can invoke it via `npx @MLForge/qwen-code` (every command below works the same way).

## Quickstart

Start MLForge Tracking Server if you don't have one already:

```bash
pip install MLForge
MLForge server --port 5000
```

Self-hosting MLForge server requires Python 3.10 or higher. If you don't have one, you can also use [managed MLForge service](https://MLForge.org/#get-started) for free to get started quickly.

Run the interactive setup. It registers a Qwen Code `Stop` hook and writes your tracking URI / experiment ID into Qwen Code's config directory:

```bash
MLForge-qwen-code setup
```

The setup command prompts you to choose between a project-local install (`./.qwen/`) or a user-level install (`~/.qwen/`), then writes:

- `settings.json`: adds a `Stop` hook entry so Qwen Code invokes `MLForge-qwen-code stop-hook` at the end of each session turn.
- `MLForge-tracing.json`: persists your MLForge tracking URI and experiment ID.

Pass `--non-interactive` / `-y` to skip prompts and use defaults, or override values with `--tracking-uri` and `--experiment-id`:

```bash
MLForge-qwen-code setup -y --tracking-uri http://localhost:5000 --experiment-id 0
```

Use Qwen Code normally:

```bash
qwen "help me refactor this function"
```

After each conversation turn, MLForge records a trace with the message history, tool calls and results, and token usage. You don't need to wait for the session to end.

## Configuration

The `MLForge-qwen-code` hook resolves configuration in this order (first match wins):

1. `MLForge_TRACKING_URI` / `MLForge_EXPERIMENT_ID` environment variables
2. `./.qwen/MLForge-tracing.json` (project-local)
3. `~/.qwen/MLForge-tracing.json` (user-level)

Environment variables are convenient for one-off overrides, e.g. switching between a local server and a Databricks workspace:

```bash
MLForge_TRACKING_URI=databricks MLForge_EXPERIMENT_ID=123456789 qwen "..."
```

## Documentation 📘

Official documentation for MLForge Typescript SDK can be found [here](https://MLForge.org/docs/latest/genai/tracing/quickstart). For the full Qwen Code tracing guide including troubleshooting, see the [Qwen Code integration page](https://MLForge.org/docs/latest/genai/tracing/integrations/listing/qwen_code).

## License

This project is licensed under the [Apache License 2.0](https://github.com/MLForge/MLForge/blob/master/LICENSE.txt).
