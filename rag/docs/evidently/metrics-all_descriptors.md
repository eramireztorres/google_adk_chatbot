---
url: https://docs.evidentlyai.com/metrics/all_descriptors
source: Evidently Documentation
---

For an intro, read about [Core Concepts](/docs/library/overview) and check the [LLM Quickstart](/quickstart_llm). For a reference code example, see this [Descriptor cookbook](https://github.com/evidentlyai/evidently/blob/main/examples/cookbook/descriptors.ipynb).

## [​](#deterministic-evals) Deterministic evals

Programmatic and heuristics-based evaluations.

### [​](#pattern-match) Pattern match

Check for general pattern matching.

| Name | Description | Parameters |
| --- | --- | --- |
| **ExactMatch()** | * Checks if the column contents matches between two provided columns. * Returns True/False for every input. * Example: `ExactMatch(columns=["answer", "target"])` | **Required:**  * `columns`  **Optional:**  * `alias` |
| **RegExp()** | * Matches the text against a set regular expression. * Returns True/False for every input. * Example: `RegExp(reg_exp=r"^I")` | **Required:**  * `reg_exp`  **Optional:**  * `alias` |
| **BeginsWith()** | * Checks if the text starts with a given combination. * Returns True/False for every input. * Example: `BeginsWith(prefix="How")` | **Required:**  * `prefix`  **Optional:**  * `alias` * `case_sensitive = True` or `False` |
| **EndsWith()** | * Checks if the text ends with a given combination. * Returns True/False for every input. * Example: `EndsWith(suffix="Thank you."`) | **Required:**  * `suffix`  **Optional:**  * `alias` * `case_sensitive = True` or `False` |

### [​](#content-checks) Content checks

Verify presence of specific words, items or components.

| Name | Description | Parameters |
| --- | --- | --- |
| **Contains()** | * Checks if the text contains **any** or **all** specified items (e.g., competitor names). * Returns True/False for every input. * Example: `Contains(items=["chatgpt"])` | **Required:**  * `items: List[str]`  **Optional:**  * `alias` * `mode = any` or `all` * `case_sensitive = True` or `False` |
| **DoesNotContain()** | * Checks if the text does not contain the specified items (e.g., forbidden expressions). * Returns True/False for every input. * Example: `DoesNotContain(items=["as a large language model"])` | **Required:**  * `items: List[str]`  **Optional:**  * `alias` * `mode = all` * `case_sensitive = True` or `False` |
| **IncludesWords()** | * Checks if the text includes **any** or **all** specified words. * Considers only vocabulary words. * Returns True/False for every input. * Example: `IncludesWords(words_list=['booking', 'hotel', 'flight'])` | **Required:**  * `words_list: List[str]`  **Optional:**  * `alias` * `mode = any` or `all` * `lemmatize = True` or `False` |
| **ExcludesWords()** | * Checks if the texts excludes all specified words (e.g. profanity lists). * Considers only vocabulary words. * Returns True/False for every input. * Example: `ExcludesWords(words_list=['buy', 'sell', 'bet'])` | **Required:**  * `words_list: List[str]`  **Optional:**  * `alias` * `mode = all` * `lemmatize = True` or `False` |
| **ItemMatch()** | * Checks if the text contains **any** or **all** specified items. * The item list is specific to each row and provided in a separate column. * Returns True/False for each row. * Example: `ItemMatch(["Answer", "Expected_items"])` | **Required:**  * `columns`  **Optional:**  * `alias` * `mode = all` or `any` * `case_sensitive = True` or `False` |
| **ItemNoMatch()** | * Checks if the text excludes **all** specified items. * The item list is specific to each row and provided in a separate column. * Returns True/False for each row. * Example: `ItemMatch(["Answer", "Forbidden_items"])` | **Required:**  * `columns`  **Optional:**  * `alias` * `mode = all` * `case_sensitive = True` or `False` |
| **WordMatch()** | * Checks if the text includes **any** or **all** specified words. * Word list is specific to each row and provided in a separate column. * Considers only vocabulary words. * Returns True/False for every input. * Example: `WordMatch(["Answer", "Expected_words"]` | **Required:**  * `columns`  **Optional:**  * `alias` * `mode = any` or `all` * `lemmatize = True` or `False` |
| **WordNoMatch()** | * Checks if the text excludes **all** specified words. * Word list is specific to each row and provided in a separate column. * Considers only vocabulary words. * Returns True/False for every input. * Example: `WordNoMatch(["Answer", "Forbidden_words"]` | **Required:**  * `columns`str  **Optional:**  * `alias` * `mode = all` * `lemmatize = True` or `False` |
| **ContainsLink()** | * Checks if the column contains at least one valid URL. * Returns True/False for each row. | **Optional:**  * `alias` |

### [​](#syntax-validation) Syntax validation

Validate structured data formats or code syntax.

