---
url: https://docs.evidentlyai.com/docs/library/output_formats
source: Evidently Documentation
---

You can view or export Reports in multiple formats.
**Pre-requisites**:

* You know how to [generate Reports](/docs/library/report).

## [​](#log-to-workspace) Log to Workspace

You can save the computed Report in Evidently Cloud or your local workspace.

Copy

```python
ws.add_run(project.id, my_eval, include_data=False)
```

**Uploading evals**. Check Quickstart examples [for ML](/quickstart_ml) or [for LLM](/quickstart_llm) for a full workflow.

## [​](#view-in-jupyter-notebook) View in Jupyter notebook

You can directly render the visual summary of evaluation results in interactive Python environments like Jupyter notebook or Colab.
After running the Report, simply call the resulting Python object:

Copy

```python
my_report
```

This will render the HTML object directly in the notebook cell.

## [​](#html) HTML

You can also save this interactive visual Report as an HTML file to open in a browser:

Copy

```python
my_report.save_html(“file.html”)
```

This option is useful for sharing Reports with others or if you’re working in a Python environment that doesn’t display interactive visuals.

## [​](#json) JSON

You can get the results of the calculation as a JSON. It is useful for storing and exporting results elsewhere.
To view the JSON in Python:

Copy

```python
my_report.json()
```

To save the JSON as a separate file:

Copy

```python
my_report.save_json("file.json")
```

## [​](#python-dictionary) Python dictionary

You can get the output as a Python dictionary. This format is convenient for automated evaluations in data or ML pipelines, allowing you to transform the output or extract specific values.
To get the dictionary:

Copy

```python
my_report.dict()
```