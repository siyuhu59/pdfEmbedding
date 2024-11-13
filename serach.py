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
        embedding = np.frombuffer(vector_blob, dtype=np.float32)
        similarity = cosine_similarity([query_vector], [embedding])[0][0]
        similarities.append((id, similarity))
    
    # Find the most similar paragraph
    most_similar_id, _ = max(similarities, key=lambda x: x[1])
    result = db.select("SELECT clauses FROM legal_vectors WHERE id = ?", (most_similar_id,))
    return result[0][0] if result else None

if __name__ == "__main__":
    db = SQLiteManager('example.db')

    # Example usage
    query_text = "Your input paragraph here"
    most_similar_paragraph = get_most_similar_paragraph(query_text, db)
    print("Most similar paragraph clauses:", most_similar_paragraph)
