from pymongo import MongoClient
from pymongo.server_api import ServerApi


def get_client():
    return MongoClient(
        "mongodb+srv://goitlearnRos:1488228322@cluster0.6sa0kld.mongodb.net/?appName=Cluster0",
        server_api=ServerApi("1"),
    )

def insert_initial_data(db):
    return db.cats.insert_many(
        [
            {"name": "Heorhii", "age": 28, "features": ["beard", "dark", "cursing"]},
            {"name": "Sasha", "age": 32, "features": ["bald", "team lead", "shy"]},
            {"name": "Pasha", "age": 29, "features": ["cool", "friendly", "plays guitar"]},
        ]
    )
