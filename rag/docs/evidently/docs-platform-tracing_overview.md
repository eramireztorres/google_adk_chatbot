---
url: https://docs.evidentlyai.com/docs/platform/tracing_overview
source: Evidently Documentation
---

Trace store and viewer are Pro features available in **Evidently Cloud** and **Evidently Enterprise**.

Tracing uses the open-source `Tracely` library, based on OpenTelemetry.

## [​](#what-is-llm-tracing) What is LLM tracing?

Tracing lets you instrument your AI application to collect data for evaluation and analysis.
It captures detailed records of how your LLM app operates, including inputs, outputs and any intermediate steps and events (e.g., function calls). You define what to include.
Evidently provides multiple ways to explore tracing data.

* Trace view
* Dataset view
* Dialogue view

See a timeline of execution steps with input-output details and latency.![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/tracing.png)

Once you capture the data, you can also run evals on the tracing datasets.

## [​](#do-i-always-need-tracing) Do I always need tracing?

Tracing is optional on the Evidently Platform. You can also:

* Upload tabular datasets using Dataset API.
* Run evals locally and send results to the platform without tracing.

However, tracing is especially useful for understanding complex LLM chains and execution flows, both in experiments and production monitoring.