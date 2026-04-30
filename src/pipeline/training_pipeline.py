from src.logger import logging
from src.exception import MyException
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.Model_trainer import ModelTrainer
from src.entity.config_entity import DataIngestionConfig,DataValidationConfig,TrainingPipelineConfig,DataTransformationConfig,ModelTrainerConfig
class TrainingPipeline:
    def __init__(self):
        self.pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.pipeline_config)
        self.data_validation_config=DataValidationConfig(training_pipeline_config=self.pipeline_config)
        self.data_transformation_config=DataTransformationConfig(training_pipeline_config=self.pipeline_config)
        self.model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.pipeline_config)
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
    def start_data_transformation(self,data_validation_artifact,data_ingestion_artifact):
        try:
            logging.info("Data Transformation started")
            data_transformation=DataTransformation(data_transformation_config=self.data_transformation_config,data_ingestion_artifact=data_ingestion_artifact,data_validation_artifact=data_validation_artifact)
            data_transformation_artifact=data_transformation.IniciateDataTransformation()
            logging.info("Data Transformation completed")
            return data_transformation_artifact
        except Exception as e:
            raise MyException(e) from e
    def start_model_trainer(self,data_transformation_artifact):
        try:
            logging.info("Model Training started")
            model_trainer=ModelTrainer(data_transformation_artifact=data_transformation_artifact,model_trainer_config=self.model_trainer_config)
            model_trainer_artifact=model_trainer.Iniciate_Model_Trainer()
            logging.info("Model Training completed")
            return model_trainer_artifact
        except Exception as e:
            raise MyException(e) from e
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,data_validation_artifact=data_validation_artifact)
            model_training_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
        except Exception as e:
            raise MyException(e) from e