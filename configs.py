import os

from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI
import tiktoken
import requests

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pc_index = pc.Index(os.getenv("INDEX"))
reddit_pass = os.getenv("REDDIT_PASS")
reddit_user = os.getenv("REDDIT_USER")
reddit_app_id = os.getenv("REDDIT_CLIENT_ID")
reddit_app_secret = os.getenv("REDDIT_SECRET")

openai_client = OpenAI()
EMBEDDINGS_MODEL = "text-embedding-3-small"

INDEX_NAMESPACES = {'nfl': {'reg_season': 'nfl_reg_season', 'post_season': 'nfl_post_season'}}

encoding = tiktoken.encoding_for_model(EMBEDDINGS_MODEL)

def get_reddit_token():
    #https://github.com/reddit-archive/reddit/wiki/OAuth2
    client_auth = requests.auth.HTTPBasicAuth(reddit_app_id, reddit_app_secret)
    post_data = {"grant_type": "password", "username": reddit_user, "password": reddit_pass}
    headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    return response.json()['access_token']
