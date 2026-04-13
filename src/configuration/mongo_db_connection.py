import pymongo
import os
from src.constants import DATABASE_NAME,MONGODB_URL_KEY
from src.logger import logging
from src.exception import MyException
import certifi
ca=certifi.where()
class MongoDBClient:
    client=None
    def __init__(self,database_name=DATABASE_NAME):
        try:
            if MongoDBClient.client is None:
                mongo_db_url=os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Envirnment variable {MONGODB_URL_KEY} is not set")
                MongoDBClient.client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
                self.client=MongoDBClient.client
                self.database=self.client[database_name]
                self.database_name=database_name
                logging.info("MongoDB connected successfully")
        except Exception as e:
            raise MyException(e)