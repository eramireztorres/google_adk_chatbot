---
url: https://docs.evidentlyai.com/docs/platform/dashboard_add_panels
source: Evidently Documentation
---

You can add Panels in the user interface or using Python API. This pages describes the Python API. Check how to [add panels in the UI](dashboard_add_panels_ui).

## [​](#dashboard-management) Dashboard Management

Dashboards as code are available in Evidently OSS, Cloud, Enterprise.

You must first connect to [Evidently Cloud](/docs/setup/cloud) and [create a Project](/docs/platform/projects_manage).

**Adding Tabs**. To add a new Tab:

Copy

```python
project.dashboard.add_tab("Another Tab")
```

You can also create a new Tab while adding a Panel as shown below. If the destination Tab doesn’t exist, it will be created. If it does, the Panel will be added below existing ones in that Tab.
**Deleting Tabs**. To delete a Tab:

Copy

```python
project.dashboard.delete_tab("Another Tab")
```

**Deleting Panels**. To delete a specific Panel:

Copy

```python
project.dashboard.delete_panel("Dashboard title", "My new tab")
```

(First list the Panel name, then the Tab name).
**[DANGER]. Delete Dashboard**. To delete all Tabs and Panels on the Dashboard:

Copy

```python
project.dashboard.clear_dashboard()
```

Note: This does **not** delete the underlying Reports or dataset; it only clears the Panels.

## [​](#adding-panels) Adding Panels

Imports:

Copy

```python
from evidently.sdk.models import PanelMetric
from evidently.sdk.panels import DashboardPanelPlot
```

You can add multiple Panels at once: they will appear in the listed order.

### [​](#text) Text

Text-only panels are perfect for titles.
**Add a text panel**. Add a new text panel to the specified Tab.

Copy

```python
project.dashboard.add_panel(
    DashboardPanelPlot(
        title="Dashboard title",
        size="full", 
        values=[], #leave empty
        plot_params={"plot_type": "text"},
    ),
    tab="My new tab", #will create a Tab if there is no Tab with this name
)
```

### [​](#counters) Counters

Counter panels show a value with optional supporting text.

![panel_counter_example-min](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/dashboard/panel_counter_example-min.png)

## Text counter

Shows the specified value(s) and optional text.

![panel_pie_chart](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/dashboard/panel_pie_chart.png)

## Pie chart

Shows the specified value(s) in a pie chart.

**Add Counters**. To add panels for the `RowCount` metric with different aggregations:

Copy

```python
# Sum
project.dashboard.add_panel(
    DashboardPanelPlot(
        title="Row count",
        subtitle="Total number of evaluations over time.",
        size="half",
        values=[PanelMetric(legend="Row count", metric="RowCount")],
        plot_params={"plot_type": "counter", "aggregation": "sum"},
    ),
    tab="My tab",
)

# Average
project.dashboard.add_panel(
    DashboardPanelPlot(
        title="Row count",
        subtitle="Average number of evaluations per Report.",
        size="half",
        values=[PanelMetric(legend="Row count", metric="RowCount")],
        plot_params={"plot_type": "counter", "aggregation": "avg"},
    ),
    tab="My tab",
)

# Last
project.dashboard.add_panel(
    DashboardPanelPlot(
        title="Row count",
        subtitle="Latest number of evaluations.",
        size="half",
        values=[PanelMetric(legend="Row count", metric="RowCount")],
        plot_params={"plot_type": "counter", "aggregation": "last"},
    ),
    tab="My tab",
)
```

**Add pie charts**. You can use the same aggregation params (`sum`, `last`, `avg`).

Copy

```python
project.dashboard.add_panel(
    DashboardPanelPlot(
        title="Row count",
        subtitle="Total number of evaluations over time.",
        size="half",
        values=[PanelMetric(legend="Row count", metric="RowCount")],
        plot_params={"plot_type": "pie", "aggregation": "sum"},
    ),
    tab="My tab",
)
```

### [​](#plots) Plots

These Panels display values as bar or line plots.

![panel_line_chart](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/dashboard/panel_line_chart.png)

## Line chart

Shows the selected values over time. You can add multiple series to the same chart as multiple lines.

![panel_dist_stacked_2-min](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/dashboard/panel_dist_stacked_2-min.png)

## Bar chart (stacked)

Shows selected values or distributions over time (if stored in each Report). Stacked in a single bar.

![panel_dist_group_2-min](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/dashboard/panel_dist_group_2-min.png)

## Bar chart (grouped)

Shows selected values or distributions over time (if stored in each Report). Multiple bars.

**Add Plots**. To add time series panels for the `RowCount` metric.

Copy

```python
# line chart
project.dashboard.add_panel(
             DashboardPanelPlot(
                title="Row count",
                subtitle = "Number of evaluations over time.",
                size="half",
                values=[
                    PanelMetric(
                        legend="Row count",
                        metric="RowCount",
                    ),
                ],
                plot_params={"plot_type": "line"},
            ),
            tab="My tab",
        )
        
# bar chart
project.dashboard.add_panel(
             DashboardPanelPlot(
                title="Row count",
                subtitle = "Number of evaluations over time.",
                size="half",
                values=[
                    PanelMetric(
                        legend="Row count",
                        metric="RowCount",
                    ),
                ],
                plot_params={"plot_type": "bar", "is_stacked": False}, #default False, set as True to get stacked bars
            ),
            tab="My tab",
        )
```

**Multiple values**. A single Panel can show multiple values. For example, this will add multiple lines on a Line chart:

Copy

