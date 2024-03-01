import os

from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI
import tiktoken

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pc_index = pc.Index(os.getenv("INDEX"))

openai_client = OpenAI()
EMBEDDINGS_MODEL = "text-embedding-3-small"

INDEX_NAMESPACES = {'nfl': {'reg_season': 'nfl_reg_season', 'post_season': 'nfl_post_season'}}

encoding = tiktoken.encoding_for_model(EMBEDDINGS_MODEL)