| Name | Description | Parameters |
| --- | --- | --- |
| **IsValidJSON()** | * Checks if the column contains a valid JSON. * Returns True/False for every input. | **Optional:**  * `alias` |
| **JSONSchemaMatch()** | * Checks if the column contains a valid JSON object matching the expected **schema**: all keys are present and values are not `None`. * Exact match mode checks no extra keys are present. * Optional type validation for each key. * Returns True/False for each input. * Example: `JSONSchemaMatch(expected_schema={"name": str, "age": int}, exact_match=False, validate_types=True)` | **Required:**  * `expected_schema: Dict[str, type]`  **Optional:**  * `exact_match = True` or `False` * `validate_types = True` or `False` |
| **JSONMatch()** | * Checks if the column contains a valid JSON object matching a JSON provided in a reference column. * Matches **key-value pairs** irrespective of order. * Whitespace outside of the actual values (e.g., spaces or newlines) is ignored. * Returns True/False for every input. * Example: `JSONMatch(first_column="Json1", second_column="Json2"),` | **Required:**  * `first_column` * `second_column`  **Optional:**  * `alias` |
| **IsValidPython()** | * Checks if the column contains valid Python code without syntax errors. * Returns True/False for every input. | **Optional:**  * `alias` |
| **IsValidSQL()** | * Checks if the column contains a valid SQL query without executing the query. * Returns True/False for every input. | **Optional:**  * `alias` |

### [​](#text-stats) Text stats

Descriptive text statistics.

| Name | Descriptor | Parameters |
| --- | --- | --- |
| **TextLength()** | * Measures the length of the text in symbols. * Returns an absolute number. | **Optional:**  * `alias` |
| **OOVWordsPercentage()** | * Calculates the percentage of out-of-vocabulary words based on imported NLTK vocabulary. * Returns a score on a scale: 0 to 100. | **Optional:**  * `alias` * `ignore_words: Tuple = ()` |
| **NonLetterCharacterPercentage()** | * Calculates the percentage of non-letter characters. * Returns a score on a scale: 0 to 100. | **Optional:**  * `alias` |
| **SentenceCount()** | * Counts the number of sentences in the text. * Returns an absolute number. | **Optional:**  * `alias` |
| **WordCount()** | * Counts the number of words in the text. * Returns an absolute number. | **Optional:**  * `alias` |

### [​](#custom) Custom

Implement your own programmatic checks.

| Name | Descriptor | Parameters |
| --- | --- | --- |
| **CustomDescriptor()** | * Implements a custom check for specific column(s) as a Python function. * Use it to run your own programmatic checks. * Returns score and/or label as specified. * Can accept and return multiple columns. | **Optional:**  * `alias` * `func: callable`  See [how to add a custom descriptor](/metrics/customize_descriptor). |
| **CustomColumnsDescriptor()** | * Implements a custom check as a Python function that can be applied to any column in the dataset. * Use it to run your own programmatic checks. * Returns score and/or label as specified. * Accepts and returns a single column. | **Optional:**  * `alias` * `func: callable`  See [how to add a custom descriptor](/metrics/customize_descriptor). |

## [​](#llm-based-evals) LLM-based evals

Using an external LLMs with an evaluation prompt. You can specify the LLM to use as an evaluator.

### [​](#custom-2) Custom

LLM judge templates.

| Name | Descriptor | Parameters |
| --- | --- | --- |
| **LLMEval()** | * Scores the text using user-defined criteria. * You must specify provider, model and use prompt template to formulate the criteria. * Returns score and/or label as specified. | **Optional:**  * `alias` * `template` * `provider` * `model` * `additional_columns: dict` * See [custom LLM judge parameters](/metrics/customize_llm_judge). |

### [​](#rag) RAG

RAG-specific evals for retrieval and generation. ([Tutorial](/examples/LLM_rag_evals)).

