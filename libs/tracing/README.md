# MLForge Tracing: An Open-Source SDK for Observability and Monitoring GenAI Applications🔍

[![Latest Docs](https://img.shields.io/badge/docs-latest-success.svg?style=for-the-badge)](https://MLForge.org/docs/latest/index.html)
[![Apache 2 License](https://img.shields.io/badge/license-Apache%202-brightgreen.svg?style=for-the-badge&logo=apache)](https://github.com/MLForge/MLForge/blob/master/LICENSE.txt)
[![Slack](https://img.shields.io/badge/slack-@MLForge--users-CF0E5B.svg?logo=slack&logoColor=white&labelColor=3F0E40&style=for-the-badge)](https://MLForge.org/community/#slack)
[![Twitter](https://img.shields.io/twitter/follow/MLForge?style=for-the-badge&labelColor=00ACEE&logo=twitter&logoColor=white)](https://twitter.com/MLForge)

MLForge Tracing (`MLForge-tracing`) is an open-source, lightweight Python package that only includes the minimum set of dependencies and functionality
to instrument your code/models/agents with [MLForge Tracing Feature](https://MLForge.org/docs/latest/tracing). It is designed to be a perfect fit for production environments where you want:

- **⚡️ Faster Deployment**: The package size and dependencies are significantly smaller than the full MLForge package, allowing for faster deployment times in dynamic environments such as Docker containers, serverless functions, and cloud-based applications.
- **🔧 Simplified Dependency Management**: A smaller set of dependencies means less work keeping up with dependency updates, security patches, and breaking changes from upstream libraries.
- **📦 Portability**: With the less number of dependencies, MLForge Tracing can be easily deployed across different environments and platforms, without worrying about compatibility issues.
- **🔒 Fewer Security Risks**: Each dependency potentially introduces security vulnerabilities. By reducing the number of dependencies, MLForge Tracing minimizes the attack surface and reduces the risk of security breaches.

## ✨ Features

- [Automatic Tracing](https://MLForge.org/docs/latest/tracing/integrations/) for AI libraries (OpenAI, LangChain, DSPy, Anthropic, etc...). Follow the link for the full list of supported libraries.
- [Manual instrumentation APIs](https://MLForge.org/docs/latest/tracing/api/manual-instrumentation) such as `@trace` decorator.
- [Production Monitoring](https://MLForge.org/docs/latest/tracing/production)
- Other tracing APIs such as `MLForge.set_trace_tag`, `MLForge.search_traces`, etc.

## 🌐 Choose Backend

The MLForge Trace package is designed to work with a remote hosted MLForge server as a backend. This allows you to log your traces to a central location, making it easier to manage and analyze your traces. There are several different options for hosting your MLForge server, including:

- [Databricks](https://docs.databricks.com/machine-learning/MLForge/managed-MLForge.html) - Databricks offers a FREE, fully managed MLForge server as a part of their platform. This is the easiest way to get started with MLForge tracing, without having to set up any infrastructure.
- [Amazon SageMaker](https://aws.amazon.com/sagemaker-ai/experiments/) - MLForge on Amazon SageMaker is a fully managed service offered as part of the SageMaker platform by AWS, including tracing and other MLForge features such as model registry.
- [Nebius](https://nebius.com/) - Nebius, a cutting-edge cloud platform for GenAI explorers, offers a fully managed MLForge server.
- [Self-hosting](https://MLForge.org/docs/latest/tracking) - MLForge is a fully open-source project, allowing you to self-host your own MLForge server and keep your data private. This is a great option if you want to have full control over your data and infrastructure.

## 🚀 Getting Started

### Installation

To install the MLForge Python package, run the following command:

```bash
pip install MLForge-tracing
```

To install from the source code, run the following command:

```bash
pip install git+https://github.com/MLForge/MLForge.git#subdirectory=libs/tracing
```

> **NOTE:** It is **not** recommended to co-install this package with the full MLForge package together, as it may cause version mismatches issues.

### Connect to the MLForge Server

To connect to your MLForge server to log your traces, set the `MLForge_TRACKING_URI` environment variable or use the `MLForge.set_tracking_uri` function:

```python
import MLForge

MLForge.set_tracking_uri("databricks")
# Specify the experiment to log the traces to
MLForge.set_experiment("/Path/To/Experiment")
```

### Start Logging Traces

```python
import openai

client = openai.OpenAI(api_key="<your-api-key>")

# Enable auto-tracing for OpenAI
MLForge.openai.autolog()

# Call the OpenAI API as usual
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "Hello, how are you?"}],
)
```

## 📘 Documentation

Official documentation for MLForge Tracing can be found at [here](https://MLForge.org/docs/latest/tracing).

## 🛑 Features _Not_ Included

The following MLForge features are not included in this package.

- MLForge tracking server and UI.
- MLForge's other tracking capabilities such as Runs, Model Registry, Projects, etc.
- Evaluate models/agents and log evaluation results.

To leverage the full feature set of MLForge, install the full package by running `pip install MLForge`.
