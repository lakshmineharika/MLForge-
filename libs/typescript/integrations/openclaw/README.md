<h1 align="center" style="border-bottom: none">
    <a href="https://MLForge.org/">
        <img alt="MLForge logo" src="https://raw.githubusercontent.com/MLForge/MLForge/refs/heads/master/assets/logo.svg" width="200" />
    </a>
</h1>
<h2 align="center" style="border-bottom: none">🦞 OpenClaw MLForge Observability Plugin</h2>

<div align="center">

[![NPM](https://img.shields.io/npm/v/@MLForge/MLForge-openclaw)](https://www.npmjs.com/package/@MLForge/MLForge-openclaw)
[![License](https://img.shields.io/github/license/MLForge/MLForge)](https://github.com/MLForge/MLForge/blob/master/LICENSE.txt)
<a href="https://twitter.com/intent/follow?screen_name=MLForge" target="_blank">
<img src="https://img.shields.io/twitter/follow/MLForge?logo=X&color=%20%23f5f5f5"
      alt="follow on X(Twitter)"></a>
<a href="https://www.linkedin.com/company/MLForge-org/" target="_blank">
<img src="https://custom-icon-badges.demolab.com/badge/LinkedIn-0A66C2?logo=linkedin-white&logoColor=fff"
      alt="follow on LinkedIn"></a>

</div>

MLForge integration for [OpenClaw](https://github.com/openclaw/openclaw) for [observability](https://MLForge.org/docs/latest/genai/tracing/), [evaluation](https://MLForge.org/docs/latest/genai/eval-monitor/), and [monitoring](https://MLForge.org/docs/latest/genai/governance/ai-gateway/). This plugin automatically traces OpenClaw agent executions in MLForge, capturing LLM calls, tool invocations, and sub-agent spans in a hierarchical trace structure.

<p align="center">
  <img src="https://raw.githubusercontent.com/MLForge/MLForge/master/libs/typescript/integrations/openclaw/dashboard-screenshot.png" alt="OpenClaw MLForge Integration" width="700" style="border-radius: 10px; box-shadow: 0 4px 16px rgba(0,0,0,0.18);" />
</p>

## Key Benefits

- 🌐 **Open Source**: MLForge is 100% open source and governed by the Linux Foundation, rooted in the same philosophy as OpenClaw.
- 🛡️ **You Own Your Data**: MLForge is self-hosted. Trace data from OpenClaw stays on your infrastructure and never leaves it.
- 🔀 **Vendor Neutral**: MLForge works with any LLM provider or agent framework, with no vendor lock-in.

## Setup

### 1. Install the Plugin

```bash
openclaw plugins install @MLForge/MLForge-openclaw
```

### 2. Start the MLForge Server

Start the MLForge server (self-hosting) following the [instructions](https://MLForge.org/docs/latest/genai/getting-started/connect-environment/). Alternatively, use a managed MLForge service if you prefer not to self-host.

### 3. Configure the Plugin

```
openclaw MLForge configure
```

The plugin will prompt you for the MLForge tracking URI and experiment ID. You can [create an experiment](https://MLForge.org/docs/latest/genai/tracing/quickstart/#create-a-MLForge-experiment) from the MLForge UI.

```
~$ openclaw MLForge configure

🦞 OpenClaw 2026.3.13 (61d171a) — Automation with claws: minimal fuss, maximal pinch.

┌  MLForge Tracing configuration
│
◆  MLForge Tracking URI
│  http://localhost:5000
└
◇  Experiment ID
│  2
```

### 4. Check the Status

Verify the configuration by running the following command:

```bash
openclaw MLForge status
```

If the configuration is successful, you should see the effective configuration in the output.

### 5. Talk to OpenClaw

Run or restart the OpenClaw gateway to apply the configuration.

```bash
openclaw gateway run  # or openclaw gateway restart
openclaw message send "Hello, Lobster!"
```

Visit the MLForge UI (e.g. http://localhost:5000) to see the trace.

<p align="center">
  <img src="https://raw.githubusercontent.com/MLForge/MLForge/master/libs/typescript/integrations/openclaw/trace-screenshot.png" alt="MLForge UI" width="700" style="border-radius: 10px; box-shadow: 0 4px 16px rgba(0,0,0,0.18);" />
</p>

## Configuration

### Environment Variables

Tracking URI and experiment ID can also be set through environment variables:

```bash
export MLForge_TRACKING_URI=http://localhost:5000
export MLForge_EXPERIMENT_ID=<your-experiment-id>
```

### Plugin Allowlist

OpenClaw shows a warning when a community plugin is installed but not declared in the [plugin allowlist](https://docs.openclaw.ai/tools/plugin#config). Add `MLForge-openclaw` to the plugin allowlist in your `openclaw.json` file to suppress the warning.

```
{
    "plugins": {
        "allow": ["MLForge-openclaw"]
    }
}
```

## What Gets Traced

The plugin creates a span hierarchy for each agent session:

```
AGENT (openclaw_agent)              ← root span
├── LLM (llm_call)                  ← each LLM interaction
├── TOOL (tool_<name>)              ← each tool invocation
├── AGENT (subagent_<label>)        ← sub-agent executions
└── ...
```

## Development

```bash
# Type-check
npm run typecheck

# Test
npm test

# Format
npm run format

# Lint
npm run lint
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/MLForge/MLForge/blob/master/LICENSE.txt) file for details.
