import json

import tiktoken
import pandas as pd
from openai import OpenAI

from pinecone_configs import pc_index


client = OpenAI()

embedding_model = "text-embedding-3-small"
embedding_encoding = "cl100k_base"
max_tokens = 8000

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def combine_embed(df):
    encoding = tiktoken.get_encoding(embedding_encoding)
    df['combined'] = df.apply(lambda row: f'NFL Season Year: {row["Year"]}, Week: {row["Week"]}, Game Date: {row["Date"]}, Team 1: {row["Team 1"]}, Team 1 Site Status: {row["Team 1 Site Status"]}, Team 2: {row["Team 2"]}, Team 2 Site Status: {row["Team 2 Site Status"]}', axis=1)
    df["embedding"] = df.combined.apply(lambda x: get_embedding(x, model=embedding_model))
    return df


def upsert_data_vector_db(df: pd.DataFrame):
    combine_embed(df)
    docs = df.to_json(orient='records')
    parsed_docs = json.loads(docs)
    # https://docs.pinecone.io/docs/upsert-data