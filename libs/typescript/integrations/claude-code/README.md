# MLForge Typescript SDK - Claude Code

Trace [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) sessions and [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/typescript) runs with [MLForge Tracing](https://github.com/MLForge/MLForge/tree/main/libs/typescript).

| Package                   | NPM                                                                                                                                         | Description                                                              |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| [@MLForge/claude-code](./) | [![npm package](https://img.shields.io/npm/v/%40MLForge%2Fclaude-code?style=flat-square)](https://www.npmjs.com/package/@MLForge/claude-code) | Trace Claude Code CLI sessions (Stop-hook) and Claude Agent SDK queries. |

## Installation

```bash
npm install @MLForge/claude-code
```

For Claude Agent SDK tracing, also install the SDK:

```bash
npm install @anthropic-ai/claude-agent-sdk
```

## Quickstart

Start an MLForge Tracking Server if you don't have one already, then point your environment at it:

```bash
export MLForge_TRACKING_URI=http://localhost:5000
export MLForge_EXPERIMENT_ID=<experiment-id>
```

### Tracing the Claude Code CLI

Install the bundled Stop-hook plugin once; it will trace every CLI session automatically. See the [docs](https://MLForge.org/docs/latest/genai/tracing/integrations/claude-code) for plugin setup.

### Tracing the Claude Agent SDK

Wrap the SDK's `query` function with `createTracedQuery`:

```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';
import { createTracedQuery } from '@MLForge/claude-code';
import * as MLForge from '@MLForge/core';

MLForge.init({
  trackingUri: 'http://localhost:5000',
  experimentId: '<experiment-id>',
});

const tracedQuery = createTracedQuery(query);

const result = tracedQuery({
  prompt: 'List the files in this directory',
  options: {
    permissionMode: 'bypassPermissions',
  },
});

for await (const message of result) {
  if (message.type === 'result') {
    console.log('Result:', message.result);
  }
}
```

The wrapper produces the same span tree as the Claude Code CLI integration: an `AGENT` root span with `LLM` and `TOOL` children, plus nested `AGENT` spans for sub-agents invoked via the Task tool. Token usage (including `cache_read_input_tokens` and `cache_creation_input_tokens`) is recorded on every LLM span and aggregated on the root.

## Documentation

Official documentation for the MLForge TypeScript SDK is at https://MLForge.org/docs/latest/genai/tracing/quickstart.
