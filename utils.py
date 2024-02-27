from configs import pc_index

def delete_vectors():
    delete_response = pc_index.delete(deleteAll=True)
    return delete_response