---
url: https://docs.evidentlyai.com/metrics/all_metrics
source: Evidently Documentation
---

For an intro, read [Core Concepts](/docs/library/overview) and check quickstarts for [LLMs](docs/quickstart_llm) or [ML](docs/quickstart_ml). For a reference code example, see this [Metric cookbook](https://github.com/evidentlyai/evidently/blob/main/examples/cookbook/metrics.ipynb).

How to read the tables

* **Metric**: the name of Metric or Preset you can pass to `Report`.
* **Description:** what it does. Complex Metrics link to explainer pages.
* **Parameters:** available options. You can also add conditional `tests` to any Metric with standard operators like `eq` (equal), `gt` (greater than), etc. [How Tests work](/docs/library/tests).
* **Test defaults** are conditions that apply when you invoke Tests but do not set a pass/fail condition yourself.
  + **With reference**: if you provide a reference dataset during the Report `run`, the conditions are set relative to reference.
  + **No reference**: if you do not provide a reference, Tests will use fixed heuristics (like expect no missing values).

## [​](#text-evals) Text Evals

Summarizes results of text or LLM evals. To score individual inputs, first use [descriptors](/metrics/all_descriptors).

[Data definition](/docs/library/data_definition). You may need to map text columns.

| Metric | Description | Parameters | Test Defaults |
| --- | --- | --- | --- |
| **TextEvals()** | * Large Preset. * Shows `ValueStats` for all descriptors. * You must specify descriptors ([see how](/docs/library/descriptors) and [all descriptors](/metrics/all_descriptors)). * Metric result: for all Metrics. * [Preset page](/metrics/preset_text_evals). | **Optional**:  * `columns` | As in Metrics included in `ValueStats` |

## [​](#columns) Columns

Use to aggregate descriptor results or check data quality on column level.

You may need to map column types using [Data definition](/docs/library/data_definition).

### [​](#value-stats) Value stats

Descriptive statistics.

| Metric | Description | Parameters | Test Defaults |
| --- | --- | --- | --- |
| **ValueStats()** | * Small Preset, column-level. * Computes various descriptive stats. Included Metrics: `UniqueValueCount`, `MissingValueCount`, `MinValue`, `MaxValue`, `MeanValue`, `StdValue`, `QuantileValue` (0.25, 0.5, 0.75). * Returns different stats based on the column type. | **Required**:  * `column`  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**. As in individual Metrics. * **With reference**. As in indiviudal Metrics. |
| **MinValue()** | * Column-level. * Returns min value for a given numerical column. * Metric result: `value`. | **Required**:  * `column`  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**. N/A. * **With reference**. Fails if Min Value is differs by more than 10% (+/-). |
| **StdValue()** | * Column-level. * Computes the standard deviation of a given numerical column. * Metric result: `value`. | **Required**:  * `column`  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**. N/A. * **With reference**. Fails if the standard deviation differs by more than 10% (+/-). |
| **MeanValue()** | * Column-level. * Computes the mean value of a given numerical column. * Metric result: `value`. | **Required**:  * `column`  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**. N/A. * **With reference**. Fails if the mean value differs by more than 10%. |
| **MaxValue()** | * Column-level. * Computes the max value of a given numerical column. * Metric result: `value`. | **Required**:  * `column`  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**. N/A. * **With reference**. Fails if the max value is higher than in the reference. |
| **MedianValue()** | * Column-level. * Computes the median value of a given numerical column. * Metric result: `value`. | **Required**:  * `column`  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**. N/A. * **With reference**. Fails if the median value differs by more than 10% (+/-). |
| **QuantileValue()** | * Column-level. * Computes the quantile value of a given numerical column. * Defaults to 0.5 if no quantile is specified. * Metric result: `value`. | **Required**:  * `column`  **Optional**:  * `quantile` (default: 0.5) * [Test conditions](/docs/library/tests) | * **No reference**. N/A. * **With reference**. Fails if quantile value differs by more than 10% (+/-). |
| **CategoryCount()**    Example:   `CategoryCount(` `column="city",`  `category="NY")` | * Column-level. * Counts occurrences of the specified category or categories. * To check the joint share of several categories, pass the list `categories=["a", "b"]`. * Metric result: `count`, `share`. | **Required**:  * `column` * `category` * `categories`  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**. N/A. * **With reference**. Fails if the specified category is not present. |

### [​](#column-data-quality) Column data quality

Column-level data quality metrics.

[Data definition](/docs/library/data_definition). You may need to map column types.

| Metric | Description | Parameters | Test Defaults |
| --- | --- | --- | --- |
| **MissingValueCount()** | * Column-level. * Counts the number and share of missing values. * Metric result: `count`, `share`. | **Required**:  * `column`  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: Fails if there are missing values. * **With reference**: Fails if share of missing values is >10% higher. |
| **InRangeValueCount()**    Example:   `InRangeValueCount(` `column="age",` `left="1", right="18")` | * Column-level. * Counts the number and share of values in the set range. * Metric result: `count`, `share`. | **Required**:  * `column` * `left` * `right`  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: N/A. * **With reference**: Fails if column contains values out of the min-max reference range. |
| **OutRangeValueCount()** | * Column-level. * Counts the number and share of values out of the set range. * Metric result: `count`, `share`. | **Required**:  * `column` * `left` * `right`  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: N/A. * **With reference**: Fails if any value is out of min-max reference range. |
| **InListValueCount()** | * Column-level. * Counts the number and share of values in the set list. * Metric result: `count`, `share`. | **Required**:  * `column` * `values`  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: N/A. * **With reference**: Fails if any value is out of list. |
| **OutListValueCount()**    Example:   `OutListValueCount(` `column="city",`  `values=["Lon", "NY"])` | * Column-level. * Counts the number and share of values out of the set list. * Metric result: `count`, `share`. | **Required**:  * `column` * `values`  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: N/A. * **With reference**: Fails if any value is out of list. |
| **UniqueValueCount()** | * Column-level. * Counts the number and share of unique values. * Metric result: `values` (dict with `count, share`). | **Required**:  * `column`  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: N/A. * **With reference**: Fails if the share of unique values differs by >10% (+/-). |

## [​](#dataset) Dataset

Use for exploratory data analysis and data quality checks.

[Data definition](/docs/library/data_definition). You may need to map column types, ID and timestamp.

### [​](#dataset-stats) Dataset stats

Descriptive statistics.

| Metric | Description | Parameters | Test Defaults |
| --- | --- | --- | --- |
| **DataSummaryPreset()** | * Large Preset. * Combines `DatasetStats` and `ValueStats` for all or specified columns. * Metric result: for all Metrics. * [Preset page](/metrics/preset_data_summary) | **Optional**:  * `columns` | As in individual Metrics. |
| **DatasetStats()** | * Small preset. * Dataset-level. * Calculates descriptive dataset stats, including columns by type, rows, missing values, empty columns, etc. * Metric result: for all Metrics. | None | * **No reference**: As in included Metrics * **With reference**: As in included Metrics. |
| **RowCount()** | * Dataset-level. * Counts the number of rows. * Metric result: `value`. | **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: N/A. * **With reference**: Fails if row count differs by >10%. |
| **ColumnCount()** | * Dataset-level. * Counts the number of columns. * Metric result: `value`. | **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: N/A. * **With reference**: Fails if not equal to reference. |

### [​](#dataset-data-quality) Dataset data quality

Dataset-level data quality metrics.

[Data definition](/docs/library/data_definition). You may need to map column types, ID and timestamp.

| Metric | Description | Parameters | Test Defaults |
| --- | --- | --- | --- |
| **ConstantColumnsCount()** | * Dataset-level. * Counts the number of constant columns. * Metric result: `value`. | **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: Fails if there is at least one constant column. * **With reference**: Fails if count is higher than in reference. |
| **EmptyRowsCount()** | * Dataset-level. * Counts the number of empty rows. * Metric result: `value`. | **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: Fails if there is at least one empty row. * **With reference**: Fails if share differs by >10%. |
| **EmptyColumnsCount()** | * Dataset-level. * Counts the number of empty columns. * Metric result: `value`. | **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: Fails if there is at least one empty column. * **With reference**: Fails if count is higher than in reference. |
| **DuplicatedRowCount()** | * Dataset-level. * Counts the number of duplicated rows. * Metric result: `value`. | **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: Fails if there is at least one duplicated row. * **With reference**: Fails if share differs by >10% (+/-). |
| **DuplicatedColumnsCount()** | * Dataset-level. * Counts the number of duplicated columns. * Metric result: `value`. | **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: Fails if there is at least one duplicated column. * **With reference**: Fails if count is higher than in reference. |
| **DatasetMissingValueCount()** | * Dataset-level. * Calculates the number and share of missing values. * Displays the number of missing values per column. * Metric result: `share`, `count`. | **Required**:  * `columns`  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: Fails if there are missing values. * **With reference**: Fails if share is >10% higher than reference (+/-). |
| **AlmostConstantColumnsCount()** | * Dataset-level. * Counts almost constant columns (95% identical values). * Metric result: `value`. | **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: Fails if there is at least one almost constant column. * **With reference**: Fails if count is higher than in reference. |
| **ColumnsWithMissingValuesCount()** | * Dataset-level. * Counts columns with missing values. * Metric result: `value`. | **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: Fails if there is at least one column with missing values. * **With reference**: Fails if count is higher than in reference. |

## [​](#data-drift) Data Drift

Use to detect distribution drift for text and tabular data or over computed text descriptors. Checks 20+ drift methods listed separately: [text and tabular](/metrics/customize_data_drift).

[Data definition](/docs/library/data_definition). You may need to map column types, ID and timestamp.

[Metrics explainers](/metrics/explainer_drift). Understand how data drift works.

| Metric | Description | Parameters | Test Defaults |
| --- | --- | --- | --- |
| **DataDriftPreset()** | * Large Preset. * Requires reference. * Calculates data drift for all or set columns. * Uses the default or set method. * Returns drift score for each column. * Visualizes all distributions. * Metric result: all Metrics. * [Preset page](/metrics/customize_data_drift). | **Optional**:  * `columns` * `method` * `cat_method` * `num_method` * `per_column_method` * `threshold` * `cat_threshold` * `num_threshold` * `per_column_threshold`  See [drift options](/metrics/customize_data_drift). | * **With reference**: Data drift defaults, depending on column type. See [drift methods](/metrics/customize_data_drift). |
| **DriftedColumnsCount()** | * Dataset-level. * Requires reference. * Calculates the number and share of drifted columns in the dataset. * Each column is tested for drift using the default algorithm or set method. * Returns only the total number of drifted columns. * Metric result: `count`, `share`. | **Optional**:  * `columns` * `method` * `cat_method` * `num_method` * `per_column_method` * `threshold` * `cat_threshold` * `num_threshold` * `per_column_threshold`  See [drift options](/metrics/customize_data_drift). | * **With reference**: Fails if 50% of columns are drifted. |
| **ValueDrift()** | * Column-level. * Requires reference. * Calculates data drift for a defined column (num, cat, text). * Visualizes distributions. * Metric result: `value`. | **Required**:  * `column`  **Optional:**  * `method` * `threshold`  See [drift options](/metrics/customize_data_drift). | * **With reference**: Data drift defaults, depending on column type. See [drift methods](/metrics/customize_data_drift). |

## [​](#classification) Classification

Use to evaluate quality on a classification task (probabilistic, non-probabilistic, binary and multi-class).

[Data definition](/docs/library/data_definition). You may need to map prediction, target columns and classification type.

### [​](#general) General

Use for binary classification and aggregated results for multi-class.

| Metric | Description | Parameters | Test Defaults |
| --- | --- | --- | --- |
| **ClassificationPreset()** | * Large Preset with many classification Metrics and visuals. * See [Preset page](/metrics/preset_classification). * Metric result: all Metrics. | Optional: `probas_threshold` . | As in individual Metrics. |
| **ClassificationQuality()** | * Small Preset. * Summarizes quality Metrics in a single widget. * Metric result: all Metrics. | Optional: `probas_threshold` | As in individual Metrics. |
| **Accuracy()** | * Calculates accuracy. * Metric result: `value`. | **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: Fails if lower than dummy model accuracy. * **With reference**: Fails if accuracy differs by >20%. |
| **Precision()** | * Calculates precision. * Visualizations available: Confusion Matrix, PR Curve, PR Table. * Metric result: `value`. | **Required**:  * Set at least one visualization: `conf_matrix`, `pr_curve`, `pr_table`.  **Optional**:  * `probas_threshold` (default: None or 0.5 for probabilistic classification) * `top_k` * [Test conditions](/docs/library/tests) | * **No reference**: Fails if Precision is lower than the dummy model. * **With reference**: Fails if Precision differs by >20%. |
| **Recall()** | * Calculates recall. * Visualizations available: Confusion Matrix, PR Curve, PR Table. * Metric result: `value`. | **Required**:  * Set at least one visualization: `conf_matrix`, `pr_curve`, `pr_table`.  **Optional**:  * `probas_threshold` * `top_k` * [Test conditions](/docs/library/tests) | * **No reference**: Fails if lower than dummy model recall. * **With reference**: Fails if Recall differs by >20%. |
| **F1Score()** | * Calculates F1 Score. * Metric result: `value`. | **Required**:  * Set at least one visualization: `conf_matrix`.  **Optional**:  * `probas_threshold` * `top_k` * [Test conditions](/docs/library/tests) | * **No reference**: Fails if lower than dummy model F1. * **With reference**: Fails if F1 differs by >20%. |
| **TPR()** | * Calculates True Positive Rate (TPR). * Metric result: `value`. | **Required**:  * Set at least one visualization: `pr_table`.  **Optional**:  * `probas_threshold` * `top_k` * [Test conditions](/docs/library/tests) | * **No reference**: Fails if TPR is lower than the dummy model. * **With reference**: Fails if TPR differs by >20%. |
| **TNR()** | * Calculates True Negative Rate (TNR). * Metric result: `value`. | **Required**:  * Set at least one visualization: `pr_table`.  **Optional**:  * `probas_threshold` * `top_k` * [Test conditions](/docs/library/tests) | * **No reference**: Fails if TNR is lower than the dummy model. * **With reference**: Fails if TNR differs by >20%. |
| **FPR()** | * Calculates False Positive Rate (FPR). * Metric result: `value`. | **Required**:  * Set at least one visualization: `pr_table`.  **Optional**:  * `probas_threshold` * `top_k` * [Test conditions](/docs/library/tests) | * **No reference**: Fails if FPR is higher than the dummy model. * **With reference**: Fails if FPR differs by >20%. |
| **FNR()** | * Calculates False Negative Rate (FNR). * Metric result: `value`. | **Required**:  * Set at least one visualization: `pr_table`.  **Optional**:  * `probas_threshold` * `top_k` * [Test conditions](/docs/library/tests) | * **No reference**: Fails if FNR is higher than the dummy model. * **With reference**: Fails if FNR differs by >20%. |
| **LogLoss()** | * Calculates Log Loss. * Metric result: `value`. | **Required**:  * Set at least one visualization: `pr_table`.  **Optional**:  * `top_k` * [Test conditions](/docs/library/tests) | * **No reference**: Fails if LogLoss is higher than the dummy model (equals 0.5 for a constant model). * **With reference**: Fails if LogLoss differs by >20%. |
| **RocAUC()** | * Calculates ROC AUC. * Can visualize PR curve or table. * Metric result: `value`. | **Required**:  * Set at least one visualization: `pr_table`, `roc_curve`.  **Optional**:  * `top_k` * [Test conditions](/docs/library/tests) | * **No reference**: Fails if ROC AUC is ≤ 0.5. * **With reference**: Fails if ROC AUC differs by >20%. |

Dummy metrics:


Dummy model quality

Use these Metics to get the quality of a dummy model created on the same data (based on heuristics). You can compare your model quality to verify that it’s better than random. These Metrics serve as a baseline in automated testing.

| Metric | Description | Parameters | Test Defaults |
| --- | --- | --- | --- |
| **ClassificationDummyQuality()** | * Small Preset summarizing quality of a dummy model. * Metric result: all Metrics | N/A | N/A |
| **DummyPrecision()** | * Calculates precision for a dummy model. * Metric result: `value`. | N/A | N/A |
| **DummyRecall()** | * Calculates recall for a dummy model. * Metric result: `value`. | N/A | N/A |
| **DummyF1()** | * Calculates F1 Score for a dummy model. * Metric result: `value`. | N/A | N/A |

### [​](#by-label) By label

Use when you have multiple classes and want to evaluate quality separately.

| Metric | Description | Parameters | Test Defaults |  |
| --- | --- | --- | --- | --- |
| **ClassificationQualityByLabel()** | * Small Preset summarizing classification quality Metrics by label. * Metric result: all Metrics. | None | As in individual Metrics. |  |
| **PrecisionByLabel()** | * Calculates precision by label in multiclass classification. * Metric result (dict): `label: value`. | **Optional**:  * `probas_threshold` * `top_k` * [Test conditions](/docs/library/tests) | * **No reference**: Fails if Precision is lower than the dummy model. * **With reference**: Fails if Precision differs by >20%. |  |
| **F1ByLabel()** | * Calculates F1 Score by label in multiclass classification. * Metric result (dict): `label: value`. | **Optional**:  * `probas_threshold` * `top_k` * [Test conditions](/docs/library/tests) | * **No reference**: Fails if F1 is lower than the dummy model. * **With reference**: Fails if F1 differs by >20%. |  |
| **RecallByLabel()** | * Calculates recall by label in multiclass classification. * Metric result (dict): `label: value` | **Optional**:  * `probas_threshold` * `top_k` * [Test conditions](/docs/library/tests) | * **No reference**: Fails if Recall is lower than the dummy model. * **With reference**: Fails if Recall differs by >20%. |  |
| **RocAUCByLabel()** | * Calculates ROC AUC by label in multiclass classification. * Metric result (dict): `label: value` | **Optional**:  * `probas_threshold` * `top_k` * [Test conditions](/docs/library/tests) | * **No reference**: Fails if ROC AUC is ≤ 0.5. * **With reference**: Fails if ROC AUC differs by >20%. |  |

## [​](#regression) Regression

Use to evaluate the quality of a regression model.

[Data definition](/docs/library/data_definition). You may need to map prediction and target columns.

| Metric | Description | Parameters | Test Defaults |
| --- | --- | --- | --- |
| **RegressionPreset** | * Large Preset. * Includes a wide range of regression metrics with rich visuals. * Metric result: all metrics. * See [Preset page](/metrics/preset_regression). | None. | As in individual metrics. |
| **RegressionQuality** | * Small Preset. * Summarizes key regression metrics in a single widget. * Metric result: all metrics. | None. | As in individual metrics. |
| **MeanError()** | * Calculates the mean error. * Visualizations available: Error Plot, Error Distribution, Error Normality. * Metric result: `mean`, `std`. | **Required**:  * Set at least one visualization: `error_plot`, `error_distr`, `error_normality`.  **Optional**:  * [Test conditions](/docs/library/tests). Use `mean_tests` and `std_tests`. | * **No reference/With reference**: Expect ME to be near zero. Fails if Mean Error is skewed and condition is violated: `eq = approx(absolute=0.1 * error_std)`. |
| **MAE()** | * Calculates Mean Absolute Error (MAE). * Visualizations available: Error Plot, Error Distribution, Error Normality. * Metric result: `mean`, `std`. | **Required**:  * Set at least one visualization: `error_plot`, `error_distr`, `error_normality`.  **Optional**:  * [Test conditions](/docs/library/tests). Use `mean_tests` and `std_tests`. | * **No reference**: Fails if MAE is higher than the dummy model predicting the median target value. * **With reference**: Fails if MAE differs by >10%. |
| **RMSE()** | * Calculates Root Mean Square Error (RMSE). * Metric result: `value`. | **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: Fails if RMSE is higher than the dummy model predicting the mean target value. * **With reference**: Fails if RMSE differs by >10%. |
| **MAPE()** | * Calculates Mean Absolute Percentage Error (MAPE). * Visualizations available: Percentage Error Plot. * Metric result: `mean`, `std`. | **Required**:  * Set at least one visualization: `perc_error_plot`.  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: Fails if MAPE is higher than the dummy model predicting the weighted median target value. * **With reference**: Fails if MAPE differs by >10%. |
| **R2Score()** | * Calculates R² (Coefficient of Determination). * Metric result: `value`. | **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: Fails if R² ≤ 0. * **With reference**: Fails if R² differs by >10%. |
| **AbsMaxError()** | * Calculates Absolute Maximum Error. * Metric result: `value`. | **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**: Fails if absolute maximum error is higher than the dummy model predicting the median target value. * **With reference**: Fails if it differs by >10%. |

Dummy metrics:


Dummy model quality

Use these Metics to get the baseline quality for regression: they use optimal constants (varies by the Metric). These Metrics serve as a baseline in automated testing.

| Metric | Description | Parameters | Test Defaults |
| --- | --- | --- | --- |
| **RegressionDummyQuality()** | * Small Preset summarizing quality of a dummy model. * Metric result: all Metrics | N/A | N/A |
| **DummyMeanError()** | * Calculates Mean Error for a dummy model. * Metric result: `mean_error`, `error std`. | N/A | N/A |
| **DummyMAE()** | * Calculates Mean Absolute Error (MAE) for a dummy model. * Metric result: `mean_absolute_error`, `absolute_error_std`. | N/A | N/A |
| **DummyMAPE()** | * Calculates Mean Absolute Percentage Error (MAPE) for a dummy model. * Metric result: `mean_perc_absolute_error`, `perc_absolute_error std`. | N/A | N/A |
| **DummyRMSE()** | * Calculates Root Mean Square Error (RMSE) for a dummy model. * Metric result: `rmse`. | N/A | N/A |
| **DummyR2()** | * Calculates Calculates R² (Coefficient of Determination) for a dummy model. * Metric result: `r2score`. | N/A | N/A |

## [​](#ranking) Ranking

Use to evaluate ranking, search / retrieval or recommendations.

[Data definition](/docs/library/data_definition). You may need to map prediction and target columns and ranking type.

[**Metric explainers**](/metrics/explainer_recsys)**.** Check ranking metrics explainers.

| Metric | Description | Parameters | Test Defaults |
| --- | --- | --- | --- |
| **RecallTopK()** | * Calculates Recall at the top K retrieved items. * Metric result: `value`. | **Required**:  * `k`  **Optional**:  * `no_feedback_users` * `min_rel_score` * [Test conditions](/docs/library/tests) | * **No reference**: Tests if recall > 0. * **With reference**: Fails if Recall differs by >10%. |
| **FBetaTopK()** | * Calculates F-beta score at the top K retrieved items. * Metric result: `value`. | **Required**:  * `k`  **Optional**:  * `no_feedback_users` * `min_rel_score` * [Test conditions](/docs/library/tests) | * **No reference**: Tests if F-beta > 0. * **With reference**: Fails if F-beta differs by >10%. |
| **PrecisionTopK()** | * Calculates Precision at the top K retrieved items. * Metric result: `value`. | **Required**:  * `k`  **Optional**:  * `no_feedback_users` * `min_rel_score` * [Test conditions](/docs/library/tests) | * **No reference**: Tests if Precision > 0. * **With reference**: Fails if Precision differs by >10%. |
| **MAP()** | * Calculates Mean Average Precision at the top K retrieved items. * Metric result: `value`. | **Required**:  * `k`  **Optional**:  * `no_feedback_users` * `min_rel_score` * [Test conditions](/docs/library/tests) | * **No reference**: Tests if MAP > 0. * **With reference**: Fails if MAP differs by >10%. |
| **NDCG()** | * Calculates Normalized Discounted Cumulative Gain at the top K retrieved items. * Metric result: `value`. | **Required**:  * `k`  **Optional**:  * `no_feedback_users` * `min_rel_score` * [Test conditions](/docs/library/tests) | * **No reference**: Tests if NDCG > 0. * **With reference**: Fails if NDCG differs by >10%. |
| **MRR()** | * Calculates Mean Reciprocal Rank at the top K retrieved items. * Metric result: `value`. | **Required**:  * `k`  **Optional**:  * `no_feedback_users` * `min_rel_score` * [Test conditions](/docs/library/tests) | * **No reference**: Tests if MRR > 0. * **With reference**: Fails if MRR differs by >10%. |
| **HitRate()** | * Calculates Hit Rate at the top K retrieved items. * Metric result: `value`. | **Required**:  * `k`  **Optional**:  * `no_feedback_users` * `min_rel_score` * [Test conditions](/docs/library/tests) | * **No reference**: Tests if Hit Rate > 0. * **With reference**: Fails if Hit Rate differs by >10%. |
| **ScoreDistribution()** | * Computes the predicted score entropy (KL divergence). * Applies only when the recommendations\_type is a score.. * Metric result: `value`. | **Required**:  * `k`  **Optional**:  * [Test conditions](/docs/library/tests) | * **No reference**:`value` * **With reference**: `value`. |