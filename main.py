from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

from ollama_llm import OllamaLlm
from retrievers.ensemble_retriever import ensemble_retriever


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


template ="""请基于以下内容回答问题
{context}

问题: {question}
"""
prompt = ChatPromptTemplate.from_template(template)


retrieval_chain = (
    RunnableParallel({"context": ensemble_retriever | format_docs, "question": RunnablePassthrough()})
    | prompt
    # | model
    # | StrOutputParser()
)

print(retrieval_chain.invoke("开发票收税吗？"))
# print(chain.invoke({'question': '开发票收税吗？'}))
