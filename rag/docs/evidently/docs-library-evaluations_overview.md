---
url: https://docs.evidentlyai.com/docs/library/evaluations_overview
source: Evidently Documentation
---

This page shows the core eval workflow with the Evidently library and links to guides.

## [​](#define-and-run-the-eval) Define and run the eval

To log the evaluation results to the Evidently Platform, first connect to [Evidently Cloud](/docs/setup/cloud) or your [local workspace](/docs/setup/self-hosting) and [create a Project](/docs/platform/projects_manage). It’s optional: you can also run evals locally.

1

Prepare the input data

Get your data in a table like a `pandas.DataFrame`. More on [data requirements](/docs/library/overview#dataset). You can also [load data](/docs/platform/datasets_workflow) from Evidently Platform, like tracing or synthetic datasets.

2

Create a Dataset object

Create a Dataset object with `DataDefinition()` that specifies column role and types. You can also use default type detection. [How to set Data Definition](/docs/library/data_definition).

Copy

```python
eval_data = Dataset.from_pandas(
    source_df,
    data_definition=DataDefinition()
)
```

3

(Optional) Add descriptors

For text evals, choose and compute row-level `descriptors`. Optionally, add row-level tests to get pass/fail for specific inputs. [How to use Descriptors](/docs/library/descriptors).

Copy

```python
eval_data.add_descriptors(descriptors=[
    TextLength("Question", alias="Length"),
    Sentiment("Answer", alias="Sentiment")
])
```

4

Configure Report

For dataset-level evals (classification, data drift) or to summarize descriptors, create a `Report` with chosen `metrics` or `presets`. How to [configure Reports](/docs/library/report).

Copy

```python
report = Report([
    DataSummaryPreset()
])
```

5

(Optional) Add Test conditions

Add dataset-level Pass/Fail conditions, like to check if all texts are in < 100 symbols length. How to [configure Tests](/docs/library/tests).

Copy

```python
report = Report([
    DataSummaryPreset(),
    MaxValue(column="Length", tests=[lt(100)]),
])
```

6

(Optional) Add Tags and Timestamps

Add `tags` or `metadata` to identify specific evaluation runs or datasets, or override the default `timestamp` . [How to add metadata](/docs/library/tags_metadata).

7

Run the Report

To execute the eval, `run`the Report on the `Dataset` (or two).

Copy

```python
my_eval = report.run(eval_data, None)
```

8

Explore the results

* To upload to the Evidently Platform. [How to upload results](/docs/platform/evals_api).

Copy

```python
ws.add_run(project.id, my_eval, include_data=True)
```

* To view locally. [All output formats](/docs/library/output_formats).

Copy

```python
my_eval
##my_eval.json()
```

## [​](#quickstarts) Quickstarts

Check for end-to-end examples:

[## LLM quickstart

Evaluate the quality of text outputs.](/quickstart_llm)[## ML quickstart

Test tabular data quality and data drift.](/quickstart_ml)