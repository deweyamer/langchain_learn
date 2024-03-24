from typing import Dict

from elasticsearch import Elasticsearch
from retrievers.elasticsearch_retriever import ElasticsearchRetriever

es_url = "http://localhost:9200"
es_client = Elasticsearch(hosts=[es_url])
index_name = "test-langchain-retriever"
title_field = "title"
content_field = "title"

def bm25_query_content(search_query: str) -> Dict:
    return {
        "query": {
            "match": {
                'content': search_query,
            },
        },
    }





bm25_content_retriever = ElasticsearchRetriever.from_es_params(
    index_name=index_name,
    body_func=bm25_query_content,
    content_field='content',
    url=es_url,
)

