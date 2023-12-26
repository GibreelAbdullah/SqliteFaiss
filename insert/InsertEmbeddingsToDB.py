import json
from common.generateEmbeddingsMpnet import generate_embeddings
# from common.generateEmbeddingsBert import generate_embeddings

def insert_embeddings_to_db(cur, text):

    embeddings = generate_embeddings(text)

    # Insert into data table example data and get rowid
    cur.execute("""
        INSERT INTO hadith(text)
        VALUES (?)
    """, (text,))
    rowid = cur.lastrowid


    # Insert actual embeddings, associate it with rowid of data table
    cur.execute("""
        INSERT INTO hadith_faiss(
            rowid, embeddings
        )
        VALUES (?, ?)
    """, (rowid, json.dumps(embeddings)))
