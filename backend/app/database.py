import os 
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME" , "jobassistant")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is missing from the .env file")

client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=10000,
)


database = client[DATABASE_NAME]

resumes_collection = database['resumes']



def check_database_connection():
    client.admin.command("ping")
    return True

