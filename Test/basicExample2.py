import json
import sqlite3
import sqlite_vss

def st_encode(x):
  result = model.encode([x])
  return json.dumps(result.tolist()[0])

conn = sqlite3.connect("hadithVSS.db")
conn.enable_load_extension(True)
sqlite_vss.load(conn)

cursor = conn.cursor()
searchQuery = st_encode('Search Text')


query = f"""
SELECT rowid
from
hadith_faiss
WHERE  vss_search(text, Vss_search_params('{searchQuery}', 2))
"""

cursor = conn.execute(query)
data = cursor.fetchall()
print(data)
conn.commit()
conn.close()