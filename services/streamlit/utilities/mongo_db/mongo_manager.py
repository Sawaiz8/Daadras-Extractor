from pymongo import MongoClient
from typing import List, Dict
from datetime import datetime
import os
from datetime import datetime, timedelta


class MongoDBManager:
    def __init__(self, uri=os.getenv("MONGO_URL"), db_name=os.getenv("MONGO_INITDB_DATABASE")):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None
        self.student_data_collection = None
        self.volunteer_data_collection = None
        self.sessions_data_collection = None

    def connect(self):
        # Connect to MongoDB
        self.client = MongoClient(self.uri)
        # Access the database
        self.db = self.client[self.db_name]
        self.student_data_collection = self.db["students_data"]
        self.volunteer_data_collection = self.db["volunteers_data"]
        self.sessions_data_collection = self.db["sessions_data"]
        
    def disconnect(self)-> None:
        if self.client:
            self.client.close()
        self.client = None
        self.db = None
        self.student_data_collection = None
        self.volunteer_data_collection = None
        self.sessions_data_collection = None
        
    def db_connection(func):
        async def wrapper(self, *args, **kwargs):
            self.connect()
            try:
                result = await func(self, *args, **kwargs)
            finally:
                self.disconnect()
            return result
        return wrapper

    @db_connection
    async def upsert_student_data(self, student_data) -> None:
        # Get the current max student_id and increment by 1
        max_student = self.student_data_collection.find_one(
            sort=[("student_id", -1)]
        )
        next_id = 1 if max_student is None else max_student["student_id"] + 1
        
        # Set the auto-generated ID
        student_data["student_id"] = next_id
        
        self.student_data_collection.update_one(
            {"student_id": student_data["student_id"]},
            {"$set": student_data},
            upsert=True
        )

    @db_connection
    async def upsert_volunteer_data(self, volunteer_data: Dict) -> None:
        # Get the current max volunteer_id and increment by 1
        max_volunteer = self.volunteer_data_collection.find_one(
            sort=[("volunteer_id", -1)]
        )
        next_id = 1 if max_volunteer is None else max_volunteer["volunteer_id"] + 1
        
        # Set the auto-generated ID
        volunteer_data["volunteer_id"] = next_id
        
        self.volunteer_data_collection.update_one(
            {"volunteer_id": volunteer_data["volunteer_id"]},
            {"$set": volunteer_data},
            upsert=True
        )
    
    @db_connection
    async def upsert_session_data(self, session_data: Dict) -> None:
        # Get the current max session_id and increment by 1
        max_session = self.sessions_data_collection.find_one(
            sort=[("session_id", -1)]
        )
        next_id = 1 if max_session is None else max_session["session_id"] + 1
        
        # Set the auto-generated ID
        session_data["session_id"] = next_id
        
        self.sessions_data_collection.update_one(
            {"session_id": session_data["session_id"]},
            {"$set": session_data},
            upsert=True
        )
    
    @db_connection
    async def get_all_session_names(self) -> List[str]:
        session_names = list(self.sessions_data_collection.distinct("session_name"))
        return session_names if session_names else []


