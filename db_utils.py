from pymongo import MongoClient
from dotenv import load_dotenv
import pymongo
import os

load_dotenv()

mongo_uri = os.getenv("mongo")

client  = MongoClient(mongo_uri)
db      = client.get_database(os.getenv("db_name"))
collection = db.get_collection("news")

def update_data(url,date):
    
    data = {
        "url" : url,
        "date" : date
    }

    collection.insert_one(data)
    

update_data("test_url", "dd/mm/yyyy")