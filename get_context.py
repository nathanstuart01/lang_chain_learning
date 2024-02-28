import sys

from configs import pc_index, INDEX_NAMESPACES
from utils import get_embedding

def get_context(question: str, namespace: str, max_len: int = 3750, filters: dict = {}):
    q_embed = get_embedding(question)
    if filters:
        res = pc_index.query(namespace=namespace, vector=q_embed, top_k=48, include_metadata=True, filter=filters)
    else:
        res = pc_index.query(namespace=namespace, vector=q_embed, top_k=48, include_metadata=True)
    
    cur_len = 0
    contexts = []

    for row in res['matches']:
        import pdb;pdb.set_trace()
        text = row["metadata"]
        # this errors out
        # add in n_tokens or find a way to get the tokens??
        cur_len += row['metadata']['n_tokens'] + 4
        if cur_len < max_len:
            contexts.append(text)
        else:
            cur_len -= row['metadata']['n_tokens'] + 4
            if max_len - cur_len < 200:
                break
    return "\\\\n\\\\n###\\\\n\\\\n".join(contexts)

if __name__ == "__main__":
    context_question = sys.argv[1]
    if not context_question:
        raise ValueError("Context question cannot be blank")
    print('getting context for llm')
    get_context(context_question, INDEX_NAMESPACES['nfl']['reg_season'])
