import json

import pandas as pd

def upload_data_vector_db(df: pd.DataFrame):
    docs = df.to_json(orient='records')
    parsed_docs = json.loads(docs)
    import pdb;pdb.set_trace()
    #https://docs.pinecone.io/page/examples
    # use case would be to embed for search purposes
    # Search (where results are ranked by relevance to a query string)
    # start here use this example
    # I want to embed the text fields I will later search on for generating patterns from stats
    # combine Week Year Date Team 1 Team 1 Site Status Team 2 Team 2 Site Status into one text field
    # embed then once embeded add into 
