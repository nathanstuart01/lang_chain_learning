import sys
import time

from pinecone import Pinecone, PodSpec

from pinecone_configs import pc

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

if __name__ == '__main__':
    index_name = sys.argv[1]
    create_index(index_name, pc)
