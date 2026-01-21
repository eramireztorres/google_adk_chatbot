---
url: https://docs.evidentlyai.com/examples/introduction
source: Evidently Documentation
---

**We have an applied course on LLM evaluations!** Free video course with 10+ tutorials. [Sign up](https://www.evidentlyai.com/llm-evaluation-course-practice).

## [​](#quickstarts) Quickstarts

If you are new, start here.

[## LLM quickstart

Evaluate the quality of text outputs.](/quickstart_llm)[## ML quickstart

Test tabular data quality and data drift.](/quickstart_ml)[## Tracing quickstart

Collect inputs and outputs from AI your app.](/quickstart_tracing)

## [​](#llm-tutorials) LLM Tutorials

End-to-end examples of specific workflows and use cases.

[## LLM as a judge

How to create and evaluate an LLM judge against human labels.](/examples/LLM_judge)[## RAG evaluation

A walkthrough of different RAG evaluation metrics.](/examples/LLM_rag_evals)[## LLM as a jury

Using multiple LLMs to evaluate the same output.](LLM_jury)[## LLM evaluation methods

A walkthrough of different LLM evaluation methods. [CODE + VIDEO]](LLM_evals)[## Descriptor cookbook

A walkthrough of different descriptors (deterministic, ML, etc.) a single notebook.](https://github.com/evidentlyai/evidently/blob/main/examples/cookbook/descriptors.ipynb)[## LLM judge prompt optimization (1)

Optimize a multi-class classifier using target labels.](https://github.com/evidentlyai/evidently/blob/main/examples/cookbook/prompt_optimization_bookings_example.ipynb)[## LLM judge prompt optimization (2)

Optimize a binary classifier using target labels and free-form feedback.](https://github.com/evidentlyai/evidently/blob/main/examples/cookbook/prompt_optimization_code_review_example.ipynb)

## [​](#ml-tutorials) ML tutorials

End-to-end examples of specific workflows and use cases.

[## Metric cookbook

Various data/ML metrics: Regression, Classification, Data Quality, Data Drift.](https://github.com/evidentlyai/evidently/blob/main/examples/cookbook/metrics.ipynb)

## [​](#integrations) Integrations

End-to-end examples of integrating Evidently with other tools and platforms.

[## GitHub actions

Running Evidently evals as part of CI/CD workflow. Native GitHub action integration for regression testing.](/examples/GitHub_actions)[## Different LLM providers as judges

Examples of using different external evaluator LLMs as LLM judges: OpenAI, Gemini, Google Vertex, Mistral, Ollama.](https://github.com/evidentlyai/evidently/blob/main/examples/future_examples/llm_providers.ipynb)[## Evidently + Grafana: LLM evals

Visualize Evidently LLM evaluation metrics with Grafana. (Postgres as a database).](https://github.com/evidentlyai/evidently/tree/main/examples/llm_eval_grafana_dashboard)[## Evidently+ Grafana: Data drift

Visualize Evidently data drift evaluations on a Grafana dashboard. (Postgres as a database).](https://github.com/evidentlyai/evidently/tree/main/examples/data_drift_grafana_dashboard)

## [​](#deployment) Deployment

[## Evidently Open-source UI tutorial

How to create a workspace, project and run Reports.](https://github.com/evidentlyai/evidently/blob/main/examples/service/workspace_tutorial.ipynb)

## [​](#llm-evaluation-course-video-tutorials) LLM Evaluation Course - Video Tutorials

We have an applied LLM evaluation course where we walk through the core evaluation workflows. Each consists of the code example and a video tutorial walthrough.
📥 [Sign up for the course](https://www.evidentlyai.com/llm-evaluation-course-practice)
📹 [See complete Youtube playlist](https://www.youtube.com/watch?v=K8LLVi5Xrh8&list=PL9omX6impEuNTr0KGLChHwhvN-q3ZF12d&index=2)

| **Tutorial** | **Description** | **Code example** | **Video** |
| --- | --- | --- | --- |
| **Intro to LLM Evals** | Introduction to LLM evaluation: concepts, goals, and motivations behind evaluating LLM outputs. | – | * Video |
| **LLM Evaluation Methods** | Tutorial with an overview of methods.  * Part 1. Anatomy of a single evaluation. Covers basic LLM evaluation API and setup. * Part 2. Reference-based evaluation: exact match, semantic similarity, BERTScore, and LLM judge. * Part 3. Reference-free evaluation: text statistics, regex, ML models, LLM judges, and session-level evaluators. | [Open Notebook](https://github.com/evidentlyai/community-examples/blob/main/learn/LLMCourse_Tutorial_1_Intro_to_LLM_evals_methods.ipynb) | * Video 1 * Video 2 * Video 3 |
| **LLM as a Judge** | Tutorial on creating and tuning LLM judges aligned with human preferences. | [Open Notebook](LLMCourse_Tutorial_2_LLM_as_a_judge.ipynb) | * Video |
| **Clasification Evaluation** | Tutorial on evaluating LLMs and a simple predictive ML baseline on a multi-class classification task. | [Open Notebook](https://github.com/evidentlyai/community-examples/blob/main/learn/LLMCourse_Classification_Evals.ipynb) | * Video |
| **Content Generation with LLMs** | Tutorial on how to use LLMs to write tweets and evaluate how engaging they are. Introduction to the concept of tracing. | [Open Notebook](https://github.com/evidentlyai/community-examples/blob/main/learn/LLMCourse_Content_Generation_Evals.ipynb) | * Video |
| **RAG evaluations** | * Part 1. Theory on how to evaluate RAG systems: retrieval, generation quality and synthetic data. * Part 2. Tutorial on building a toy RAG application and evaluating correctness and faithfulness. | [Open Notebook](https://github.com/evidentlyai/community-examples/blob/main/learn/LLMCourse_RAG_Evals.ipynb) | * Video 1 * Video 2 |
| **AI agent evaluations** | Tutorial on how to build a simple Q&A agent and evaluate tool choice and answer correctness. | [Open Notebook](https://github.com/evidentlyai/community-examples/blob/main/learn/LLMCourse_Agent_Evals.ipynb) | * Video |
| **Adversarial testing** | Tutorial on how to run scenario-based risk testing on forbidden topics and brand risks. | [Open Notebook](https://github.com/evidentlyai/community-examples/blob/main/learn/LLMCourse_Adversarial_Testing.ipynb) | * Video |

## [​](#more-examples) More examples

You can also find more examples in the [Example Repository](https://github.com/evidentlyai/community-examples).