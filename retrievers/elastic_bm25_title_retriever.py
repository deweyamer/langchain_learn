from typing import Dict

from elasticsearch import Elasticsearch

from retrievers.elasticsearch_retriever import ElasticsearchRetriever

es_url = "http://localhost:9200"
es_client = Elasticsearch(hosts=[es_url])
index_name = "test-langchain-retriever"

def bm25_query(search_query: str) -> Dict:
    return {
        "query": {
            "match": {
                'title': search_query,
            },
        },
    }


bm25_title_retriever = ElasticsearchRetriever.from_es_params(
    index_name=index_name,
    body_func=bm25_query,
    content_field='content',
    url=es_url,
)
