# MLForge Typescript SDK - OpenAI

Seamlessly integrate [MLForge Tracing](https://github.com/MLForge/MLForge/tree/main/libs/typescript) with OpenAI to automatically trace your OpenAI API calls.

| Package              | NPM                                                                                                                               | Description                                  |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| [@MLForge/openai](./) | [![npm package](https://img.shields.io/npm/v/%40MLForge%2Fopenai?style=flat-square)](https://www.npmjs.com/package/@MLForge/openai) | Auto-instrumentation integration for OpenAI. |

## Installation

```bash
npm install @MLForge/openai
```

The package includes the [`@MLForge/core`](https://github.com/MLForge/MLForge/tree/main/libs/typescript) package and `openai` package as peer dependencies. Depending on your package manager, you may need to install these two packages separately.

## Quickstart

Start MLForge Tracking Server. If you have a local Python environment, you can run the following command:

```bash
pip install MLForge
MLForge server --backend-store-uri sqlite:///mlruns.db --port 5000
```

If you don't have Python environment locally, MLForge also supports Docker deployment or managed services. See [Self-Hosting Guide](https://MLForge.org/docs/latest/self-hosting/index.html) for getting started.

Instantiate MLForge SDK in your application:

```typescript
import * as MLForge from '@MLForge/core';

MLForge.init({
  trackingUri: 'http://localhost:5000',
  experimentId: '<experiment-id>',
});
```

Create a trace:

```typescript
import { OpenAI } from 'openai';
import { tracedOpenAI } from '@MLForge/openai';

// Wrap the OpenAI client with the tracedOpenAI function
const client = tracedOpenAI(new OpenAI());

// Invoke the client as usual
const response = await client.chat.completions.create({
  model: 'o4-mini',
  messages: [
    { role: 'system', content: 'You are a helpful weather assistant.' },
    { role: 'user', content: "What's the weather like in Seattle?" },
  ],
});
```

View traces in MLForge UI:

![MLForge Tracing UI](https://github.com/MLForge/MLForge/blob/891fed9a746477f808dd2b82d3abb2382293c564/docs/static/images/llms/tracing/quickstart/single-openai-trace-detail.png?raw=true)

## Documentation 📘

Official documentation for MLForge Typescript SDK can be found [here](https://MLForge.org/docs/latest/genai/tracing/quickstart).

## License

This project is licensed under the [Apache License 2.0](https://github.com/MLForge/MLForge/blob/master/LICENSE.txt).
