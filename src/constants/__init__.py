import os
from datetime import date
from from_root import from_root 
DATABASE_NAME="Project"
COLLECTION_NAME="Salary"
MONGODB_URL_KEY="MONGODB_URL"
PIPELINE_NAME=""
ARTIFACT_DIR="artifact"
CURRENT_YEAR=date.today().year
TARGET_COLUMN="salary"
FILE_NAME="data.csv"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"
REPORT_FILE_PATH="report.yaml"
SCHEMA_FILE_NAME=from_root("config/Schema.yaml")
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.25
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_COLLECTION_NAME:str="Salary"
DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_SCHEMA_FILE_PATH:str="config/schema.yaml"
TRAIN_X_FILE_NAME="train_x.npy"
TRAIN_Y_FILE_NAME="train_y.npy"
TEST_X_FILE_NAME="test_x.npy"
TEST_Y_FILE_NAME="test_y.npy"
DATA_TRANSFORMATION_DIR_NAME="data_tranformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR="data"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR="object"
PREPROCESSING_OBJECT_FILE_NAME="preprocessing.pkl"