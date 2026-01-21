from evidently.descriptors import (
    CorrectnessLLMEval,
    BERTScore,
    SemanticSimilarity,
    ContextRelevance,
    FaithfulnessLLMEval,
)
from evidently import Report
from evidently.presets import TextEvals
try:
    from evidently import Dataset, DataDefinition
    from evidently.core.datasets import RAG
except ImportError:
    from evidently.core import Dataset, DataDefinition
    # Try to find RAG elsewhere if needed
    try:
        from evidently.core.datasets import RAG
    except ImportError:
        RAG = None

import inspect

print("--- Dataset.from_pandas ---")
print(inspect.signature(Dataset.from_pandas))

if RAG:
    print("\n--- evidently.core.datasets.RAG ---")
    print(inspect.signature(RAG))

print("\n--- TextEvals ---")
print(inspect.signature(TextEvals))

print("--- CorrectnessLLMEval ---")
print(inspect.signature(CorrectnessLLMEval))
# print(help(CorrectnessLLMEval))

print("\n--- BERTScore ---")
print(inspect.signature(BERTScore))

print("\n--- SemanticSimilarity ---")
print(inspect.signature(SemanticSimilarity))

print("\n--- ContextRelevance ---")
print(inspect.signature(ContextRelevance))

print("\n--- FaithfulnessLLMEval ---")
print(inspect.signature(FaithfulnessLLMEval))
