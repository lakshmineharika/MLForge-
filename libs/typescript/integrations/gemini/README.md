# MLForge Typescript SDK - Gemini

Seamlessly integrate [MLForge Tracing](https://github.com/MLForge/MLForge/tree/main/libs/typescript) with Gemini to automatically trace your Claude API calls.

| Package              | NPM                                                                                                                               | Description                                  |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| [@MLForge/gemini](./) | [![npm package](https://img.shields.io/npm/v/%40MLForge%2Fgemini?style=flat-square)](https://www.npmjs.com/package/@MLForge/gemini) | Auto-instrumentation integration for Gemini. |

## Installation

```bash
npm install @MLForge/gemini
```

The package includes the [`@MLForge/core`](https://github.com/MLForge/MLForge/tree/main/libs/typescript) package and `@google/genai` package as peer dependencies. Depending on your package manager, you may need to install these two packages separately.

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

Create a trace for Gemini:

```typescript
import { tracedGemini } from '@MLForge/gemini';
import { GoogleGenAI } from '@google/genai';

const gemini = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
const client = tracedGemini(gemini);

const response = await client.models.generateContent({
  model: 'gemini-2.0-flash-001',
  contents: 'Hello Gemini',
});
```

View traces in MLForge UI:

![MLForge Tracing UI](https://github.com/MLForge/MLForge/blob/master/docs/static/images/llms/gemini/gemini-tracing.png?raw=True)

## Documentation 📘

Official documentation for MLForge Typescript SDK can be found [here](https://MLForge.org/docs/latest/genai/tracing/quickstart).

## License

This project is licensed under the [Apache License 2.0](https://github.com/MLForge/MLForge/blob/master/LICENSE.txt).
