from typing import List

from langchain_community.embeddings import HuggingFaceBgeEmbeddings


class BgeEmbedding:
    def __init__(self):
        model_name = "/Users/dewey/embeddings/bge-small-zh-v1.5"
        model_kwargs = {"device": "cpu"}
        encode_kwargs = {"normalize_embeddings": True}
        self.hf = HuggingFaceBgeEmbeddings(
            model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
        )

    def embed_query(self, text: str) -> List[float]:
        return self.hf.embed_query(text)

    def embed_documents(self, texts:list[str]) -> List[List[float]]:
        embeds = []
        for text in texts:
            embeds.append(self.embed_query(text))
        return embeds


