---
url: https://docs.evidentlyai.com/docs/library/data_definition
source: Evidently Documentation
---

To run evaluations, you must create a `Dataset` object with a `DataDefinition`, which maps:

* **Column types** (e.g., categorical, numerical, text).
* **Column roles** (e.g., id, prediction, target).

This allows Evidently to process the data correctly. Some evaluations need specific columns and will fail if they’re missing. You can define the mapping using the Python API or by assigning columns visually when uploading data to the Evidently platform.

## [​](#basic-flow) Basic flow

**Step 1. Imports.** Import the following modules:

Copy

```python
from evidently import Dataset
from evidently import DataDefinition
```

**Step 2. Prepare your data.** Use a pandas.DataFrame.

Your data can have [flexible structure](/docs/library/overview#dataset) with any mix of categorical, numerical or text columns. Check the [Reference table](/metrics/all_metrics) for data requirements in specific evaluations.

**Step 3. Create a Dataset object**. Use `Dataset.from_pandas` with `data_definition`:

Copy

```python
eval_data = Dataset.from_pandas(
    source_df,
    data_definition=DataDefinition()
)
```

To map columns automatically, pass an empty `DataDefinition()` . Evidently will map columns:

* By type (numerical, categorical).
* By matching column names to roles (e.g., a column “target” treated as target).

Automation works in many cases, but manual mapping is more accurate. It is also necessary for evaluating prediction quality or handling text columns.

**How to set the data definition manually?** See the section below for available options.

**Step 4. Run evals.** Once the **Dataset** object is ready, you can [add Descriptors](/docs/library/descriptors)  and [run Reports](/docs/library/report).

### [​](#special-cases) Special cases

**Working directly with pandas.DataFrame**. You can sometimes pass a `pandas.DataFrame` directly to `report.run()` without creating the Dataset object. This works for checks like numerical/categorical data summaries or drift detection. However, it’s best to always create a `Dataset` object explicitly for clarity and control.
**Working with two datasets**. If you’re working with current and reference datasets (e.g., for drift detection), create a Dataset object for each. Both must have identical data definition.

## [​](#data-definition) Data definition

This page shows all the different mapping options. Note that you **only need to use the relevant ones** that apply for your evaluation scenario. For example, you don’t need columns like target/prediction to run data quality or LLM checks.

### [​](#column-types) Column types

Knowing the column type helps compute correct statistics, visualizations, and pick default tests.

#### [​](#text-data) Text data

If you run LLM evaluations, simply specify the columns with inputs/outputs as text.

Copy

```python
definition = DataDefinition(
    text_columns=["Latest_Review"]
    )
    
eval_data = Dataset.from_pandas(
    source_df,
    data_definition=definition
)
```

**It’s optional but useful**. You can [generate text descriptors](/docs/library/descriptors) without explicit mapping. But it’s a good idea to map text columns since you may later run other evals which vary by column type.

#### [​](#tabular-data) Tabular data

Map numerical, categorical or datetime columns:

Copy

```python
definition = DataDefinition(
    text_columns=["Latest_Review"],
    numerical_columns=["Age", "Salary"],
    categorical_columns=["Department"],
    datetime_columns=["Joining_Date"]
    )
    
eval_data = Dataset.from_pandas(
    source_df,
    data_definition=definition
)
```

Explicit mapping helps avoid mistakes like misclassifying numerical columns with few unique values as categorical.

If you **exclude** certain columns in mapping, they’ll be ignored in all evaluations.

#### [​](#default-column-types) Default column types

If you do not pass explicit mapping, the following defaults apply:

| **Column Type** | **Description** | **Automated Mapping** |
| --- | --- | --- |
| `numerical_columns` | * Columns with numeric values. | All columns with numeric types (`np.number`). |
| `datetime_columns` | * Columns with datetime values. * Ignored in data drift calculations. | All columns with DateTime format (`np.datetime64`). |
| `categorical_columns` | * Columns with categorical values. | All non-numeric/non-datetime columns. |
| `text_columns` | * Text columns. * Mapping required for text data drift detection. | No automated mapping. |

### [​](#id-and-timestamp) ID and timestamp

If you have a timestamp or ID column, it’s useful to identify them.

Copy

```python
definition = DataDefinition(
    id_column="Id",
    timestamp="Date"
    )
```

| **Column role** | **Description** | **Automated mapping** |
| --- | --- | --- |
| `id_column` | * Identifier column. * Ignored in data drift calculations. | Column named “id” |
| `timestamp` | * Timestamp column. * Ignored in data drift calculations. | Column named “timestamp” |

How is`timestamp` different from `datetime_columns`?

* **DateTime** is a column type. You can have many DateTime columns in the dataset. For example, conversation start / end time or features like “date of last contact.”
* **Timestamp** is a role. You can have a single timestamp column. It often represents the time when a data input was recorded. Use it if you want to see it as index on the plots.

### [​](#llm-evals) LLM evals

When you generate [text descriptors](/docs/library/descriptors) and add them to the dataset, they are automatically mapped as `descriptors` in Data Definition. This means they will be included in the `TextEvals` [preset](/metrics/preset_text_evals) or treated as descriptors when you plot them on the dashboard.
However, if you computed some scores or metadata externally and want to treat them as descriptors, you can map them explicitly:

Copy

```python
definition = DataDefinition(
    numerical_descriptors=["chat_length", "user_rating"],
    categorical_descriptors=["upvotes", "model_type"]
    )
```

### [​](#regression) Regression

To run regression quality checks, you must map the columns with:

* Target: actual values.
* Prediction: predicted values.

You can have several regression results in the dataset, for example in case of multiple regression. (Pass the mappings in a list).
Example mapping:

Copy

```python
definition = DataDefinition(
    regression=[Regression(target="y_true", prediction="y_pred")]
    )
```

Defaults:

Copy

```python
    target: str = "target"
    prediction: str = "prediction"
```

### [​](#classification) Classification

To run classification checks, you must map the columns with:

* Target: true label.
* Prediction: predicted labels/probabilities.

There two different mapping options, for binary and multi-class classification. You can also have several classification results in the dataset. (Pass the mappings in a list).

#### [​](#multiclass) Multiclass

Example mapping:

Copy

```python
from evidently import MulticlassClassification

data_def = DataDefinition(
    classification=[MulticlassClassification(
        target="target",
        prediction_labels="prediction",
        prediction_probas=["0", "1", "2"],  # If probabilistic classification
        labels={"0": "class_0", "1": "class_1", "2": "class_2"}  # Optional, for display only
    )]
)
```

Available options and defaults:

Copy

```python
    target: str = "target"
    prediction_labels: str = "prediction"
    prediction_probas: Optional[List[str]] = None #if probabilistic classification
    labels: Optional[Dict[Label, str]] = None
```

When you have multiclass classification with predicted probabilities in separate columns, the column names in `prediction_probas` must exactly match the class labels. For example, if your classes are 0, 1, and 2, your probability columns must be named: “0”, “1”, “2”. Values in `target` and `prediction` columns should be strings.

#### [​](#binary) Binary

Example mapping:

Copy

```python
from evidently import BinaryClassification

definition = DataDefinition(
    classification=[BinaryClassification(
        target="target",
        prediction_labels="prediction")],
    categorical_columns=["target", "prediction"])
```

Available options and defaults:

Copy

```python
    target: str = "target"
    prediction_labels: Optional[str] = None
    prediction_probas: Optional[str] = "prediction" #if probabilistic classification
    pos_label: Label = 1 #name of the positive label
    labels: Optional[Dict[Label, str]] = None
```

### [​](#ranking) Ranking

#### [​](#recsys) RecSys

To evaluate recommender systems performance, you must map the columns with:

* Prediction: this could be predicted score or rank.
* Target: relevance labels (e.g., this could be an interaction result like user click or upvote, or a true relevance label)

The **target** column can contain either:

* a binary label (where `1` is a positive outcome)
* any scores (positive values, where a higher value corresponds to a better match or a more valuable user action).

Here are the examples of the expected data inputs.
If the system prediction is a **score** (expected by default):

| user\_id | item\_id | prediction (score) | target (relevance) |
| --- | --- | --- | --- |
| user\_1 | item\_1 | 1.95 | 0 |
| user\_1 | item\_2 | 0.8 | 1 |
| user\_1 | item\_3 | 0.05 | 0 |

If the model prediction is a **rank**:

| user\_id | item\_id | prediction (rank) | target (relevance) |
| --- | --- | --- | --- |
| user\_1 | item\_1 | 1 | 0 |
| user\_1 | item\_2 | 2 | 1 |
| user\_1 | item\_3 | 3 | 0 |

Example mapping:

Copy

```python
definition = DataDefinition(
    ranking=[Recsys()]
    )
```

Available options and defaults:

Copy

```python
    user_id: str = "user_id" #columns with user IDs
    item_id: str = "item_id" #columns with ranked items
    target: str = "target"
    prediction: str = "prediction"
```