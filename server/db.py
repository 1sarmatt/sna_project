# db.py
from pymongo import MongoClient
import os

client = MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017/"))
db = client["collab_editor"]

documents_collection = db["documents"]
