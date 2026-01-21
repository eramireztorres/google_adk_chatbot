---
url: https://docs.evidentlyai.com/docs/platform/datasets_overview
source: Evidently Documentation
---

Datasets are available in **Evidently OSS, Cloud** and **Evidently Enterprise**.

## [​](#what-is-a-dataset) What is a Dataset?

**Datasets** are collections of data from your application used for analysis and automated checks. You can bring in existing datasets, capture live data, or create synthetic datasets.
![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/dataset_llm.png)

## [​](#how-to-create-a-dataset) How to create a Dataset?

You can add Datasets to the platform in multiple ways:

* **Upload directly**. Use the UI (Evidently Cloud) to upload CSV files or push datasets via the Python API.
* **Upload with Reports**. Attach datasets to Reports when running local evaluations. This is optional — you can also upload only summary metrics.
* **Generate synthetic data**. Use built-in platform features to generate synthetic evaluation datasets. (Cloud only).
* **Create from Traces**. During tracing, Evidently automatically generates tabular datasets that can be used for evaluations. (Cloud only).

**Where do I find the data?** To view all datasets (uploaded, synthetic, or evaluation results), go to the “Dataset” page in your Project menu. For raw tracing datasets, check the Tracing section.

## [​](#synthetic-data) Synthetic Data

You can synthesize evaluation datasets directly in Evidently Cloud:

* **Generate from examples or description**. Describe specific test scenarios and generate matching datasets.
* **Generate from source documents**. Generate Q&A pairs from source documents like PDF, CSV or markdown files (great for RAG evaluations).

After creating or uploading datasets, you can edit or diversify them further using the “more like this” feature.

## [​](#when-do-you-need-datasets) When do you need Datasets?

Here are common use cases for datasets in Evidently:

* **Organize evaluation datasets**. Save curated datasets with expected inputs and optional ground truth outputs. You can bring in domain experts to collaborate on these datasets in UI, and access them programmatically for CI/CD checks.
* **Debug evaluation results**. After you run an evaluation, view the dataset to identify and debug specific failures. E.g. you can sort all text outputs by added scores.
* **Store ML inference logs or LLM traces**. Collect raw data from production or experimental runs, use it as a source of truth, and run evaluations over it.