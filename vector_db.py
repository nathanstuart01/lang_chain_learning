import uuid
import json

import pandas as pd

from configs import pc_index, openai_client, embedding_model

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return openai_client.embeddings.create(input = [text], model=model).data[0].embedding

def create_metadata(row: pd.DataFrame):
    data = row.to_dict()
    keys = ['combined', 'values', 'id']
    for key in keys:
        data.pop(key)
    metadata = {}
    for k, v in data.items():
        metadata[k] = str(v) if not type(v) is str else v
    return metadata

def combine_embed(df):
    df['combined'] = df.apply(lambda row: f'NFL Season Year: {row["Year"]}, Week: {row["Week"]}, Game Date: {row["Date"]}, Team 1: {row["Team 1"]}, Team 1 Site Status: {row["Team 1 Site Status"]}, Team 2: {row["Team 2"]}, Team 2 Site Status: {row["Team 2 Site Status"]}', axis=1)
    df["values"] = df.combined.apply(lambda x: get_embedding(x, model=embedding_model))
    df['id'] = [uuid.uuid4().hex for _ in range(len(df.index))]
    df['metadata'] = df.apply(lambda row: create_metadata(row), axis=1)
    df.drop([
        'Week',
        'Year',
        'Date', 
        'Team 1', 
        'Team 1 Site Status',
        'Team 1 Record Overall',
        'Team 1 Record Away',
        'Score 1', 
        'Quarter Scores Team 1', 
        'Team 2', 
        'Team 2 Site Status',
        'Team 2 Record Overall',
        'Team 2 Record Home',
        'Score 2',
        'Quarter Scores Team 2',
        'Team 1 Box Score',
        'Team 2 Box Score',
        'combined'], inplace=True, axis=1)
    return df


def upsert_vector_db(df: pd.DataFrame):
    pc_index.upsert_from_dataframe(combine_embed(df))
    print('done upserting vector data')
