import sqlite_vss
import sqlite3


conn = sqlite3.connect('db.sqlite')
conn.enable_load_extension(True)
cur = conn.cursor()
sqlite_vss.load(conn)


cur.execute("""
SELECT *
FROM hadith_faiss""")

# We should get here the row ID which is similar to vectors_to_search value
result = cur.fetchall()
print(result)