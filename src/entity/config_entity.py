import os
from dataclasses import dataclass,field
from src.constants import *
from datetime import datetime

@dataclass
class TrainingPipelineConfig:
    pipeline_name=PIPELINE_NAME
    artifact_path:str=field(init=False)
    def __post_init__(self):
        TIMESTAMP=datetime.today().strftime('%d_%m_%Y_%H_%M_%S')
        self.artifact_path=os.path.join(ARTIFACT_DIR,TIMESTAMP)
@dataclass
class DataIngestionConfig:
    training_pipeline_config:TrainingPipelineConfig
    data_ingestion_dir:str=field(init=False)
    feature_store:str=field(init=False)
    train_file_path:str=field(init=False)
    test_file_path:str=field(init=False)
    train_test_split_ratio:float=DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection:str=DATA_INGESTION_COLLECTION_NAME
    def __post_init__(self):
        self.data_ingestion_dir=os.path.join(self.training_pipeline_config.artifact_path,DATA_INGESTION_DIR_NAME)
        self.feature_store=os.path.join(self.data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,FILE_NAME)
        self.train_file_path=os.path.join(self.data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TRAIN_FILE_NAME)
        self.test_file_path=os.path.join(self.data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TEST_FILE_NAME)
@dataclass
class DataValidationConfig:
    training_pipeline_config:TrainingPipelineConfig
    data_validation_dir:str=field(init=False)
    validation_report_file_path:str=field(init=False)
    def __post_init__(self):
        self.data_validation_dir=os.path.join(self.training_pipeline_config.artifact_path,DATA_VALIDATION_DIR_NAME)
        self.validation_report_file_path=os.path.join(self.data_validation_dir,REPORT_FILE_PATH)