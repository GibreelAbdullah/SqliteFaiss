import json
import sqlite3
import sqlite_vss

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def st_encode(x):
  result = model.encode([x])
  return json.dumps(result.tolist()[0])

conn = sqlite3.connect("hadithVSS.db")
conn.enable_load_extension(True)
sqlite_vss.load(conn)

cursor = conn.cursor()
searchQuery = st_encode('Search Text')


query = f"""
with matches as (SELECT rowid, distance
from
hadith_faiss
WHERE  vss_search(text, Vss_search_params('{searchQuery}', 2))
)
SELECT hadith.text, matches.distance
from matches
left join hadith on hadith.rowid = matches.rowid
"""

# query = f"""
# SELECT  'vss_search(text, Vss_search_params({searchQuery}, 2))' from
# hadith_faiss as ssdff
# """

cursor = conn.execute(query)
data = cursor.fetchall()
print(data)
conn.commit()
conn.close()