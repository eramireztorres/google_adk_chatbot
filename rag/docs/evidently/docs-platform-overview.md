---
url: https://docs.evidentlyai.com/docs/platform/overview
source: Evidently Documentation
---

Evidently Platform helps you manage AI quality across the AI system lifecycle, from pre-deployment testing to production monitoring. It supports evaluations of open-ended LLM outputs, predictive tasks like classification, and complex workflows like AI agents.
![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/dashboard_llm_tabs.gif)

## [​](#key-features) Key features

Evidently Platform has a lightweight open-source version for evaluation tracking and monitoring, and a Cloud/Enterprise version with extra features. [Check feature availability.](/faq/oss_vs_cloud)

* Evaluations
* Datasets
* Synthetic data
* Regression testing
* Monitoring
* Tracing

Run evaluations locally with the Evidently Python library or no-code on the platform. Use 100+ built-in evals and templates. Track, compare, and debug experiments.
![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/evals_explore_view-min.png)

While many workflows can be run no-code directly on the platform, you’ll often need programmatic access – for example, to upload datasets or run local experimental evaluations. In these cases, you can use the Evidently Python library to interact with the Evidently Cloud API.
To collect input-outputs from your production AI systems, you’d also need to install Tracely, a lightweight tool based on OpenTelemetry.