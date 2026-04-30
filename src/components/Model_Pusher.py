import sys
import time
from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from src.entity.config_entity import ModelPusherConfig
from src.entity.s3_estimator import Proj1Estimator
class ModelPusher:
    def __init__(self,model_evaluation_artifact: ModelEvaluationArtifact,model_pusher_config: ModelPusherConfig):
        try:
            self.model_evaluation_artifact = model_evaluation_artifact
            self.model_pusher_config = model_pusher_config
            self.s3 = SimpleStorageService()
        except Exception as e:
            raise MyException(e) from e
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            logging.info("Entered ModelPusher")
            if not self.model_evaluation_artifact.is_model_accepted:
                logging.info("Model NOT accepted → skipping S3 upload")
                return ModelPusherArtifact(bucket_name=self.model_pusher_config.bucket_name,s3_model_path="None")
            timestamp = int(time.time())
            s3_model_path = f"model/{timestamp}/model.pkl"
            logging.info(f"Uploading model to S3 path: {s3_model_path}")
            proj1_estimator = Proj1Estimator(bucket_name=self.model_pusher_config.bucket_name,model_path=s3_model_path)
            proj1_estimator.save_model(from_file=self.model_evaluation_artifact.trained_model_path)
            model_pusher_artifact = ModelPusherArtifact(bucket_name=self.model_pusher_config.bucket_name,s3_model_path=s3_model_path)
            logging.info("Model successfully uploaded with versioning")
            return model_pusher_artifact
        except Exception as e:
            raise MyException(e) from e