from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)

# Database = quiz  (already from URI)
db = client.get_database()

# Access collections directly

users = db["users"]
counter = db["counter"]

def get_next_reg_number():
    doc = counter.find_one_and_update(
        {"_id": "reg_number"},
        {"$inc": {"value": 1}},
        upsert=True,
        return_document=True
    )
    return f"SWAP{doc['value']:03d}"


def reset_counter():
    counter.update_one({"_id": "reg_number"}, {"$set": {"value": 0}}, upsert=True)


def save_registration(data):
    users.insert_one(data)
