from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json

client = MongoClient(
    "mongodb+srv://goitlearnRos:1488228322@cluster0.6sa0kld.mongodb.net/?appName=Cluster0",
    server_api=ServerApi("1"),
)

db = client.Task_2# create DB Task_2

authors_collection = db.authors #create author
quotes_collection = db.quotes #create text

with open("authors.json", "r", encoding="utf-8") as f:
    authors_data = json.load(f)

with open("quotes.json", "r", encoding="utf-8") as f:
    quotes_data = json.load(f)

authors_collection.delete_many({}) #script multiple usage 
quotes_collection.delete_many({}) #script multiple usage 

if authors_data:
    result_authors = authors_collection.insert_many(authors_data)
    print(f"Inserted authors: {len(result_authors.inserted_ids)}")

if quotes_data:
    result_quotes = quotes_collection.insert_many(quotes_data)
    print(f"Inserted quotes: {len(result_quotes.inserted_ids)}")

print("DONE!")
