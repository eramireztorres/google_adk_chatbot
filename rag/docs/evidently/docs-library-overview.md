---
url: https://docs.evidentlyai.com/docs/library/overview
source: Evidently Documentation
---

The Evidently Python library is an open-source tool designed to evaluate, test and monitor the quality of AI systems, from experimentation to production. You can use the evaluation library on its own, or as part of the [Monitoring Platform](/docs/platform/overview) (self-hosted or Evidently Cloud).
This page provides a conceptual overview of the Evidently library.

# [​](#at-a-glance) At a glance

Evidently library covers 4 core workflows. You can these features together or standalone.
**1. AI/ML Evaluations**

**TL;DR**: Lots of useful AI/ML/data metrics out of the box. Exportable as scores or visual reports.

Evidently’s core capability is running evaluations on AI system inputs and outputs. It includes 100+ built-in metrics and checks, and also useful configurable templates for custom evaluations.
You can get raw either metrics or pass/fail test results.
We support metrics that make sense both for predictive ML tasks and generative LLM system outputs. Example built-in checks:

| **Type** | **Example checks** |
| --- | --- |
| **🔡 Text qualities** | Length, sentiment, special symbols, pattern matches, etc. |
| **📝 LLM output quality** | Semantic similarity, relevance, RAG faithfulness, custom LLM judges, etc. |
| **🛢 Data quality** | Missing values, duplicates, min-max ranges, correlations, etc. |
| **📊 Data drift** | 20+ tests and distance metrics to detect distribution drift. |
| **🎯 Classification** | Accuracy, precision, recall, ROC AUC, confusion matrix, bias, etc. |
| **📈 Regression** | MAE, ME, RMSE, error distribution, error normality, error bias, etc. |
| **🗂 Ranking (inc. RAG)** | NDCG, MAP, MRR, Hit Rate, etc. |

You can get evaluation results in multiple formats:

* **Export scores** as JSON or Python dictionary.
* **As a DataFrame**, either as a raw metrics table or by attaching scores to existing data rows.
* **Generate visual reports** in Jupyter, Colab, or export as HTML
* **Upload to Evidently Platform** to track evaluations over time

This exportability makes it easy to integrate Evidently into your existing workflows and pipelines – even if you are not using the Evidently Platform.
Here is an example visual report showing various data quality metrics and test results. Other evaluations can be presented in the same way, or exported as raw scores:
![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/concepts/report_test_preview.gif)
**📌 Links:**

* Quickstart for [LLM evaluation](/quickstart_llm)
* Quickstart for [ML evaluation](/quickstart_ml)

Or read on through this page for conceptual introduction.
**2. Synthetic data generation [NEW]**

**TL;DR**: We have a nice config for structured synthetic data generation using LLMs.

Primarily designed for LLM use cases, Evidently also helps you generate synthetic test datasets - such as RAG-style question-answer pairs from a knowledge base or synthetic inputs to cold-start your AI app testing.
**📌 Links:**

* [Synthetic data](docs/library/synthetic_data_api)

**3. Prompt optimization [NEW]**

**TL;DR**: We help write prompts using labeled or annotated data as a target.

Evidently also includes tools for automated prompt writing. This features uses built-in evaluation capabilities to score prompt variations, optimizing them based on a target dataset and/or free-form user feedback.
This feature also help automatically generate LLM judge prompts to streamline the creation of custom evaluations.
**📌 Links:**

* [Prompt optimization](docs/library/prompt_optimization)

4. **Tracking and Visualization UI**

**TL;DR**: There is also a minimal UI to store and track evaluation results.

The Evidently library also includes a lightweight self-hostable UI for storing, comparing, and visualizing evaluation results over time.
While visual reports provide a snapshot of an evaluation for a specific period, dataset, or prompt version, the UI allows you to store multiple evaluations and track changes over time.
![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/concepts/evidently_oss_ui-min.png)
**📌 Links:**

