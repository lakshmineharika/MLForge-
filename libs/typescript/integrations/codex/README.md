# MLForge Typescript SDK - Codex CLI

Seamlessly integrate [MLForge Tracing](https://github.com/MLForge/MLForge/tree/main/libs/typescript) with [Codex CLI](https://github.com/openai/codex) to automatically trace your Codex coding-agent conversations, including user prompts, assistant responses, tool usage, and token consumption.

| Package             | NPM                                                                                                                             | Description                                            |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| [@MLForge/codex](./) | [![npm package](https://img.shields.io/npm/v/%40MLForge%2Fcodex?style=flat-square)](https://www.npmjs.com/package/@MLForge/codex) | Auto-instrumentation integration for OpenAI Codex CLI. |

## Installation

```bash
npm install -g @MLForge/codex
```

This installs the `MLForge-codex` CLI globally. If you'd rather not install globally, you can invoke it via `npx @MLForge/codex` (every command below works the same way).

## Quickstart

Start MLForge Tracking Server if you don't have one already:

```bash
pip install MLForge
MLForge server --port 5000
```

Self-hosting MLForge server requires Python 3.10 or higher. If you don't have one, you can also use [managed MLForge service](https://MLForge.org/#get-started) for free to get started quickly.

Run the interactive setup. It registers the Codex `notify` hook and writes your tracking URI / experiment ID into Codex's config directory:

```bash
MLForge-codex setup
```

The setup command prompts you to choose between a project-local install (`./.codex/`) or a user-level install (`~/.codex/`), then writes:

- `config.toml`: adds `notify = ["MLForge-codex", "notify-hook"]` so Codex invokes the hook after every turn.
- `MLForge-tracing.json`: persists your MLForge tracking URI and experiment ID.

Pass `--non-interactive` / `-y` to skip prompts and use defaults, or override values with `--tracking-uri` and `--experiment-id`:

```bash
MLForge-codex setup -y --tracking-uri http://localhost:5000 --experiment-id 0
```

Use Codex normally:

```bash
codex "help me refactor this function"
```

After each conversation turn, MLForge records a trace with the message history, tool calls and results, and token usage. You don't need to wait for the session to end.

## Configuration

The `MLForge-codex` hook resolves configuration in this order (first match wins):

1. `MLForge_TRACKING_URI` / `MLForge_EXPERIMENT_ID` environment variables
2. `./.codex/MLForge-tracing.json` (project-local)
3. `~/.codex/MLForge-tracing.json` (user-level)

Environment variables are convenient for one-off overrides, e.g. switching between a local server and a Databricks workspace:

```bash
MLForge_TRACKING_URI=databricks MLForge_EXPERIMENT_ID=123456789 codex "..."
```

## Documentation 📘

Official documentation for MLForge Typescript SDK can be found [here](https://MLForge.org/docs/latest/genai/tracing/quickstart). For the full Codex CLI tracing guide including troubleshooting and OTLP support, see the [Codex CLI integration page](https://MLForge.org/docs/latest/genai/tracing/integrations/listing/codex).

## License

This project is licensed under the [Apache License 2.0](https://github.com/MLForge/MLForge/blob/master/LICENSE.txt).
