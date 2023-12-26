import sqlite_vss
import sqlite3
import json

# Dummy data. just for example
text = "hello world"
embeddings = [0.1, 0.2, 0.3]
embeddings_to_search = [0.2, 0.3, 0.4]

# Initiate sqlite with sqlite-vss
conn = sqlite3.connect('db.sqlite')
conn.enable_load_extension(True)
cur = conn.cursor()
sqlite_vss.load(conn)


# Create virtual table with text_embedding column which has vectors of size 3
cur.executescript("""
    CREATE VIRTUAL TABLE IF NOT EXISTS vss_post USING vss0(
        embeddings(3)
    );
    CREATE TABLE IF NOT EXISTS post(
        id INTEGER PRIMARY KEY,
        text TEXT
    );
""")

# Insert into data table example data and get rowid
cur.execute("""
    INSERT INTO post(text)
    VALUES (?)
""", (text,))
rowid = cur.lastrowid


# Insert actual embeddings, associate it with rowid of data table
cur.execute("""
    INSERT INTO vss_post(
        rowid, embeddings
    )
    VALUES (?, ?)
""", (rowid, json.dumps(embeddings)))

conn.commit()

# Search in virtual table to get rowid which we will use to get the data assicated in rowid
cur.execute("""
SELECT rowid
FROM vss_post
WHERE vss_search(
    embeddings,
    vss_search_params(?, 1)
)
LIMIT 1
""", (json.dumps(embeddings),))

# We should get here the row ID which is similar to vectors_to_search value
result = cur.fetchone()
print(result)

# Close database and cursor
cur.close()
conn.close()