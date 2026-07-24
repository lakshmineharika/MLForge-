<h1 align="center" style="border-bottom: none">
    <br>
    <strong>⚡ MLForge</strong>
    <br>
</h1>
<h3 align="center">The Open-Source AI Engineering Platform for Agents, LLMs & Machine Learning Models</h3>

<p align="center">
  <b>MLForge</b> is an end-to-end MLOps platform for managing experiment tracking, LLM observability, prompt optimization, model evaluation, and deployment.
</p>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE.txt)
[![Author](https://img.shields.io/badge/Author-Lakshmi_Neharika_Anchula-orange.svg)](https://github.com/lakshmineharika)

</div>

<br>

---

## 👩‍💻 Author & Project Maintainer

| Field | Details |
| :--- | :--- |
| **Name** | **Lakshmi Neharika Anchula** |
| **Role** | Data Scientist \| AI ML Engineer |
| **Primary Email** | [lakshmianchula10@gmail.com](mailto:lakshmianchula10@gmail.com) |
| **Git Push Email** | [lakshmineharika2000@gmail.com](mailto:lakshmineharika2000@gmail.com) |
| **Phone** | +1 (848) 372-9051 |
| **LinkedIn** | [linkedin.com/in/neharika1020](https://linkedin.com/in/neharika1020) |
| **GitHub** | [@lakshmineharika](https://github.com/lakshmineharika) |

---

## 📌 Executive Summary

**MLForge** provides a unified lifecycle management system for machine learning models and Generative AI applications. Designed for data scientists and ML engineers, it simplifies experimental tracking, automates LLM evaluation, manages prompt versions, and facilitates seamless model deployment into production environments.

---

## 🌟 Key Features

* 🔍 **LLM Observability & Agent Tracing:** Built on OpenTelemetry standards to capture full execution traces, latency, costs, and token usage for AI agents and LLM calls.
* 📊 **Experiment Tracking:** Automatically log parameters, performance metrics, dataset versions, and artifacts for reproducible ML workflows.
* 🏷️ **Prompt Management & Evaluation:** Version, test, and optimize prompts with 50+ built-in evaluation metrics and LLM judges.
* 📦 **Model Registry & Governance:** Centralized model catalog for managing versions, approval stages, and lifecycle transitions.
* 🚀 **Multi-Cloud Deployment:** Deploy trained models as REST microservices or containerized endpoints on Docker, Kubernetes, and cloud providers.

---

## 🚀 Quick Start in 3 Steps

### 1. Install MLForge
```bash
pip install mlforge
```

### 2. Start MLForge Server
```bash
mlforge server --port 5000
```

### 3. Track Experiments & LLM Calls
```python
import mlforge

# Connect to MLForge server
mlforge.set_tracking_uri("http://localhost:5000")
mlforge.openai.autolog()

from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Explain MLOps lifecycle in 2 sentences."}]
)

print("Logged trace & metrics to MLForge UI at http://localhost:5000")
```

---

## 🛠️ Technology Stack & Integrations

* **Core Language:** Python 3.10+, TypeScript, Rust
* **Observability:** OpenTelemetry, Custom Tracing Handlers
* **ML & Deep Learning:** PyTorch, TensorFlow, Scikit-Learn, XGBoost, LightGBM
* **GenAI & Agent Frameworks:** LangChain, LangGraph, LlamaIndex, OpenAI, Anthropic, Gemini, CrewAI
* **Storage & Serving:** SQLAlchemy, PostgreSQL, S3, Docker, Kubernetes

---

## 📄 License & Citation

This project is licensed under the [Apache 2.0 License](LICENSE.txt).

If you use MLForge in your research or portfolio projects, please cite it as:

```bibtex
@software{Anchula_MLForge_2026,
  author = {Anchula, Lakshmi Neharika},
  title = {{MLForge: Open Source AI Engineering Platform for Agents, LLMs & Models}},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/lakshmineharika/MLForge-}
}
```