| Name | Descriptor | Parameters |
| --- | --- | --- |
| **ContextQualityLLMEval()** | * Evaluates if the context provides sufficient information to answer the question. * Returns a label (VALID or INVALID) or a score. * Run over the “context” column and pass the `question` column as a parameter. * Example: `ContextQualityLLMEval("Context", question="Question")` | **Required:**  * `question`  **Optional:**  * `alias` * `provider` * `model` * See [LLM judge parameters](/metrics/customize_llm_judge). |
| **ContextRelevance()** | * Checks if the context is relevant to the given question (0 to 1) for multiple context chunks. * Pass all context chunks as a list in the `context` column. * Uses semantic similarity (default) or LLM. * Aggregates relevance: `mean` (default) or `hit` (at least one chunk is relevant). * Example: `ContextRelevance("Question", "Context", output_scores=True, aggregation_method="hit", method="llm")` | **Required:**  * `input` * `contexts`  **Optional:**  * `output_scores`: `False` or `True` * `method`: `semantic_similarity` or `llm` * `aggregation_method`: `mean` or `hit` * `aggregation_method_params={"threshold":0.95}` (set the relevance threshold as greater or equal, 0.8 by default) * `alias` * `provider` * `model` * See [LLM judge parameters](/metrics/customize_llm_judge). |
| **FaithfulnessLLMEval()** | * Assesses whether the response stays faithful to the given context.Checks for hallucinations or unsupported claims. * Returns a label (FAITHFUL or UNFAITHFUL) or a score. * Run over the “response” column and pass the `context` column as a parameter. * Example: `FaithfulnessLLMEval("Response", context="Context")` | **Required:**  * `context`  **Optional:**  * `alias` * `provider` * `model` * See [LLM judge parameters](/metrics/customize_llm_judge). |
| **CompletenessLLMEval()** | * Determines whether the response fully uses the information provided in the context. * Returns a label (COMPLETE or INCOMPLETE) or a score. * Run over the “response” column and pass the `context` column as a parameter. * Example: `CompletenessLLMEval("Response", context="Context")` | **Required:**  * `context`  **Optional:**  * `alias` * `provider` * `model` * See [LLM judge parameters](/metrics/customize_llm_judge). |

### [​](#generation) Generation

Evals for varied generation scenarios.

| Name | Descriptor | Parameters |
| --- | --- | --- |
| **CorrectnessLLMEval()** | * Evaluates the correctness of a response by comparing it with the target output. * Useful for RAG or any LLM generation where you have a ground truth output * Returns a label (CORRECT or INCORRECT) or a score. * Run over the “response” column and pass the `target_output` column as a parameter. * Example: `CorrectnessLLMEval("Response", target_output="Target")` | **Required:**  * `target_output`  **Optional:**  * `alias` * `provider` * `model` * See [LLM judge parameters](/metrics/customize_llm_judge). |
| **DeclineLLMEval()** | * Detects if the text contains a refusal or rejection. * Useful to detect instances where an LLM denies the user response. * Returns a label (DECLINE or OK) or a score. | **Optional:**  * `alias` * `provider` * `model` * See [LLM judge parameters](/metrics/customize_llm_judge). |
| **PIILLMEval()** | * Detects texts containing PII (Personally Identifiable Information). * Returns a label (PII or OK) or a score. | **Optional:**  * `alias` * `provider` * `model` * See [LLM judge parameters](/metrics/customize_llm_judge). |
| **NegativityLLMEval()** | * Detects negative texts. * Returns a label (NEGATIVE or POSITIVE) or a score. | **Optional:**  * `alias` * `provider` * `model` * See [LLM judge parameters](/metrics/customize_llm_judge). |
| **BiasLLMEval()** | * Detects biased texts. * Returns a label (BIAS or OK) or a score. | **Optional:**  * `alias` * `provider` * `model` * See [LLM judge parameters](/metrics/customize_llm_judge). |
| **ToxicityLLMEval()** | * Detects toxic texts. * Returns a label (TOXICITY or OK) or a score. | **Optional:**  * `alias` * `provider` * `model` * See [LLM judge parameters](/metrics/customize_llm_judge). |

## [​](#ml-based-evals) ML-based evals

Use pre-trained machine learning or embedding models.

| Name | Descriptor | Parameters |
| --- | --- | --- |
| **SemanticSimilarity()** | * Calculates pairwise semantic similarity (Cosine Similarity) between two columns using a sentence embeddings model [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). * Returns a score from 0 to 1: (0: different, 0.5: unrelated, 1: identical) * Example use: `SemanticSimilarity(columns=["Question", "Answer"])`. | **Required:**  * `columns`  **Optional:**  * `alias` |
| **BERTScore()** | * Calculates similarity between two text columns based on token embeddings. * Returns [BERTScore](https://arxiv.org/pdf/1904.09675) (F1 Score). * Example use: `BERTScore(columns=["Answer", "Target"])`. | **Required:**  * `columns`  **Optional:**  * `model` * `tfidf_weighted` * `alias` |
| **Sentiment()** | * Analyzes text sentiment using a word-based model from NLTK. * Returns a score: -1 (negative) to 1 (positive). | **Optional:**  * `alias` |
| **HuggingFace()** | * Scores the text using a user-selected HuggingFace model. * See [HuggingFace descriptor docs](/metrics/customize_hf_descriptor) for example models. | **Optional:**  * `alias` * See [docs](/metrics/customize_hf_descriptor). |
| **HuggingFaceToxicity()** | * Detects hate speech using a [`roberta-hate-speech`](https://huggingface.co/facebook/roberta-hate-speech-dynabench-r4-target) model. * Returns predicted probability for the “hate” label. Scale: 0 to 1. | **Optional:**  * `toxic_label`(default: `hate`) * `alias` * See [docs](/metrics/customize_hf_descriptor). |