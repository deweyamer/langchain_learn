from typing import Dict

from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchRetriever

from bge_embedding import BgeEmbedding

es_url = "http://localhost:9200"
es_client = Elasticsearch(hosts=[es_url])
es_client.info()
index_name = "test-langchain-retriever"
text_field = "content"
dense_vector_field = "content_embedding"
num_characters_field = "num_characters"
texts = [
    "foo",
    "bar",
    "world",
    "hello world",
    "hello",
    "foo bar",
    "bla bla foo",
]

embeddings = BgeEmbedding()

def vector_query(search_query: str) -> Dict:
    vector = embeddings.embed_query(search_query)  # same embeddings as for indexing
    return {
        "knn": {
            "field": dense_vector_field,
            "query_vector": vector,
            "k": 5,
            "num_candidates": 10,
        }
    }


vector_retriever = ElasticsearchRetriever.from_es_params(
    index_name=index_name,
    body_func=vector_query,
    content_field=text_field,
    url=es_url,
)

