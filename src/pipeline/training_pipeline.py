from src.components.data_ingestion import DataIngestion
from src.logger import logging
from src.exception import MyException
from src.components.data_validation import DataValidation
from src.entity.config_entity import DataIngestionConfig,DataValidationConfig,TrainingPipelineConfig
class TrainingPipeline:
    def __init__(self):
        self.pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.pipeline_config)
        self.data_validation_config=DataValidationConfig(training_pipeline_config=self.pipeline_config)
    def start_data_ingestion(self):
        try:
            logging.info("Data ingestion started")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.Iniciate_Data_Ingestion()
            logging.info("Data ingestion completed")
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e) from e
    def start_data_validation(self,data_ingestion_artifact):
        try:
            logging.info("Data validation started")
            data_validation=DataValidation(data_validation_config=self.data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact=data_validation.Iniciate_Data_Validation()
            logging.info("Data validation completed")
            return data_validation_artifact
        except Exception as e:
            raise MyException(e) from e
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise MyException(e) from e