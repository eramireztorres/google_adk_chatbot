import hashlib
from typing import List

from langchain_core.embeddings import Embeddings


class FakeEmbeddings(Embeddings):
    """Deterministic, local embeddings for tests only."""

    embedding_dimension = 8

    def _hash_to_vec(self, text: str) -> List[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        # 8 floats from bytes, normalized to [0,1]
        return [b / 255.0 for b in digest[: self.embedding_dimension]]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._hash_to_vec(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._hash_to_vec(text)

    def __call__(self, text: str) -> List[float]:
        return self.embed_query(text)


class DummyLLM:
    def __init__(self, content: str = "OK"):
        self._content = content

    def invoke(self, _prompt: str):
        class _Resp:
            def __init__(self, content: str):
                self.content = content

        return _Resp(self._content)
