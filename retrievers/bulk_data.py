import uuid
from typing import Iterable, List

import ijson
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from langchain_core.embeddings import Embeddings




import ijson
from tqdm import tqdm

from bge_embedding import BgeEmbedding


def get_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # 使用 ijson 的 items 函数来逐行迭代 JSON 数据
        for item in ijson.items(file, 'item'):
            # 这里 'item' 是 JSON 数据的根节点
            yield item




def create_index(
    es_client: Elasticsearch,
    index_name: str,
):
    es_client.indices.create(
        index=index_name,
        mappings={
            "properties": {
                'title': {"type": "text"},
                'content_embedding': {"type": "dense_vector"},
                'content': {"type": "text"},
                'timestamp': {"type": "date",
                            "format": "yyyy.MM.dd"}
            }
        },
    )


def index_data_batch(
    es_client: Elasticsearch,
    index_name: str,
    batch_data: List,
    refresh: bool = True,
) -> None:

    total_requests = 0

    requests = [
        {
            "_op_type": "index",
            "_index": index_name,
            "_id": uuid.uuid4(),
            'title': data['title'],
            'content': data['content'],
            'timestamp': data['timestamp'],
            'content_embedding': data['content_embedding']
        }
        for data in batch_data
    ]
    bulk(es_client, requests)
    total_requests += len(requests)

    if refresh:
        es_client.indices.refresh(index=index_name)



if __name__ == '__main__':
    if __name__ == '__main__':
        path = '/Users/dewey/Documents/taa_agency.json'
        es_client = Elasticsearch(hosts=['http://localhost:9200'],basic_auth=('elasic','llSn0ICO*b=FxMCVlo0H'))  # 更改为你的Elasticsearch主机
        index_name = "test-langchain-retriever"
        if not es_client.indices.exists(index=index_name):
            create_index(es_client, index_name)
        datas = []
        bge = BgeEmbedding()
        for data in tqdm(get_json_data(path)):
            embedding = bge.embed_query(data['chunks'][:512])
            tmp = dict()
            tmp['title'] = data['title_or_question']
            tmp['content'] = data['chunks']
            tmp['content_embedding'] = embedding
            tmp['timestamp'] = data['timestamp']
            datas.append(tmp)  # 将数据添加到列表中
            if len(datas) >= 20:
                index_data_batch(es_client, index_name, datas)
                datas = []  # 清空列表以准备下一批数据

        # 处理剩余的数据，如果不足20条
        if datas:
            index_data_batch(es_client, index_name, datas)
