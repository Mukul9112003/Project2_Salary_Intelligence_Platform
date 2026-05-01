from src.exception import MyException
from src.logger import logging
import numpy as np
import pandas as pd
import os
from ast import literal_eval
from sklearn.preprocessing import FunctionTransformer
from src.utils.main_utils import read_yaml_file,read_csv_file,save_object,save_numpy_array
from src.constants import SCHEMA_FILE_NAME,TARGET_COLUMN
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.pipeline import Pipeline
from category_encoders import TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from scipy.sparse import hstack,csr_matrix
class MeraTransformer(BaseEstimator,TransformerMixin):
    def __init__(self):
        self.config=read_yaml_file(filepath=SCHEMA_FILE_NAME)
    def fit(self,X,Y=None):
        return self
    def transform(self,X,y=None):
        if "job_posted_date" in X.columns:
            X["job_posted_date"] = pd.to_datetime(X["job_posted_date"], errors="coerce")
            X["month"]=X["job_posted_date"].dt.month
            X["quarter"]=X["job_posted_date"].dt.quarter
        X["job_schedule_type"]=X["job_schedule_type"].fillna("Unknown")
        def extract_level(title):
            title = str(title).lower()
            if "senior" in title:
                return "senior"
            elif "junior" in title:
                return "junior"
            elif "lead" in title:
                return "lead"
            else:
                return "mid"
        X["seniority"]=X["job_title"].apply(extract_level)
        cols = ["job_work_from_home","job_no_degree_mention","job_health_insurance"]
        X[cols]=X[cols].astype(int)
        from ast import literal_eval
        def clean_skills(x):
            try:
                if isinstance(x, list):
                    return " ".join(x)
                elif isinstance(x, str) and x.startswith("["):
                    return " ".join(literal_eval(x))
                elif isinstance(x, str):
                    return x
                else:
                    return ""
            except:
                return ""

        X["job_skills"] = X["job_skills"].apply(clean_skills)
        X = X.drop(columns=[c for c in ["job_via","search_location","job_posted_date"] if c in X.columns])
        return X
class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact
        except Exception as e:
            raise MyException(e) from e
    def preprocessing_start(self):
        try:
            preprocessing=Pipeline(steps=[
                ("mera",MeraTransformer()),
                ("category_handling",ColumnTransformer(transformers=[
                    ("cat",OneHotEncoder(handle_unknown="ignore"),["job_title_short","job_schedule_type","seniority","quarter"]),
                    ("target",TargetEncoder(),["company_name","job_country","job_location"]),
                    ("text", Pipeline([("selector", FunctionTransformer(lambda x: x.iloc[:,0], validate=False)),("tfidf", TfidfVectorizer(max_features=100))]), ["job_skills"])
                    ],remainder="drop")
                    )
                    ])
            return preprocessing
        except Exception as e:
            raise MyException(e) from e
    def IniciateDataTransformation(self):
        try:
            if self.data_validation_artifact.status:
                train=read_csv_file(self.data_ingestion_artifact.trained_file_path)
                test=read_csv_file(self.data_ingestion_artifact.tested_file_path)
                logging.info("train and test data load successfully from data ingestion artifact ")
                X_train,y_train=train.drop(columns=[TARGET_COLUMN],axis=1),train[TARGET_COLUMN]
                X_test,y_test=test.drop(columns=[TARGET_COLUMN],axis=1),test[TARGET_COLUMN]
                preprocessing=self.preprocessing_start()
                preprocessing.fit(X_train,y_train)
                logging.info("Preprocessing object made successfully")
                X_transformed_train=preprocessing.transform(X_train)
                X_transformed_test=preprocessing.transform(X_test)
                X_transformed_train=X_transformed_train.toarray()
                X_transformed_test=X_transformed_test.toarray()
                dir_name=os.path.dirname(self.data_transformation_config.preprocessing_object_file_path)
                os.makedirs(dir_name,exist_ok=True)
                save_object(filepath=self.data_transformation_config.preprocessing_object_file_path,content=preprocessing)
                logging.info("Preprocessing object is store successfully")
                dir_name=os.path.dirname(self.data_transformation_config.transformed_train_X_file_path)
                os.makedirs(dir_name,exist_ok=True)
                save_numpy_array(filepath=self.data_transformation_config.transformed_train_X_file_path,content=X_transformed_train)
                save_numpy_array(filepath=self.data_transformation_config.transformed_train_Y_file_path,content=y_train)
                logging.info("Transformed train array is store successfully")
                save_numpy_array(filepath=self.data_transformation_config.transformed_test_X_file_path,content=X_transformed_test)
                save_numpy_array(filepath=self.data_transformation_config.transformed_test_Y_file_path,content=y_test)
                logging.info("Transformed test array is store successfully")
                data_transformation_artifact=DataTransformationArtifact(trained_transformed_X_filepath=self.data_transformation_config.transformed_train_X_file_path,
                                                                        trained_transformed_Y_filepath=self.data_transformation_config.transformed_train_Y_file_path,
                                                                        tested_transformed_X_filepath=self.data_transformation_config.transformed_test_X_file_path,
                                                                        tested_transformed_Y_filepath=self.data_transformation_config.transformed_test_Y_file_path,
                                                                        preprocessing_file_object_filepath=self.data_transformation_config.preprocessing_object_file_path)
                return data_transformation_artifact
        except Exception as e:
            raise MyException(e) from e
