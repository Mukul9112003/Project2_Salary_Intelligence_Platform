from src.logger import logging
from src.exception import MyException
import os
import pandas as pd
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.data_access.salary import MongoDataFetcher
from sklearn.model_selection import train_test_split
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise MyException(e) from e
    def export_data(self):
        try:
            my_data=MongoDataFetcher()
            df=my_data.fetch_data_from_database()
            dir_file=os.path.dirname(self.data_ingestion_config.feature_store)
            os.makedirs(dir_file,exist_ok=True)
            df.to_csv(self.data_ingestion_config.feature_store,index=False,header=True)
            logging.info("Data saved to feature store")
            return df
        except Exception as e:
            raise MyException(e) from e
    def split_train_test(self,df:pd.DataFrame):
        try:
            logging.info("Starting train-test split")
            train_df,test_df=train_test_split(df,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)
            dir_name=os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_name,exist_ok=True)
            train_df.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)
            logging.info(f"Train shape: {train_df.shape}, Test shape: {test_df.shape}")
        except Exception as e:
            raise MyException(e) from e
    def Iniciate_Data_Ingestion(self):
        df=self.export_data()
        logging.info("Data Ingestion Exporting data successfully")
        self.split_train_test(df)
        logging.info("Data Ingestion Train test split successfully")
        data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.train_file_path,tested_file_path=self.data_ingestion_config.test_file_path)
        logging.info("Data Ingestion Completed Successfully")
        return data_ingestion_artifact