from langchain.retrievers import EnsembleRetriever
from retrievers.elastic_bm25_cotent_retriever import bm25_content_retriever
from retrievers.elastic_bm25_title_retriever import bm25_title_retriever


ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_content_retriever, bm25_title_retriever], weights=[0.5, 0.5]
)

# docs = ensemble_retriever.get_relevant_documents("三流一致")
# print(docs)
