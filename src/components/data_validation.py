from src.logger import logging
from src.exception import MyException
import pandas as pd
import os
from src.constants import SCHEMA_FILE_NAME
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact
from src.utils.main_utils import read_yaml_file,read_csv_file,write_yaml_file
class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self._Schema_file_path=read_yaml_file(filepath=SCHEMA_FILE_NAME)
        except Exception as e:
            raise MyException(e) from e
    def validate_column(self,df):
        try:
            status=True
            message=[]
            expected_output=self._Schema_file_path["column"]
            if len(expected_output.keys())!=len(df.columns):
                status=False
                msg=f"number of column are not eqaul to expected column"
                logging.error(msg)
                message.append(msg)
            if list(df.columns)!=list(expected_output.keys()):
                status=False
                msg=f"Some columns are missing from expected column"
                logging.error(msg)
                message.append(msg)
            for col,excepted in expected_output.items():
                if col not in df.columns:
                    status=False
                    msg=f"{col} is not present is dataframe "
                    logging.error(msg)
                    message.append(msg)
                    continue
                Series=df[col]
                if excepted=="object":
                    invalid=Series.dropna().apply(lambda x:not isinstance(x,str))
                    if invalid.any():
                        status=False
                        msg=f"{col} is not all values are object or string in dataframe "
                        logging.error(msg)
                        message.append(msg)
                        continue
                elif excepted=="int":
                    converted=pd.to_numeric(Series,errors="coerce")
                    invalid=converted.isna() & Series.notna()
                    non_integer=(converted % 1 !=0) & converted.notna()
                    if invalid.any() or non_integer.any():
                        status=False
                        msg=f"{col} is not values are integer in dataframe "
                        logging.error(msg)
                        message.append(msg)
                        continue
                elif excepted=="float":
                    converted=pd.to_numeric(Series,errors="coerce")
                    invalid=converted.isna() & Series.notna()
                    if invalid.any():
                        status=False
                        msg=f"{col} is not all values are float in dataframe "
                        logging.error(msg)
                        message.append(msg)
                        continue
                elif excepted=="datetime":
                    converted=pd.to_datetime(Series,errors="coerce")
                    invalid=converted.isna() & Series.notna()
                    if invalid.any():
                        status=False
                        msg=f"{col} is not all values are datetime in dataframe "
                        logging.error(msg)
                        message.append(msg)
                        continue
                elif excepted == "bool":
                    converted = Series.map(lambda x: True if str(x).lower() in ["true", "1", "yes"] else False if str(x).lower() in ["false", "0", "no"] else None)

                    invalid = converted.isna() & Series.notna()

                    if invalid.any():
                        status = False
                        msg = f"{col} has non-boolean values in dataframe"
                        logging.error(msg)
                        message.append(msg)
                        continue
                else:
                    logging.warning(f"{col} unexpected column is present ")
            return status,message
        except Exception as e:
            raise MyException(e) from e
    def Iniciate_Data_Validation(self):
        try:
            train=read_csv_file(filepath=self.data_ingestion_artifact.trained_file_path)
            logging.info("Trained data loaded ")
            test=read_csv_file(filepath=self.data_ingestion_artifact.tested_file_path)
            logging.info("Tested data loaded")
            train_status,train_message=self.validate_column(train)
            logging.info("Trainig data validation done ")
            test_status,test_message=self.validate_column(test)
            logging.info("Testing data validation done ")
            status_all=train_status and test_status
            message=train_message+test_message
            dir_name=os.path.dirname(self.data_validation_config.validation_report_file_path)
            os.makedirs(dir_name,exist_ok=True)
            report={
                "status":status_all,
                "message":message
            }
            write_yaml_file(filepath=self.data_validation_config.validation_report_file_path,content=report)
            data_validation_artifact=DataValidationArtifact(status=status_all,message=message,validation_report_file_path=self.data_validation_config.validation_report_file_path)
            return data_validation_artifact
        except Exception as e:
            raise MyException(e) from e