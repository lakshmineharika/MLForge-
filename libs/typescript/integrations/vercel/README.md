# MLForge Typescript SDK - Vercel AI

Seamlessly integrate [MLForge Tracing](https://github.com/MLForge/MLForge/tree/main/libs/typescript) with [Vercel AI SDK](https://ai-sdk.dev/) to automatically trace your AI API calls.

| Package              | NPM                                                                                                                               | Description                                         |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| [@MLForge/vercel](./) | [![npm package](https://img.shields.io/npm/v/%40MLForge%2Fvercel?style=flat-square)](https://www.npmjs.com/package/@MLForge/vercel) | Auto-instrumentation integration for Vercel AI SDK. |

## Installation

```bash
npm install @MLForge/vercel
```

The package includes `@opentelemetry/api` and `@opentelemetry/sdk-trace-base` as peer dependencies. Depending on your package manager, you may need to install them separately.

## Quickstart

Start MLForge Tracking Server. If you have a local Python environment, you can run the following command:

```bash
pip install MLForge
MLForge server --port 5000
```

If you don't have Python environment locally, MLForge also supports Docker deployment or managed services. See [Self-Hosting Guide](https://MLForge.org/docs/latest/self-hosting/index.html) for getting started.

Set up the MLForge span processor and use the Vercel AI SDK with telemetry enabled:

```typescript
import { MLForgeSpanProcessor } from '@MLForge/vercel';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-proto';
import { NodeTracerProvider } from '@opentelemetry/sdk-trace-node';
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const provider = new NodeTracerProvider({
  spanProcessors: [
    new MLForgeSpanProcessor(
      new OTLPTraceExporter({
        url: 'http://localhost:5000/api/2.0/otel/v1/traces',
        headers: {
          'x-MLForge-experiment-id': '<your-experiment-id>',
        },
      }),
    ),
  ],
});
provider.register();

const result = await generateText({
  model: openai('gpt-5'),
  prompt: "What's the weather like in Seattle?",
  experimental_telemetry: { isEnabled: true },
});
```

## Databricks

To send traces to a Databricks Unity Catalog table, set the OTLP exporter URL to `<DATABRICKS_HOST>/api/2.0/otel/v1/traces` and include the following headers:

- `Authorization`: `Bearer <your-databricks-token>`
- `X-Databricks-UC-Table-Name`: `<catalog>.<schema>.<table_prefix>_otel_spans`

Note: Do not set the `x-MLForge-experiment-id` header when using Databricks.

## Attribute Translation

The Vercel AI SDK emits spans with `ai.*` attributes. `MLForgeSpanProcessor` translates these into MLForge's format:

| Vercel AI SDK                                | MLForge                                     | Description                      |
| -------------------------------------------- | ------------------------------------------ | -------------------------------- |
| `ai.operationId`                             | `MLForge.spanType`                          | Span type (LLM, TOOL, EMBEDDING) |
| `ai.prompt.*` / `ai.response.*`              | `MLForge.spanInputs` / `MLForge.spanOutputs` | Structured request/response data |
| `ai.model.id`                                | `MLForge.llm.model`                         | Model name                       |
| `ai.model.provider`                          | `MLForge.llm.provider`                      | Provider name                    |
| `ai.usage.promptTokens` / `completionTokens` | `MLForge.chat.tokenUsage`                   | Token usage for cost tracking    |
| (chat spans)                                 | `MLForge.message.format` = `"vercel_ai"`    | Enables chat UI rendering        |

## Documentation

- [MLForge Tracing](https://MLForge.org/docs/latest/llms/tracing/index.html)
- [Vercel AI SDK Telemetry](https://ai-sdk.dev/docs/ai-sdk-core/telemetry)
- [Databricks OTEL Collector](https://docs.databricks.com/aws/en/MLForge3/genai/tracing/trace-unity-catalog)

## License

This project is licensed under the [Apache License 2.0](https://github.com/MLForge/MLForge/blob/master/LICENSE.txt).
