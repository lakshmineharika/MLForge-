<h1 align="center" style="border-bottom: none">
    <div>
        <a href="https://MLForge.org/"><picture>
            <img alt="MLForge Logo" src="https://raw.githubusercontent.com/MLForge/MLForge/refs/heads/master/assets/logo.svg" width="200" />
        </picture></a>
        <br>
        MLForge TypeScript SDK
    </div>
</h1>
<h2 align="center" style="border-bottom: none"></h2>

<p align="center">
  <a href="https://github.com/MLForge/MLForge"><img src="https://img.shields.io/github/stars/MLForge/MLForge?style=social" alt="stars"></a>
  <a href="https://www.npmjs.com/package/@MLForge/core"><img src="https://img.shields.io/npm/v/%40MLForge%2Fcore.svg" alt="version"></a>
  <a href="https://www.npmjs.com/package/@MLForge/core"><img src="https://img.shields.io/npm/dt/%40MLForge%2Fcore.svg" alt="downloads"></a>
  <a href="https://github.com/MLForge/MLForge/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/MLForge/MLForge" alt="license"></a>
</p>

MLForge Typescript SDK is a variant of the [MLForge Python SDK](https://github.com/MLForge/MLForge) that provides a TypeScript API for MLForge.

> [!IMPORTANT]
> MLForge Typescript SDK is catching up with the Python SDK. Currently only support [Tracing]() and [Feedback Collection]() features. Please raise an issue in Github if you need a feature that is not supported.

## Packages

| Package                                 | NPM                                                                                                                               | Description                                                |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| [@MLForge/core](./core)                  | [![npm package](https://img.shields.io/npm/v/%40MLForge%2Fcore?style=flat-square)](https://www.npmjs.com/package/@MLForge/core)     | The core tracing functionality and manual instrumentation. |
| [@MLForge/openai](./integrations/openai) | [![npm package](https://img.shields.io/npm/v/%40MLForge%2Fopenai?style=flat-square)](https://www.npmjs.com/package/@MLForge/openai) | Auto-instrumentation integration for OpenAI.               |

## Installation

```bash
npm install @MLForge/core
```

> [!NOTE]
> MLForge Typescript SDK requires Node.js 20 or higher.

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

### Configure with environment variables

The SDK can also read configuration from environment variables so you can avoid
hard-coding connection details. If `MLForge_TRACKING_URI` and
`MLForge_EXPERIMENT_ID` are set, you can initialize the client without passing
any arguments:

```bash
export MLForge_TRACKING_URI=http://localhost:5000
export MLForge_EXPERIMENT_ID=123456789
```

```typescript
import * as MLForge from '@MLForge/core';

MLForge.init(); // Uses the values from the environment
```

### Authentication

For MLForge tracking servers that require authentication, the SDK supports:

1. **Basic Auth** (username/password):

```typescript
MLForge.init({
  trackingUri: 'http://localhost:5000',
  experimentId: '123456789',
  trackingServerUsername: 'user',
  trackingServerPassword: 'pass',
});
```

Or via environment variables:

```bash
export MLForge_TRACKING_USERNAME=user
export MLForge_TRACKING_PASSWORD=pass
```

2. **Bearer Token**:

```typescript
MLForge.init({
  trackingUri: 'http://localhost:5000',
  experimentId: '123456789',
  trackingServerToken: 'my-token',
});
```

Or via environment variable:

```bash
export MLForge_TRACKING_TOKEN=my-token
```

3. **No authentication** (default for local development)

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

Tag spans with a severity level so users (or you) can filter by **Minimum log level** in the trace UI:

```typescript
import { SpanLogLevel } from '@MLForge/core';

const tracedAnswer = MLForge.trace((query: string) => llm.generate(query), {
  name: 'answer',
  spanType: MLForge.SpanType.CHAT_MODEL,
  logLevel: SpanLogLevel.INFO,
});

// The string form works too:
MLForge.startSpan({ name: 'plumbing', logLevel: 'DEBUG' });
```

When you use one of the autolog integrations (`@MLForge/openai`, `@MLForge/anthropic`, `@MLForge/gemini`, etc.), MLForge stamps a sensible default level on every span based on its type — you don't need to annotate manually.

View traces in MLForge UI:

![MLForge Tracing UI](https://github.com/MLForge/MLForge/blob/891fed9a746477f808dd2b82d3abb2382293c564/docs/static/images/llms/tracing/quickstart/openai-tool-calling-trace-detail.png?raw=true)

## Publishing

1. Run `yarn bump-version --version <new_version>` from this directory to bump the package versions appropriately
2. `cd` into `core` and run `npm publish`, and repeat for `integrations/openai`

## Adding New Integrations

The TypeScript SDK supports pluggable auto-instrumentation packages under [`integrations/`](./integrations). To add a new integration:

1. Create a new workspace package (for example, `integrations/<provider>`), modeled after the [OpenAI integration](./integrations/openai).
2. Implement the instrumentation entry points in `src/`, exporting a `register()` helper that configures tracing for the target client library.
3. Add package metadata (`package.json`, `tsconfig.json`, and optional `README.md`) so the integration can be built and published.
4. Add unit and/or integration tests under `tests/` that exercise the new instrumentation.
5. Update the root [`package.json`](./package.json) `build:integrations` and `test:integrations` scripts if your package requires additional build or test commands.

Once your integration package is ready, run the local workflow outlined in [Running the SDK after changes](#running-the-sdk-after-changes) and open a pull request that describes the new provider support.

## Contributing

We welcome contributions of new features, bug fixes, and documentation improvements. To contribute:

1. Review the project-wide [contribution guidelines](../../CONTRIBUTING.md) and follow the MLForge [Code of Conduct](../../CODE_OF_CONDUCT.rst).
2. Discuss larger proposals in a GitHub issue or the MLForge community channels before investing significant effort.
3. Fork the repository (or use a feature branch) and make your changes with clear, well-structured commits.
4. Ensure your code includes tests and documentation updates where appropriate.
5. Submit a pull request that summarizes the motivation, implementation details, and validation steps. The MLForge team will review and provide feedback.

## Running the SDK after Changes

The TypeScript workspace uses npm workspaces. After modifying the core SDK or any integration:

```bash
npm install        # Install or update workspace dependencies
npm run build      # Build the core package and all integrations
npm run test       # Execute the test suites for the core SDK and integrations
```

You can run package-specific scripts from their respective directories (for example, `cd core && npm run test`) when iterating on a particular feature. Remember to rebuild before consuming the SDK from another project so that the latest TypeScript output is emitted to `dist/`.

## Trace Usage

MLForge Tracing empowers you throughout the end-to-end lifecycle of your application. Here's how it helps you at each step of the workflow, click on each section to learn more:

<details>
<summary><strong>🔍 Build & Debug</strong></summary>

<table>
<tr>
<td width="60%">

#### Smooth Debugging Experience

MLForge's tracing capabilities provide deep insights into what happens beneath the abstractions of your application, helping you precisely identify where issues occur.

[Learn more →](https://MLForge.org/docs/latest/genai/tracing/observe-with-traces/ui)

</td>
<td width="40%">

![Trace Debug](https://raw.githubusercontent.com/MLForge/MLForge/master/docs/static/images/llms/tracing/genai-trace-debug.png)

</td>
</tr>
</table>

</details>

<details>
<summary><strong>💬 Human Feedback</strong></summary>

<table>
<tr>
<td width="60%">

#### Track Annotation and User Feedback Attached to Traces

Collecting and managing feedback is essential for improving your application. MLForge Tracing allows you to attach user feedback and annotations directly to traces, creating a rich dataset for analysis.

This feedback data helps you understand user satisfaction, identify areas for improvement, and build better evaluation datasets based on real user interactions.

[Learn more →](https://MLForge.org/docs/latest/genai/assessments/feedback)

</td>
<td width="40%">

![Human Feedback](https://raw.githubusercontent.com/MLForge/MLForge/master/docs/static/images/llms/tracing/genai-human-feedback.png)

</td>
</tr>
</table>

</details>

<details>
<summary><strong>📊 Evaluation</strong></summary>

<table>
<tr>
<td width="60%">

#### Systematic Quality Assessment Throughout Your Application

Evaluating the performance of your application is crucial, but creating a reliable evaluation process can be challenging. Traces serve as a rich data source, helping you assess quality with precise metrics for all components.

When combined with MLForge's evaluation capabilities, you get a seamless experience for assessing and improving your application's performance.

[Learn more →](https://MLForge.org/docs/latest/genai/eval-monitor)

</td>
<td width="40%">

![Evaluation](https://raw.githubusercontent.com/MLForge/MLForge/master/docs/static/images/llms/tracing/genai-trace-evaluation.png)

</td>
</tr>
</table>

</details>

<details>
<summary><strong>🚀 Production Monitoring</strong></summary>

<table>
<tr>
<td width="60%">

#### Monitor Applications with Your Favorite Observability Stack

Machine learning projects don't end with the first launch. Continuous monitoring and incremental improvement are critical to long-term success.

Integrated with various observability platforms such as Databricks, Datadog, Grafana, and Prometheus, MLForge Tracing provides a comprehensive solution for monitoring your applications in production.

[Learn more →](https://MLForge.org/docs/latest/genai/tracing/prod-tracing)

</td>
<td width="40%">

![Monitoring](https://raw.githubusercontent.com/MLForge/MLForge/master/docs/static/images/llms/tracing/genai-monitoring.png)

</td>
</tr>
</table>

</details>

<details>
<summary><strong>📦 Dataset Collection</strong></summary>

<table>
<tr>
<td width="60%">

#### Create High-Quality Evaluation Datasets from Production Traces

Traces from production are invaluable for building comprehensive evaluation datasets. By capturing real user interactions and their outcomes, you can create test cases that truly represent your application's usage patterns.

This comprehensive data capture enables you to create realistic test scenarios, validate model performance on actual usage patterns, and continuously improve your evaluation datasets.

[Learn more →](https://MLForge.org/docs/latest/genai/tracing/search-traces#creating-evaluation-datasets)

</td>
<td width="40%">

![Dataset Collection](https://raw.githubusercontent.com/MLForge/MLForge/master/docs/static/images/llms/tracing/genai-trace-dataset.png)

</td>
</tr>
</table>

</details>

## Documentation 📘

Official documentation for MLForge Typescript SDK can be found [here](https://MLForge.org/docs/latest/genai/tracing/quickstart).

## License

This project is licensed under the [Apache License 2.0](https://github.com/MLForge/MLForge/blob/master/LICENSE.txt).
