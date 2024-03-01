import time

from pinecone import Pinecone, PodSpec
import tiktoken
from tiktoken import Encoding

from configs import pc_index, openai_client, EMBEDDINGS_MODEL, encoding

def get_token_count(text: str) -> Encoding:
    # https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
    return len(encoding.encode(text))

def delete_vectors():
    delete_response = pc_index.delete(deleteAll=True)
    return delete_response

def get_embedding(text, model=EMBEDDINGS_MODEL):
   text = text.replace("\n", " ")
   return openai_client.embeddings.create(input = [text], model=model).data[0].embedding

def create_index(index_name: str, pc: Pinecone):
    print(f'creating index: {index_name}')
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=PodSpec(environment='gcp-starter')
    )
    while not pc.describe_index(index_name).status['ready']:
        print('creating index')
        time.sleep(1)
    print('done creating index')