* See live demo: [https://demo.evidentlyai.com](https://demo.evidentlyai.com/).
* [Self-hosting guide](/docs/setup/self-hosting)

The open-source UI is different from the Evidently Cloud / Enterprise platform version which has muliple additional features. Explore the [Evidently Platform capabailities](/docs/platform/overview).

# [​](#core-evaluation-concepts) Core evaluation concepts

Let’s take a look at the end-to-end evaluation process. It can be adapted to different metrics or data types, following the same worklows.

## [​](#dataset) Dataset

To run an evaluation, you first need to prepare the data. For example, generate and trace outputs from your ML or LLM system.

1. **Prepare your data as a pandas DataFrame**. The table can include any combination of numerical, categorical, text, metadata (including timestamps or IDs), and embedding columns.

Here are a few examples of data inputs Evidently can handle:

* LLM logs
* Data table
* Classification
* Regression
* Ranking
* Embeddings

**LLM logs**. Pass any text columns with inputs/outputs, context or ground truth.

| Question | Context | Answer |
| --- | --- | --- |
| How old is the universe? | The universe is believed to have originated from the Big Bang that occurred 13.8 billion years ago. | 13.8 billion years old. |
| What’s the lifespan of Baobab trees? | Baobab trees can live up to 2,500 years. They are often called the “Tree of Life”. | Up to 2,500 years. |
| What is the speed of light? | The speed of light in a vacuum is approximately 299,792 kilometers per second (186,282 miles per second). | Close to 299,792 km per second. |

These are examples: you data can have other structure.

2. **Create a Dataset object**. Once you have the data, you must create an Evidently `Dataset` object. This allows attaching extra meta-information so that your data is processed correctly.

This is needed because some evaluations may require specific columns or data types present. For example, to evaluate classification quality, you need both predictions and actual labels. To specify where they are located in your table, you can map the data schema using [Data Definition](/docs/library/data_definition).

3. **[Optional] Preparing two datasets**. Typically you evaluate a single (`current` ) dataset. Optionally, you can prepare a second (`reference`) dataset that will be used during the evaluation. Both must have identical structures.

![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/datasets_input_data_two.png)
When to use two datasets:

* **Side-by-side comparison**. This lets you compare outputs or data quality across two periods, prompt/model versions, etc. in a single Report.
* **Data drift detection. (Required)**. You can detect distribution shifts by comparing datasets, such as this week’s data to the previous one.
* **Simplify test setup**. You can automatically generate test conditions (e.g., min-max ranges) from the reference dataset without manual configuration.

**Data sampling**. For large datasets (millions of rows), evals can take some time. The depends on:

* the specific evaluation: some are more computationally intensive than others
* your dataset: e.g., if you run column-level evals and have lots of columns
* your infrastructure: data is processed in-memory.

If the computation takes too long, it’s often more efficient to use samples. For example, in data drift detection, you can apply random or stratified sampling.

Once your `Dataset` is ready, you can run evaluations. You can either:

* Add `descriptors` to your dataset, and then compute a summary Report.
* Compute a Report directly over raw data.

## [​](#descriptors) Descriptors

To evaluate text data and LLM outputs, you need `Descriptors`.
A **Descriptor** is a *row-level* score or label that assesses a specific quality of a given text. It’s different from metrics (like accuracy or precision) that give a score for an entire *dataset*. You can use descriptors to assess LLM outputs in summarization, Q&A, chatbots, agents, RAGs, etc.
Descriptors range from deterministic to complex ML- or LLM-based checks.
A simple example of a descriptor is `TextLength`. A more complex example is a customizable `LLMEval` descriptor: where you prompt an LLM to act as a judge and, for example, label responses as “relevant” or “not relevant”.
Descriptors can also use two texts at once, like checking `SemanticSimilarity` between two columns to compare new response to the reference one.
You can use [built-in descriptors](/metrics/all_descriptors), configure templates (like LLM judges or regular expressions) or add custom checks in Python. Each Descriptor returns a result that can be:

* **Numerical**. Any scores like symbol count or sentiment score.
* **Categorical**. Labels or binary “true”/“false” results for pattern matches.
* **Text string**. Like explanations generated by LLM.

Evidently adds the computed descriptor values directly to the dataset.
![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/concepts/overview_descriptors_export.png)
This helps with debugging: for example, you can sort to find the negative responses. You can view the results as a Pandas DataFrame or on the Evidently Platform.
**Descriptor tests**. Additionally, you can add a pass/fail condition on top of computed descriptors. For example, consider output a “pass” only when both conditions are true: it has expected length and is labeled “correct” by the LLM judge.
After you get the row-level Descriptors, you can also compute Metrics and Tests on the dataset level – using Reports.

## [​](#reports) Reports

A **Report** lets you structure and run evals on the dataset or column-level.
You can generate Reports after you get the descriptors, or for any existing dataset like a table with ML model logs. Use Reports to:

* summarize the computed text descriptors across all inputs
* analyze any tabular dataset (descriptive stats, quality, drift)
* evaluate AI system performance (regression, classification, ranking, etc.)

Each Report runs a computation and visualizes a set of **Metrics** and conditional **Tests.** If you pass two datasets, you get a side-by-side comparison. 
The easiest way to start is by using **Presets**.

### [​](#metric-presets) Metric Presets

Presets are pre-configured evaluation templates.
They help compute multiple related Metrics using a single line of code. Evidently has a number of **comprehensive Presets** ([see all](/metrics/all_presets)) for specific evaluation scenarios: from exploratory data analysis to AI quality assessments. For example:

* TextEvals
* Data Drift
* Data Summary
* Classification

`TextEvals` summarizes the scores from all text descriptors.![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/examples/llm_quickstart_report.png)

### [​](#metrics) Metrics

Each Preset is made of individual Metrics. You can also create your own **custom Report** by listing the `Metrics` you want to include.

* You can combine multiple Metrics and Presets in a Report.
* You can include both built-in Metrics and custom Metrics.

Built-in Metrics range from simple statistics like `MeanValue` or `MissingValueCount` to complex algorithmic evals like `DriftedColumnsCount`.
Each **Metric** computes a single value and has an optional visual representation (or several to choose from). For convenience, there are also **small Presets** that combine a handful of scores in a single widget, like `ValueStats` that shows many relevant descriptive value statistics at once.
![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/concepts/overview_small_preset_cat_value_compare_example.png)
Similarly `DatasetStats` give quick overview of all dataset-level stats, `ClassificationQuality` computes multiple metrics like Precision, Recall, Accuracy, ROC AUC, etc.

Explore all [**Built-in Metrics**](/metrics/all_metrics).

## [​](#test-suites) Test Suites

Reports are great for analysis and debugging, or logging metrics during monitoring. However, in many cases, you don’t want to review all the scores but run a **conditional check** to confirm that nothing is off. In this case, **Tests** are a great option.

### [​](#tests) Tests

**Tests** let you validate your results against specific expectations. You create a Test by adding a **condition** parameter to a Metric. Each Test will calculate a given value, check it against the rule, and report a pass/fail result.

* You can run multiple Tests in one go.
* You can create Tests on the dataset or column level.
* You can formulate custom conditions or use defaults.

A **Test Suite** is a collection of individual Tests. It works as an extension to a Report. Once you configure Tests, your Report will get an **additional tab** that shows a summary of outcomes.;
You can navigate the results by test outcome.
![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/concepts/overview_test_suite_example-min.png)
Each Test results in one of the following statuses:

* **Pass:** The condition was met.
* **Fail:** The condition wasn’t met.
* **Warning:** The condition wasn’t met, but the check is marked as non-critical.
* **Error:** Something went wrong with the Test itself, such as an execution error.

You can view extra details to debug. For example, if you run a Test to check that less than 5% of LLM responses fall outside the approved length, you can see the corresponding distribution:
![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/concepts/overview_descriptor_test_example-min.png)

### [​](#test-conditions) Test Conditions

Evidently has a powerful API to [set up Test conditions](/docs/library/tests).

* **Manual setup.** You can add thresholds to Metrics one by one, using simple syntax like **`greater than (gt)`** or **`less than (lt)`**. By picking different Metrics to test against, you can formulate fine-grained conditions like “less than 10% of texts can fall outside 10–100 character length.”
* **Manual setup with reference.** If you have a reference dataset (like a previous data batch), you can set conditions **relative** to it. For example, you can check if the min-max value range stays within ±5% of the reference range without setting exact thresholds.
* **Automatic setup.** You can run any Test using built-in defaults. These are either:
  + **Heuristics**. For example, the Test on missing values assumes none should be preset.
  + **Heuristics relative to reference.** Here, conditions adjust to a reference. For instance, the Test on missing values assumes their share should stay within ±10% of the reference.

### [​](#test-presets) Test Presets

For even faster setup, there are **Test Presets**. Each Metric Preset has a corresponding Test Preset that you can enable as an add-on. When you do this:

* Evidently adds a predefined set of Tests to your Report.
* These Tests use default conditions, either static or inferred from the reference dataset.

For example: 

* **Data Summary**. The Metric Preset gives an overview and stats for all columns. The Test Suite checks for quality issues like missing values, duplicates, etc. across all values.
* **Classification.** The Metric Preset shows quality metrics like precision or recall. The Test Suite verifies these metrics against a baseline, like a dummy baseline calculated by Evidently or previous model performance.

## [​](#building-your-workflow) Building your workflow

You can use Evidently Reports and Test Suites on their own or as part of a monitoring system. 

### [​](#independent-use) Independent use

Reports are great for exploratory evals:

* **Ad hoc evals.** Run one-time analyses on your data, models or LLM outputs.
* **Experiments.** Compare models, prompts, or datasets side by side.
* **Debugging.** Investigate data or model issues.

Test Suites are great for automated checks like:

* **Data validation.** Test inputs and outputs in prediction pipelines.
* **CI/CD and regression testing.** Check AI system performance after updates.
* **Safety testing**. Run structured behavioral tests like adversarial testing.

For automation, you can integrate Evidently with tools like Airflow. You can trigger actions based on Test results, such as sending alerts or halting a pipeline.

### [​](#as-part-of-platform) As part of platform

You can use **Reports** together with the **Evidently Platform** in production workflows:

* **Reports** serve as a metric computation layer, running evaluations on your data.
* The **Platform** lets you store, compare, track and alert on evaluation results.

Reports are stored as JSON files, which can be natively parsed to visualize metrics on a Dashboard.
![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/evals_flow_python.png)
This setup works for both experiments and production monitoring. For example:

* **Experiments.** Log evaluations while experimenting with prompts or model versions. Use the Platform to compare runs and track progress.
* **Regression Tests.** Use Test Suites to validate updates on your golden dataset. Debug failures and maintain a history of results on the Platform.
* **Batch Monitoring.** Integrate Reports into your data pipelines to compute Metrics for data batches. Use the Platform for performance tracking and alerting.

**Evidently Cloud** also offers managed evaluations to generate Reports directly on the platform, and other features such as synthetic data and test generation.
**Platform deployment options.** You can choose:

* Self-host the open-source platform version.
* Sign up for [Evidently Cloud](https://www.evidentlyai.com/register) (Recommended).

The Evidently Platform has additional features beyond evaluation: from synthetic data to tracing.
[Read more on the platform](/docs/platform/overview).