from src.configuration.mongo_db_connection import MongoDBClient
from src.exception import MyException
from src.constants import COLLECTION_NAME
from typing import Optional
import pandas as pd
import numpy as np
class MongoDataFetcher:
    def __init__(self):
        try:
            self.connection=MongoDBClient()
        except Exception as e:
            raise MyException(e)
    def fetch_data_from_database(self,collection_name=COLLECTION_NAME):
        try:
            collection=self.connection.database[collection_name]
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(["_id"],axis=1,inplace=True)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise MyException(e)