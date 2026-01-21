---
url: https://docs.evidentlyai.com/docs/platform/datasets_workflow
source: Evidently Documentation
---

You must first connect to [Evidently Cloud](/docs/setup/cloud) or local workspace and [create a Project](/docs/platform/projects_manage).

## [​](#upload-a-dataset) Upload a Dataset

* Python
* UI

Prepare your dataset as an Evidently Dataset with the corresponding data definition. To upload a Dataset to the specified Project in workspace `ws`, use the `add_dataset` method:

Copy

```python
eval_data = Dataset.from_pandas(
    source_df,
    data_definition=DataDefinition()
)
ws.add_dataset(
    dataset = eval_data, 
    name = "dataset_name",
    project_id = project.id, 
    description = "Optional description")
```

You must always specify the dataset `name` that you will see in the UI. The description is optional.

**How to create an Evidently Dataset?** Read the [Data Definition docs](../library/data-definition).

## [​](#download-the-dataset) Download the Dataset

You can pull the Dataset stored or generated on the platform to your local environment. For example, call the evaluation or tracing dataset to use in a CI/CD testing script.
Use the `load_dataset` method:

Copy

```python
eval_dataset = ws.load_dataset(dataset_id = "YOUR_DATASET_ID") 

#to create as pandas dataframe
df = eval_dataset.as_dataframe()
```

## [​](#include-the-dataset) Include the Dataset

You can include Datasets when you upload Reports to the platform. This way, after running an evaluation locally you simultaneously upload:

* the Report with evaluation result,
* the Dataset it was generated for, with new added scores if applicable.

By default, you upload only the Report.
To include the Dataset, use the `include_data` parameter:

Copy

```python
ws.add_run(project.id, data_report, include_data=True)
```

Check the docs on [running evals via API](/docs/platform/evals_api) for details.