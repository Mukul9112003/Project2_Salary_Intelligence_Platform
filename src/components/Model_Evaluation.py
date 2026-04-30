import sys
import os
import pandas as pd
import mlflow
import mlflow.sklearn
from dataclasses import dataclass
from typing import Optional
from sklearn.metrics import r2_score
from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import ModelTrainerArtifact,DataIngestionArtifact,ModelEvaluationArtifact
from src.exception import MyException
from src.constants import TARGET_COLUMN,MLFLOW_TRACKING_URI
from src.logger import logging
from src.utils.main_utils import load_object,write_yaml_file
from src.entity.s3_estimator import Proj1Estimator
@dataclass
class EvaluateModelResponse:
    trained_model_r2_score: float
    best_model_r2_score: float
    is_model_accepted: bool
    difference: float
class ModelEvaluation:
    def __init__(self,model_eval_config: ModelEvaluationConfig,data_ingestion_artifact: DataIngestionArtifact,model_trainer_artifact: ModelTrainerArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise MyException(e) from e
    def get_best_model(self):
        try:
            bucket = self.model_eval_config.bucket_name
            path = self.model_eval_config.s3_model_key_path
            estimator = Proj1Estimator(bucket_name=bucket,model_path=path)
            if estimator.is_model_present(model_path=path):
                return estimator
            return None
        except Exception as e:
            raise MyException(e) from e
    def evaluate_model(self):
        try:
            test_df = pd.read_csv(self.data_ingestion_artifact.tested_file_path)
            X = test_df.drop(TARGET_COLUMN, axis=1)
            y = test_df[TARGET_COLUMN]
            logging.info("Loaded test data")
            trained_model = load_object(filepath=self.model_trainer_artifact.trained_model)
            y_pred_trained=trained_model.predict(X)
            trained_r2 = float(r2_score(y, y_pred_trained))
            logging.info(f"Trained Model r2: {trained_r2}")
            best_model = self.get_best_model()
            best_r2 =0.0
            best_threshold = None
            if best_model is not None:
                logging.info("Evaluating production model")
                y_pred_best=best_model.predict(X)
                best_r2 = float(r2_score(y, y_pred_best))
                logging.info(f"Production Model F1: {best_r2}")
                logging.info(f"Production Model Threshold: {best_threshold}")
            baseline = 0 if best_r2 is None else best_r2
            is_accepted = trained_r2 > baseline
            response = EvaluateModelResponse(trained_model_r2_score=trained_r2,best_model_r2_score=best_r2,is_model_accepted=is_accepted,difference=trained_r2 - baseline)
            logging.info(f"Evaluation Result: {response}")
            return response, trained_model
        except Exception as e:
            raise MyException(e) from e
    def initiate_model_evaluation(self):
        try:
            logging.info("Starting Model Evaluation...")
            response, trained_model = self.evaluate_model()
            s3_path = self.model_eval_config.s3_model_key_path
            if response.is_model_accepted:
                logging.info("Model ACCEPTED")
                tracking_uri = os.getenv("MLFLOW_TRACKING_URI", MLFLOW_TRACKING_URI)
                mlflow.set_tracking_uri(tracking_uri)
                mlflow.set_experiment("churn_prediction")

                with mlflow.start_run():

                    mlflow.log_metric("trained_f1", response.trained_model_r2_score)
                    mlflow.log_metric("best_f1", response.best_model_r2_score or 0)
                    mlflow.log_metric("difference", response.difference)
                    mlflow.log_param("status", "accepted")
                    mlflow.sklearn.log_model(trained_model, name="model")
            else:
                logging.info("Model REJECTED — skipping MLflow + S3")
            dirname=os.path.dirname(self.model_eval_config.result)
            os.makedirs(dirname,exist_ok=True)
            report={
                "is_model_accepted":response.is_model_accepted,
                "changed_accuracy":response.difference
            }
            write_yaml_file(filepath=self.model_eval_config.result,content=report)
            artifact = ModelEvaluationArtifact(is_model_accepted=response.is_model_accepted,s3_model_path=s3_path,trained_model_path=self.model_trainer_artifact.trained_model,changed_accuracy=response.difference)
            return artifact
        except Exception as e:
            raise MyException(e) from e