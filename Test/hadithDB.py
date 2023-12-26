#DELETE THE DB FILE BEFORE RUNNING. It WILL BE RECREATED.
import json
import sqlite3
import sqlite_vss
import fasttext


editionsFile = open("../hadith-api/editions.json", "r", encoding="utf-8")
editionsData = json.load(editionsFile)
collectionDict = []

for collectionList, collectionListDetails in editionsData.items():
    for collection in collectionListDetails["collection"]:
        collectionDict.append(
            {"name": collection["name"], "language": collection["name"][:3]}
        )

# # Remove Later
# collectionDict = [{
#     "name": "eng-malik", "language" : "ara"
# }]

conn = sqlite3.connect("hadithVSS.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS hadith (hadithnumber integer,arabicnumber integer,text text,grades text,bookNumber integer,bookhadith integer,bookname text,language text,shortname text);")
cursor.execute("CREATE TABLE IF NOT EXISTS hadith_rowid_map (hadith_url text);")

collectionsFile = open("../hadith-api/updates/collections/collections.min.json")
collectionsData = json.load(collectionsFile)
collectionShortNameDict = {}
for collectionFileNameObject in collectionsData["collections"]:
    collectionShortNameDict[collectionFileNameObject["eng-name"]] = collectionFileNameObject["name"]
    

for collectionDetails in collectionDict:
    print(collectionDetails["name"])
    inputFile = open(
        "../hadith-api/editions/" + collectionDetails["name"] + ".json",
        # "../hadith-api/editions/ara-muslim.json",
        "r",
        encoding="utf-8",
    )
    data = json.load(inputFile)

    for hadith in data["hadiths"]:
        value = None
        if 'arabicnumber' in hadith.keys():
            value = hadith["arabicnumber"]
        gradings = ""
        for grades in hadith["grades"]:
            gradings = gradings + grades["name"] + "::" + grades["grade"] + " && "
        if(gradings.endswith(" && ")):
            gradings = gradings[:-4]
        cursor.execute(
            f"""INSERT INTO hadith
            (hadithnumber,arabicnumber,text,grades,bookNumber,bookhadith,bookname,language,shortname)
            VALUES(?,?,?,?,?,?,?,?,?);""",
            (
                hadith["hadithnumber"],value,hadith["text"],gradings,hadith["reference"]["book"],hadith["reference"]["hadith"],data["metadata"]["name"],collectionDetails["language"],collectionShortNameDict[data["metadata"]["name"]]
            ),
        )
    print("complete")



cursor.execute("CREATE TABLE IF NOT EXISTS hadith_rowid_map (hadith_url text);")
cursor.execute("INSERT INTO hadith_rowid_map(rowid,hadith_url) select rowid, language|| '-' || shortname || ':' || hadithnumber from hadith")

conn.enable_load_extension(True)
sqlite_vss.load(conn)

model = fasttext.load_model("eng-malik.bin")

cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS hadith_faiss USING vss0( text(384));")

cursor.execute("SELECT rowid, text from hadith;")
data = cursor.fetchall()

for row in data:
    cursor.execute(f"INSERT INTO hadith_faiss(rowid,text) values ('{row[0]}','{model[row[1]]}')")

conn.commit()
conn.close()