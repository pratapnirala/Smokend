from pymongo import MongoClient
from config import config

client = MongoClient(config.config.mongodb_uri)
db = client[config.config.mongodb_db]
users_collection = db["userCollection"]
print("MongoDB connected:", db.name)
