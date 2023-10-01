from pymongo import MongoClient
from bson.objectid import ObjectId
  
class DataSource:
    def __init__(self, db_string):
        self.client:MongoClient = MongoClient(db_string)
        if self.client == None:
            raise Exception("Error connecting to database server.")
        
    def get_database(self, db):
        if self.client != None:
            return self.client[db]
        else:
            raise Exception("Database server not connected.")
    def search_database(self, db, search_string):
        self.client:MongoClient
        if self.client != None:

            query_object = {"name": {"$regex" : f"(?i){search_string}"}}
            search_results = self.client[db]["frequencies"].find(query_object)
            return search_results
        else:
            raise Exception("Database server not connected")
        
    def store_record(self, db, record):
        self.client:MongoClient
        if self.client != None:
            self.client[db]["frequencies"].insert_one(record)
        else:
            raise Exception("Database server not connected")
        
    def delete_record(self, db, record_id):
        #print(f"ID: {record_id}")
        self.client:MongoClient
        if self.client != None:
            print(self.client[db]["frequencies"].delete_one({"_id":  record_id} ).raw_result   )
        else:
            raise Exception("Database server not connected")
    
    def update_record(self, db, record_id, fields):
        self.client:MongoClient
        if self.client != None:
            self.client[db]["frequencies"].update_one({"_id": record_id}, fields)
        else:
            raise Exception("Database server not connected")
        
    def login(self, db, id, pw):
        self.client:MongoClient
        if self.client != None:

            query_object = {"uid": f"{id}"}
            search_results = self.client[db]["users"].find_one(query_object)
            #print(f"{search_results}, {pw}, {id}")
            if search_results != None and  search_results["password"] == pw:
                return True
            else:
                return False
        else:
            raise Exception("Database server not connected")