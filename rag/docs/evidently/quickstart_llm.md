---
url: https://docs.evidentlyai.com/quickstart_llm
source: Evidently Documentation
---

Evidently helps you evaluate LLM outputs automatically. The lets you compare prompts, models, run regression or adversarial tests with clear, repeatable checks. That means faster iterations, more confident decisions, and fewer surprises in production.
In this Quickstart, you’ll try a simple eval in Python and view the results in Evidently Cloud. If you want to stay fully local, you can also do that - just skip a couple steps.
There are a few extras, like custom LLM judges or tests, if you want to go further.
Let’s dive in.

Need help at any point? Ask on [Discord](https://discord.com/invite/xZjKRaNp8b).

## [​](#1-set-up-your-environment) 1. Set up your environment

For a fully local flow, skip steps 1.1 and 1.3.

### [​](#1-1-set-up-evidently-cloud) 1.1. Set up Evidently Cloud

* **Sign up** for a free [Evidently Cloud account](https://app.evidently.cloud/signup).
* **Create an Organization** if you log in for the first time. Get an ID of your organization. ([Link](https://app.evidently.cloud/organizations)).
* **Get an API token**. Click the **Key** icon in the left menu. Generate and save the token. ([Link](https://app.evidently.cloud/token)).

### [​](#1-2-installation-and-imports) 1.2. Installation and imports

Install the Evidently Python library:

Copy

```python
!pip install evidently
```

Components to run the evals:

Copy

```python
import pandas as pd
from evidently import Dataset
from evidently import DataDefinition
from evidently import Report
from evidently.presets import TextEvals
from evidently.tests import lte, gte, eq
from evidently.descriptors import LLMEval, TestSummary, DeclineLLMEval, Sentiment, TextLength, IncludesWords
from evidently.llm.templates import BinaryClassificationPromptTemplate
```

Components to connect with Evidently Cloud:

Copy

```python
from evidently.ui.workspace import CloudWorkspace
```

### [​](#1-3-create-a-project) 1.3. Create a Project

Connect to Evidently Cloud using your API token:

Copy

```python
ws = CloudWorkspace(token="YOUR_API_TOKEN", url="https://app.evidently.cloud")
```

Create a Project within your Organization, or connect to an existing Project:

Copy

```python
project = ws.create_project("My project name", org_id="YOUR_ORG_ID")
project.description = "My project description"
project.save()

# or project = ws.get_project("PROJECT_ID")
```

## [​](#2-prepare-the-dataset) 2. Prepare the dataset

Let’s create a toy demo chatbot dataset with “Questions” and “Answers”.

Copy

```python
data = [
    ["What is the chemical symbol for gold?", "Gold chemical symbol is Au."],
    ["What is the capital of Japan?", "The capital of Japan is Tokyo."],
    ["Tell me a joke.", "Why don't programmers like nature? Too many bugs!"],
    ["When does water boil?", "Water's boiling point is 100 degrees Celsius."],
    ["Who painted the Mona Lisa?", "Leonardo da Vinci painted the Mona Lisa."],
    ["What’s the fastest animal on land?", "The cheetah is the fastest land animal, capable of running up to 75 miles per hour."],
    ["Can you help me with my math homework?", "I'm sorry, but I can't assist with homework."],
    ["How many states are there in the USA?", "USA has 50 states."],
    ["What’s the primary function of the heart?", "The primary function of the heart is to pump blood throughout the body."],
    ["Can you tell me the latest stock market trends?", "I'm sorry, but I can't provide real-time stock market trends. You might want to check a financial news website or consult a financial advisor."]
]
columns = ["question", "answer"]

eval_df = pd.DataFrame(data, columns=columns)
#eval_df.head()
```

**Preparing your own data**. You can provide data with any structure. Some common setups:

* Inputs and outputs from your LLM
* Inputs, outputs, and reference outputs (for comparison)
* Inputs, context, and outputs (for RAG evaluation)

**Collecting live data**. You can also trace inputs and outputs from your LLM app and download the dataset from traces. See the [Tracing Quickstart](/quickstart_tracing)

## [​](#3-run-evaluations) 3. Run evaluations

We’ll evaluate the answers for:

* **Sentiment:** from -1 (negative) to 1 (positive)
* **Text length:** character count
* **Denials:** refusals to answer. This uses an LLM-as-a-judge with built-in prompt.

Each evaluation is a `descriptor`. It adds a new score or label to each row in your dataset.
For LLM-as-a-judge, we’ll use OpenAI GPT-4o mini. Set OpenAI key as an environment variable:

Copy

```python
## import os
## os.environ["OPENAI_API_KEY"] = "YOUR KEY"
```

If you don’t have an OpenAI key, you can use a keyword-based check `IncludesWords` instead.

To run evals, pass the dataset and specify the list of descriptors to add:

Copy

```python
eval_dataset = Dataset.from_pandas(
    eval_df,
    data_definition=DataDefinition(),
    descriptors=[
        Sentiment("answer", alias="Sentiment"),
        TextLength("answer", alias="Length"),
        DeclineLLMEval("answer", alias="Denials")]) 

# Or IncludesWords("answer", words_list=['sorry', 'apologize'], alias="Denials")
```

**Congratulations!** You’ve just run your first eval. Preview the results locally in pandas:

Copy

```python
eval_dataset.as_dataframe()
```

![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/examples/llm_quickstart_preview.png)

**What other evals are there?** Browse all available descriptors including deterministic checks, semantic similarity, and LLM judges in the [descriptor list](/metrics/all_descriptors).

## [​](#4-create-a-report) 4. Create a Report

**Create and run a Report**. It will summarize the evaluation results.

Copy

```python
report = Report([
    TextEvals()
])

my_eval = report.run(eval_dataset, None)
```

**Local preview**. In a Python environment like Jupyter notebook or Colab, run:

Copy

```python
my_eval
```

This will render the Report directly in the notebook cell. You can also get a JSON or Python dictionary, or save as an external HTML file.

Copy

```python
# my_eval.json()
# my_eval.dict()
# my_report.save_html(“file.html”)
```

Local Reports are great for quick experiments. To run comparisons, keep track of the results and collaborate with others, upload the results to Evidently Platform.
**Upload the Report to Evidently Cloud** together with scored data:

Copy

```python
ws.add_run(project.id, my_eval, include_data=True)
```

**Explore.** Go to [Evidently Cloud](https://app.evidently.cloud/), open your Project, and navigate to Reports. You will see all score summaries and can browse the data. E.g. sort to find all answers labeled as “Denials”.
![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/examples/llm_quickstart_explore.png)

## [​](#5-get-a-dashboard) 5. Get a Dashboard

As you run more evals, it’s useful to track them over time. Go to “Dashboard” in the left menu, enter the “Edit” mode, and add a new “Columns” tab:
![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/examples/llm_quickstart_create_tab_new.gif)
You’ll see a set of panels with descriptor values. Each will have a single data point for now. As you log more evaluation results, you can track trends and set up alerts.
Want to see more complex workflows? You can add pass/fail conditions and custom evals.

## [​](#6-optional-add-tests) 6. (Optional) Add tests

You can add conditions to your evaluations. For example, you may expect that:

* **Sentiment** is non-negative (greater or equal to 0)
* **Text length** is at most 150 symbols (less or equal to 150).
* **Denials**: there are none.
* If any condition is false, consider the output to be a “fail”.

You can implement this logic easily.


Add test conditions

How to add test conditions

Copy

```python
# Run the evaluation with tests 
eval_dataset = Dataset.from_pandas(
  eval_df,
  data_definition=DataDefinition(),
  descriptors=[
      Sentiment("answer", alias="Sentiment",
                tests=[gte(0, alias="Is_non_negative")]),
      TextLength("answer", alias="Length",
                 tests=[lte(150, alias="Has_expected_length")]),
      DeclineLLMEval("answer", alias="Denials",
                     tests=[eq("OK", column="Denials",
                               alias="Is_not_a_refusal")]),
      TestSummary(success_all=True, alias="All_tests_passed")])

# Uncomment to preview the results locally
# eval_dataset.as_dataframe()
```

![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/examples/llm_quickstart_descriptor_tests-min.png)You can limit the summary report to include only specific descriptor(s).

Copy

```python
report = Report([
    TextEvals(columns=["All_tests_passed"])
])

my_eval = report.run(eval_dataset, None)
ws.add_run(project.id, my_eval, include_data=True)

#my_eval
```

To identify rows that failed any criteria, sort by “All\_test\_passed” column:

![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/examples/llm_quickstart_descriptor_tests_report-min.png)

## [​](#7-optional-add-a-custom-llm-jugde) 7. (Optional) Add a custom LLM jugde

You can implement custom criteria using built-in LLM judge templates.


Custom LLM judge

How to create a custom LLM evaluator

Let’s classify user questions as “appropriate” or “inappropriate” for an educational tool.

Copy

```python
# Define the evaluation criteria
appropriate_scope = BinaryClassificationPromptTemplate(
    criteria="""An appropriate question is any educational query related to
    academic subjects, general school-level world knowledge, or skills.
    An inappropriate question is anything offensive, irrelevant, or out of
    scope.""",
    target_category="APPROPRIATE",
    non_target_category="INAPPROPRIATE",
    include_reasoning=True,
)

# Apply evaluation
llm_evals = Dataset.from_pandas(
    eval_df,
    data_definition=DataDefinition(),
    descriptors=[
        LLMEval("question", template=appropriate_scope,
                provider="openai", model="gpt-4o-mini",
                alias="Question topic")
    ]
)

# Run and upload report
report = Report([
    TextEvals()
])

my_eval = report.run(llm_evals, None)
ws.add_run(project.id, my_eval, include_data=True)

# Uncomment to replace ws.add_run for a local preview 
# my_eval
```

You can implement any criteria this way, and plug in different LLM models.

![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/examples/llm_quickstart_descriptor_custom_llm_judge-min.png)

## [​](#what’s-next) What’s next?

Read more on how you can configure [LLM judges for custom criteria or using other LLMs](/metrics/customize_llm_judge).
We also have lots of other examples! [Explore tutorials](/metrics/introduction).