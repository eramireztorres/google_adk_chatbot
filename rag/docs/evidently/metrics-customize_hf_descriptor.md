---
url: https://docs.evidentlyai.com/metrics/customize_hf_descriptor
source: Evidently Documentation
---

You can score your text by downloading and using ML models from HuggingFace. This lets you apply any criteria from the source model, e.g. classify texts by emotion. There are:

* Ready-to-use descriptors that wrap a specific model,
* A general interface to call other suitable models you select.

**Pre-requisites**:

* You know how to use [descriptors](/docs/library/descriptors) to evaluate text data.

## [​](#imports) Imports

Copy

```python
from evidently.descriptors import HuggingFace, HuggingFaceToxicity
```

Toy data to run the example

To generate toy data and create a Dataset object:

Copy

```python
import pandas as pd

from evidently import Dataset
from evidently import DataDefinition

data = [
    ["Why is the sky blue?", 
     "The sky is blue because molecules in the air scatter blue light from the sun more than they scatter red light.", 
     "because air scatters blue light more"],
    ["How do airplanes stay in the air?", 
     "Airplanes stay in the air because their wings create lift by forcing air to move faster over the top of the wing than underneath, which creates lower pressure on top.", 
     "because wings create lift"],
    ["Why do we have seasons?", 
     "We have seasons because the Earth is tilted on its axis, which causes different parts of the Earth to receive more or less sunlight throughout the year.", 
     "because Earth is tilted"],
    ["How do magnets work?", 
     "Magnets work because they have a magnetic field that can attract or repel certain metals, like iron, due to the alignment of their atomic particles.", 
     "because of magnetic fields"],
    ["Why does the moon change shape?", 
     "The moon changes shape, or goes through phases, because we see different portions of its illuminated half as it orbits the Earth.", 
     "because it rotates"],
    ["What movie should I watch tonight?", 
     "A movie is a motion picture created to entertain, educate, or inform viewers through a combination of storytelling, visuals, and sound.", 
     "watch a movie that suits your mood"]
]

columns = ["question", "context", "response"]

df = pd.DataFrame(data, columns=columns)

eval_df = Dataset.from_pandas(
  df,
  data_definition=DataDefinition())
```

## [​](#built-in-ml-evals) Built-in ML evals

**Available descriptors**. Check all available built-in LLM evals in the [reference table](/metrics/all_descriptors#ml-based-evals).

There are built-in evaluators for some models. You can call them like any other descriptor:

Copy

```python
eval_df.add_descriptors(descriptors=[
    HuggingFaceToxicity("question", toxic_label="hate", alias="Toxicity") 
])
```

## [​](#custom-ml-evals) Custom ML evals

You can also add any custom checks [directly as a Python function](/metrics/customize_descriptor).

Alternatively, use the general `HuggingFace()` descriptor to call a specific named model. The model you use must return a numerical score or a category for each text in a column.
For example, to evaluate “curiousity” expressed in a text:

Copy

```python
eval_df.add_descriptors(descriptors=[
   HuggingFace("question",
       model="SamLowe/roberta-base-go_emotions", 
       params={"label": "curiosity"},
       alias="Curiousity"
   )
])
```

Call the result as usual:

Copy

```python
eval_df.as_dataframe()
```

Example output:
![](https://mintlify.s3.us-west-1.amazonaws.com/evi/images/examples/hf_descriptor_example_toxicity-min.png)

### [​](#sample-models) Sample models

Here are some models you can call using the `HuggingFace()` descriptor.

| Model | Example use | Parameters |
| --- | --- | --- |
| **Emotion classification**    * Scores texts by 28 emotions. * Returns the predicted probability for the chosen emotion label. * Scale: 0 to 1. * [HuggingFace Model](https://huggingface.co/SamLowe/roberta-base-go_emotions) | `HuggingFace("response", model="SamLowe/roberta-base-go_emotions", params={"label": "disappointment"}, alias="disappointment")` | **Required**:  * `params={"label":"label"}`  **Available labels**:  * admiration * amusement * anger * annoyance * approval * caring * confusion * curiosity * desire * disappointment * disapproval * disgust * embarrassment * excitement * fear * gratitude * grief * joy * love * nervousness * optimism * pride * realization * relief * remorse * sadness * surprise * neutral  **Optional**:  * `alias="name"` |
| **Zero-shot classification**    * A natural language inference model. * Use it for zero-shot classification by user-provided topics. * List candidate topics as `labels`. You can provide one or several topics. * You can set a classification threshold: if the predicted probability is below, an “unknown” label will be assigned. * Returns a label. * [HuggingFace Model](https://huggingface.co/MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli) | `HuggingFace("response", model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli", params={"labels": ["science", "physics"], "threshold":0.5}, alias="Topic")` | **Required**:  * `params={"labels": ["label"]}`  **Optional**:  * `params={"score_threshold": 0.7}` (default: 0.5) * `alias="name"` |
| **GPT-2 text detection**    * Predicts if a text is Real or Fake (generated by a GPT-2 model). * You can set a classification threshold: if the predicted probability is below, an “unknown” label will be assigned. * Note that it is not usable as a detector for more advanced models like ChatGPT. * Returns a label. * [HuggingFace Model](https://huggingface.co/openai-community/roberta-base-openai-detector) | `HuggingFace("response", model="openai-community/roberta-base-openai-detector", params={"score_threshold": 0.7}, alias="fake")` | **Optional**:  * `params={"score_threshold": 0.7}` (default: 0.5) * `alias="name"` |

This list is not exhaustive, and the Descriptor may support other models published on Hugging Face. The implemented interface generally works for models that:

* Output a single number (e.g., predicted score for a label) or a label, **not** an array of values.
* Can process raw text input directly.
* Name labels using `label` or `labels` fields.
* Use methods named `predict` or `predict_proba` for scoring.

However, since each model is implemented differently, we cannot provide a complete list of models with a compatible interface. We suggest testing the implementation on your own using trial and error. If you discover useful models, feel free to share them with the community in Discord. You can also open an issue on GitHub to request support for a specific model.