```python
project.dashboard.add_panel(
    DashboardPanelPlot(
        title="Text Length",
        subtitle="Text length stats (symbols).",
        size="full",
        values=[
            PanelMetric(legend="max", metric="MaxValue", metric_labels={"column": "length"}),
            PanelMetric(legend="mean", metric="MeanValue", metric_labels={"column": "length"}),
            PanelMetric(legend="min", metric="MinValue", metric_labels={"column": "length"}),
        ]
    )
)
```

### [​](#dashboard-panel-options) Dashboard Panel options

A summary of all parameters:

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `title` | `str` | ❌ | `None` | Title of the panel. |
| `description` | `str` | ❌ | `None` | Optional panel description shown as a subtitle. |
| `size` | `str` | ❌ | `"full"` | Panel size: `"full"` (100% width) or `"half"` (50%). |
| `values` | `list` | ✅ | — | List of `PanelMetric` objects to display. |
| `tab` | `str` | ❌ | `None` | Dashboard tab name. If not set, defaults to the first tab or creates a new “General” tab. |
| `create_if_not_exists` | `bool` | ❌ | `True` | If `True`, creates the tab if it doesn’t exist. Throws exception if `False`. |
| `plot_params` | `dict` | ❌ | `{}` | Panel visualization settings like `"plot_type"`: `"text"`, `"line"`, `"counter"`. |

## [​](#configuring-panel-values) Configuring Panel values

### [​](#metric) Metric

To define which value the Panel displays, you must reference the name of the corresponding Evidently Metric. This metric must be present in the Reports logged to your Project. If the metric isn’t present, the Panel will appear empty.
**Dataset-level Metrics**: pass the Metric name directly to `PanelMetric`, e.g., `"RowCount"`.
Example:

Copy

```python
project.dashboard.add_panel(
             DashboardPanelPlot(
                title="Row count",
                subtitle = "Number of evaluations over time.",
                size="half",
                values=[
                    PanelMetric(
                        legend="Row count",
                        metric="RowCount", ## <- metric name
                    ),
                ],
                plot_params={"plot_type": "line"},
            ),
            tab="My tab",
        )
```

**Presets** (like `TextEvals`, `ClassificationPreset`, `DataDriftPreset`) contain multiple sub-metrics. When logging Reports using a Preset, you must reference the specific **metric** inside it, such as `Accuracy`, `Recall`, etc.

**Need help finding metric names?** See the [All Metrics Reference Table](/metrics/all_metrics) for a full list of Metrics.

### [​](#metric-labels) Metric labels

Some Metrics require additional context. This applies when the metrics:

* Operate at the column level
* Return multiple values (metric results)
* Have user-defined custom parameters

In these cases, use `metric_labels` to specify what exactly you want to plot.
**Example**. To plot the share of categories inside “Denials” column:

Copy

```python
project.dashboard.add_panel(
             DashboardPanelPlot(
                title="Denials",
                subtitle = "Number of denials.",
                size="half",
                values=[
                    PanelMetric(
                        legend="""{{label}}""",
                        metric="UniqueValueCount", # <- metric from TextEvals Preset that computes distinct values
                        metric_labels={"column": "denials", #column name
                                       "value_type": "share" #metric result
                                       } 
                    ),
                ],
                plot_params={"plot_type": "bar", "is_stacked": True},
            ),
            tab="My tab",
        )
```

**Column / Descriptor**. When you compute a text descriptor or any metric that operates at the column level, use the `column` label to specify which column or descriptor it refers to.
For example, in a `TextEvals` Report, each text descriptor (e.g., text length, LLM judged “denials”, etc.) is treated as a column. These descriptors are summarized with various statistics. To plot one of these values, you need to:

* Choose a summary Metric like `UniqueValueCount`, `MissingValueCount`, `MaxValue`, etc.
* Use the `column` label to point the specific descriptor.

**Example**. To plot the min value from the “Text Length” column:

Copy

```python
values=[
    PanelMetric(
        legend="Min text length",
        metric="MinValue", # <- metric from TextEvals Preset that computes min value
        metric_labels={
            "column": "TextLength",  # <- target column name 
        }
    )
]
```

**Value type**. Most Evidently Metrics return a single `value`. For example, `Accuracy` returns the corresponding accuracy `value`. So listing just the `Metric` name is enough to specify what exactly you want to plot.
However, some metrics produce more than one metric result, like:

* `CategoryCount`: returns both `share` and `count`
* `MAE`: returns both `mean` and `std`

In this case, you must point to which value you want using the `value_type` key, e.g. `{"value_type": "share"}`

Copy

```python
values = [
    PanelMetric(
        legend="Share",
        metric="DriftedColumnsCount",  # <- metric from Data Drift Preset that returns `count` or `share` of drifting columns
        metric_labels={"value_type": "share"}  # <- plot relative share
    ),
]
```

**How to verify the metric result for a specific metric?**

* Look up the expected outputs in the [All Metrics Table](/metrics/all_metrics).
* Or, generate a Report with the target `metric` and inspect its structure via`report.dict()` or `report.json()`.

**Metrics with extra parameters**. If a metric has configurable options (like drift method), you must also include those in `metric_labels`.

### [​](#panelmetric-options) `PanelMetric` options

A summary of all parameters:

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `legend` | `str` | ❌ | `None` | Legend name in the panel. If `None`, one is auto-generated. |
| `tags` | `list` | ❌ | `[]` | Optional tags to select values only from a subset of Reports in the Project. |
| `metadata` | `dict` | ❌ | `{}` | Optional metadata to select values only from a subset of Reports in the Project. |
| `metric` | `str` | ✅ | — | Metric name (e.g., `"RowCount"`). |
| `metric_labels` | `dict` | ❌ | `{}` | Parameters like `column` names (applies to descriptors too) or `value_type`. |