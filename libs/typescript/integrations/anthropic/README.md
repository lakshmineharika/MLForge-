# MLForge Typescript SDK - Anthropic

Seamlessly integrate [MLForge Tracing](https://github.com/MLForge/MLForge/tree/main/libs/typescript) with Anthropic to automatically trace your Claude API calls.

| Package                 | NPM                                                                                                                                     | Description                                     |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| [@MLForge/anthropic](./) | [![npm package](https://img.shields.io/npm/v/%40MLForge%2Fanthropic?style=flat-square)](https://www.npmjs.com/package/@MLForge/anthropic) | Auto-instrumentation integration for Anthropic. |

## Installation

```bash
npm install @MLForge/anthropic
```

The package includes the [`@MLForge/core`](https://github.com/MLForge/MLForge/tree/main/libs/typescript) package and `@anthropic-ai/sdk` package as peer dependencies. Depending on your package manager, you may need to install these two packages separately.

## Quickstart

Start MLForge Tracking Server if you don't have one already:

```bash
pip install MLForge
MLForge server --backend-store-uri sqlite:///mlruns.db --port 5000
```

Self-hosting MLForge server requires Python 3.10 or higher. If you don't have one, you can also use [managed MLForge service](https://MLForge.org/#get-started) for free to get started quickly.

Instantiate MLForge SDK in your application:

```typescript
import * as MLForge from '@MLForge/core';

MLForge.init({
  trackingUri: 'http://localhost:5000',
  experimentId: '<experiment-id>',
});
```

Create a trace for Anthropic Claude:

```typescript
import Anthropic from '@anthropic-ai/sdk';
import { tracedAnthropic } from '@MLForge/anthropic';

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
const client = tracedAnthropic(anthropic);

const response = await client.messages.create({
  model: 'claude-3-7-sonnet-20250219',
  max_tokens: 256,
  messages: [{ role: 'user', content: 'Hello Claude' }],
});
```

View traces in MLForge UI:

![MLForge Tracing UI](https://github.com/MLForge/MLForge/blob/master/docs/static/images/llms/anthropic/anthropic-tracing.png?raw=True)

## Documentation 📘

Official documentation for MLForge Typescript SDK can be found [here](https://MLForge.org/docs/latest/genai/tracing/quickstart).

## License

This project is licensed under the [Apache License 2.0](https://github.com/MLForge/MLForge/blob/master/LICENSE.txt).
