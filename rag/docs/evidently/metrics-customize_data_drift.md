---
url: https://docs.evidentlyai.com/metrics/customize_data_drift
source: Evidently Documentation
---

All Metrics and Presets that evaluate shift in data distributions use the default [Data Drift algorithm](/metrics/explainer_drift). It automatically selects the drift detection method based on the column type (text, categorical, numerical) and volume.
You can override the defaults by passing a custom parameter to the chosen Metric or Preset. You can modify the drift detection method (choose from 20+ available), thresholds, or both. 
You can also implement fully custom drift detection methods.
**Pre-requisites**:

* You know how to use [Data Definition](/docs/library/data_definition) to map column types.
* You know how to create [Reports](/docs/library/report) and run [Tests](/docs/library/tests).

## [​](#data-drift-parameters) Data drift parameters

Setting conditions for data drift works differently from the usual Test API (with `gt`, `lt`, etc.) This accounts for nuances like varying role of thresholds across drift detection methods, where “greater” can be better or worse depending on the method.

### [​](#dataset-level) Dataset-level

**Dataset drift share**. You can set the share of drifting columns that signals **dataset drift** (default: 0.5) in the relevant Metrics or Presets. For example, to set it at 70%:

Copy

```python
report = Report([
    DataDriftPreset(drift_share=0.7)
]
```

This will detect dataset drift if over 70% columns are drifting, using defaults for each column.
**Drift methods**. You can also specify the drift detection methods used on the column level. For example, to use PSI (Population Stability Index) for all columns in the dataset:

Copy

```python
report = Report([
    DataDriftPreset(drift_share=0.7, method="psi")
]
```

This will check if over 70% columns are drifting, using PSI method with default thresholds.

See all available methods in the table below.

**Drift thresholds**. You can set thresholds for each method. For example, use PSI with a threshold of 0.3 for categorical columns.

Copy

```python
report = Report([
    DataDriftPreset(cat_method="psi", cat_threshold="0.3")
]
```

In this case, if PSI is ≥ 0.3 for any categorical column, drift will be detected for that column. The rest of the checks will use defaults: default methods for numerical and text columns (if present), and 50% as the `drift_share` threshold.

### [​](#column-level) Column-level

For column-level metrics, you can set the drift method/threshold directly for each column:

Copy

```python
report = Report([
    ValueDrift(column="Salary", method="psi"),
]
```

### [​](#all-parameters) All parameters

Use the following parameters to pass chosen drift methods. See methods and their defaults below.

| Parameter | Description | Applies To |
| --- | --- | --- |
| `method` | Defines the drift detection method for a given column (if one column is tested), or all columns in the dataset (if multiple columns are tested and the method can apply to all columns). | `ValueDrift()`, `DriftedColumnsCount()`, `DataDriftPreset()` |
| `threshold` | Sets the drift threshold in a given column or all columns.  The threshold meaning varies based on the drift detection method, e.g., it can be the value of a distance metric or a p-value of a statistical test. | `ValueDrift()`, `DriftedColumnsCount()`, `DataDriftPreset()` |
| `drift_share` | Defines the share of drifting columns as a condition for Dataset Drift. Default: 0.5 | `DriftedColumnsCount()`, `DataDriftPreset()` |
| `cat_method`  `cat_threshold` | Sets the drift method and/or threshold for all categorical columns. | `DriftedColumnsCount()`, `DataDriftPreset()` |
| `num_method`  `num_threshold` | Sets the drift method and/or threshold for all numerical columns. | `DriftedColumnsCount()`, `DataDriftPreset()` |
| `per_column_method` `per_column_threshold` | Sets the drift method and/or threshold for the listed columns (accepts a dictionary). | `DriftedColumnsCount()`, `DataDriftPreset()` |
| `text_method`   `text_threshold` | Defines the drift detection method and threshold for all text columns. | `DriftedColumnsCount()`, `DataDriftPreset()` |

## [​](#data-drift-detection-methods) Data drift detection methods

### [​](#tabular-data) Tabular data

The following methods apply to **tabular** data: numerical or categorical columns in data definition. Pass them using the `stattest` (or `num_stattest`, etc.) parameter.

