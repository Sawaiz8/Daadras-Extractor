from utilities.mongo_db.mongo_manager import MongoDBManager
import os

mongo_store = MongoDBManager(os.getenv("MONGO_URL"), os.getenv("MONGO_INITDB_DATABASE"))



