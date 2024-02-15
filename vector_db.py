import json

import pandas as pd

def upload_data_vector_db(df: pd.DataFrame):
    docs = df.to_json(orient='records')
    parsed_docs = json.loads(docs)
    #https://docs.pinecone.io/page/examples
    # next step is here