| StatTest | Applicable to | Drift score |
| --- | --- | --- |
| `ks` Kolmogorov–Smirnov (K-S) test | tabular data only numerical   **Default method for numerical data, if ≤ 1000 objects** | returns `p_value` drift detected when `p_value < threshold` default threshold: 0.05 |
| `chisquare` Chi-Square test | tabular data only categorical  **Default method for categorical with > 2 labels, if ≤ 1000 objects** | returns `p_value` drift detected when `p_value < threshold` default threshold: 0.05 |
| `z`  Z-test | tabular data only categorical  **Default method for binary data, if ≤ 1000 objects** | returns `p_value` drift detected when `p_value < threshold` default threshold: 0.05 |
| `wasserstein`  Wasserstein distance (normed) | tabular data only numerical  **Default method for numerical data, if > 1000 objects** | returns `distance` drift detected when `distance` ≥ `threshold` default threshold: 0.1 |
| `kl_div` Kullback-Leibler divergence | tabular data numerical and categorical | returns `divergence` drift detected when `divergence` ≥ `threshold` default threshold: 0.1 |
| `psi`  Population Stability Index (PSI) | tabular data numerical and categorical | returns `psi_value` drift detected when `psi_value` ≥ `threshold` default threshold: 0.1 |
| `jensenshannon`  Jensen-Shannon distance | tabular data numerical and categorical  **Default method for categorical, if > 1000 objects** | returns `distance` drift detected when `distance` ≥ `threshold` default threshold: 0.1 |
| `anderson`  Anderson-Darling test | tabular data only numerical | returns `p_value` drift detected when `p_value < threshold` default threshold: 0.05 |
| `fisher_exact`  Fisher’s Exact test | tabular data only categorical | returns `p_value` drift detected when `p_value < threshold` default threshold: 0.05 |
| `cramer_von_mises`  Cramer-Von-Mises test | tabular data only numerical | returns `p_value` drift detected when `p_value < threshold` default threshold: 0.05 |
| `g-test`  G-test | tabular data only categorical | returns `p_value` drift detected when `p_value < threshold` default threshold: 0.05 |
| `hellinger`  Hellinger Distance (normed) | tabular data numerical and categorical | returns `distance` drift detected when `distance` >= `threshold` default threshold: 0.1 |
| `mannw`  Mann-Whitney U-rank test | tabular data only numerical | returns `p_value` drift detected when `p_value < threshold` default threshold: 0.05 |
| `ed`  Energy distance | tabular data only numerical | returns `distance` drift detected when `distance >= threshold` default threshold: 0.1 |
| `es`  Epps-Singleton test | tabular data only numerical | returns `p_value` drift detected when `p_value < threshold` default threshold: 0.05 |
| `t_test`  T-Test | tabular data only numerical | returns `p_value` drift detected when `p_value < threshold` default threshold: 0.05 |
| `empirical_mmd`  Empirical-MMD | tabular data only numerical | returns `p_value` drift detected when `p_value < threshold` default threshold: 0.05 |
| `TVD`  Total-Variation-Distance | tabular data only categorical | returns `p_value` drift detected when `p_value` < `threshold` default threshold: 0.05 |

### [​](#text-data) Text data

Text drift detection applies to columns with **raw text data**, as specified in data definition. Pass them using the `stattest` (or `text_stattest`) parameter.

| StatTest | Description | Drift score |
| --- | --- | --- |
| `perc_text_content_drift`  Text content drift (domain classifier, with statistical hypothesis testing) | Applies only to text data. Trains a classifier model to distinguish between text in “current” and “reference” datasets.  **Default for text data ≤ 1000 objects.** | * returns `roc_auc` of the classifier as a `drift_score` * drift detected when `roc_auc` > possible ROC AUC of the random classifier at a set percentile * `threshold` sets the percentile of the possible ROC AUC values of the random classifier to compare against * default threshold: 0.95 (95th percentile) * `roc_auc` values can be 0 to 1 (typically 0.5 to 1); a higher value means more confident drift detection |
| `abs_text_content_drift`  Text content drift (domain classifier) | Applies only to text data. Trains a classifier model to distinguish between text in “current” and “reference” datasets.  **Default for text data when > 1000 objects.** | * returns `roc_auc` of the classifier as a `drift_score` * drift detected when `roc_auc` > `threshold` * `threshold` sets the ROC AUC threshold * default threshold: 0.55 * `roc_auc` values can be 0 to 1 (typically 0.5 to 1); a higher value means more confident drift detection |

**Text descriptors drift**. If you work with raw text data, you can also check for distribution drift in text descriptors (such as text length, etc.) To use this method, first compute the selected [text descriptors](/docs/library/descriptors). Then, use numerical / categorical drift detection methods as usual.

## [​](#add-a-custom-method) Add a custom method

If you do not find a suitable drift detection method, you can implement a custom function:

Copy

```python
import pandas as pd
from scipy.stats import anderson_ksamp

from evidently import Dataset
from evidently import DataDefinition
from evidently import Report
from evidently import ColumnType
from evidently.metrics import ValueDrift
from evidently.metrics import DriftedColumnsCount
from evidently.legacy.calculations.stattests import register_stattest
from evidently.legacy.calculations.stattests import StatTest

#toy data 
data = pd.DataFrame(data={
    "column_1": [1, 2, 3, 4, -1, 5],
    "target": [1, 1, 0, 0, 1, 1],
    "prediction": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
})

definition = DataDefinition(
    numerical_columns=["column_1", "target", "prediction"],
    )
dataset = Dataset.from_pandas(
    data,
    data_definition=definition,
)

#implement method
def _addd(
    reference_data: pd.Series,
    current_data: pd.Series,
    feature_type: ColumnType,
    threshold: float,
):
    p_value = anderson_ksamp([reference_data.values, current_data.values])[2]
    return p_value, p_value < threshold


adt = StatTest(
    name="adt",
    display_name="Anderson-Darling",
    allowed_feature_types=[ColumnType.Numerical],
    default_threshold=0.1,
)

register_stattest(adt, default_impl=_addd)


report = Report([
    # ValueDrift(column="column_1"),
    ValueDrift(column="column_1", method="adt"),
    DriftedColumnsCount(),
])

snapshot = report.run(dataset, dataset)
snapshot
```

We recommended writing a specific instance of the **StatTest class** for that function. You need:

| Parameter | Type | Description |
| --- | --- | --- |
| `name` | `str` | A short name used to reference the Stat Test from the options (registered globally). |
| `display_name` | `str` | A long name displayed in the Report. |
| `func` | `Callable` | The StatTest function. |
| `allowed_feature_types` | `List[str]` | The list of allowed feature types for this function (`cat`, `num`). |

The **StatTest function** itself should match `(reference_data: pd.Series, current_data: pd.Series, threshold: float) -> Tuple[float, bool]` signature.
Accepts:

* `reference_data: pd.Series` - The reference data series.
* `current_data: pd.Series` - The current data series to compare.
* `feature_type: str` - The type of feature being analyzed.
* `threshold: float` - The test threshold for drift detection.

Returns:

* `score: float` - Stat Test score (actual value)
* `drift_detected: bool` - indicates is drift detected with given threshold