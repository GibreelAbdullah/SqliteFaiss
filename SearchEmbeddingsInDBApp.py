import json
from common.generateEmbeddingsMpnet import generate_embeddings
import sqlite_vss
import sqlite3

def search_embedded_data_in_db(conn, text):
    cur = conn.cursor()
    embeddings = generate_embeddings(text)

    cur.execute("""
    SELECT rowid, distance
    FROM hadith_faiss
    WHERE vss_search(
        embeddings,
        vss_search_params(?, 20)
    )
    LIMIT 100
    """, (json.dumps(embeddings),))

    # We should get here the row ID which is similar to vectors_to_search value
    result = cur.fetchall()
    for row in result:
        print(row)
    return result



if __name__ == "__main__":
    conn = sqlite3.connect('db_mpnet.sqlite')
    conn.enable_load_extension(True)
    sqlite_vss.load(conn)

    cur = conn.cursor()
    search_embedded_data_in_db(conn, """Abdullah ibn Ubaydullah""")