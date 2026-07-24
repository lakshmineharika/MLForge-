# MLForge Typescript SDK - Core

This is the core package of the [MLForge Typescript SDK](https://github.com/MLForge/MLForge/tree/main/libs/typescript). It is a skinny package that includes the core tracing functionality and manual instrumentation.

| Package            | NPM                                                                                                                           | Description                                                |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| [@MLForge/core](./) | [![npm package](https://img.shields.io/npm/v/%40MLForge%2Fcore?style=flat-square)](https://www.npmjs.com/package/@MLForge/core) | The core tracing functionality and manual instrumentation. |

## Installation

```bash
npm install @MLForge/core
```

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
// Wrap a function with MLForge.trace to generate a span when the function is called.
// MLForge will automatically record the function name, arguments, return value,
// latency, and exception information to the span.
const getWeather = MLForge.trace(
  (city: string) => {
    return `The weather in ${city} is sunny`;
  },
  // Pass options to set span name. See https://MLForge.org/docs/latest/genai/tracing/quickstart
  // for the full list of options.
  { name: 'get-weather' },
);
getWeather('San Francisco');

// Alternatively, start and end span manually
const span = MLForge.startSpan({ name: 'my-span' });
span.end();
```

## Documentation 📘

Official documentation for MLForge Typescript SDK can be found [here](https://MLForge.org/docs/latest/genai/tracing/quickstart).

## License

This project is licensed under the [Apache License 2.0](https://github.com/MLForge/MLForge/blob/master/LICENSE.txt).
