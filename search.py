from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from FlagEmbedding import BGEM3FlagModel
from sqliteController import SQLiteManager

# Initialize embedding model
model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)

def get_vector(text):
    # Generate vector for a given text
    embedding = model.encode([text])['dense_vecs'][0]
    return embedding

def get_most_similar_paragraph(query_text, db):
    # Get vector representation of the input paragraph
    query_vector = get_vector(query_text)
    
    # Retrieve all vectors from the database
    rows = db.select("SELECT id, vector FROM legal_vectors")
    
    # Calculate cosine similarity for each vector
    similarities = []
    for row in rows:
        id, vector_blob = row
        embedding = np.frombuffer(vector_blob, dtype=np.float16)
        similarity = cosine_similarity([query_vector], [embedding])[0][0]
        similarities.append((id, similarity))
    
    # Find the most similar paragraph
    most_similar_id, _ = max(similarities, key=lambda x: x[1])
    result = db.select("SELECT clauses FROM legal_vectors WHERE id = ?", (most_similar_id,))
    return result[0][0] if result else None

if __name__ == "__main__":
    db = SQLiteManager('example.db')

    # Example usage
    query_text = "제1항에도 불구하고 위탁자가 신탁재산을 실질적으로 통제하는 등 대통령령으로 정하는 요건을 충족하는 신탁의 경우에는 그 신탁재산에 귀속되는 소득은 위탁자에게 귀속되는 것으로 본다."
    most_similar_paragraph = get_most_similar_paragraph(query_text, db)
    print("Most similar paragraph clauses:", most_similar_paragraph)
