import sys
import pandas as pd
from src.entity.s3_estimator import Proj1Estimator
from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import MyException
class PredictionPipeline:
    def __init__(self):
        try:
            self.bucket_name = "salary-bucket-1"  
            self.s3 = SimpleStorageService()
            self.model_path = self.get_latest_model_path()
            self.estimator = Proj1Estimator(bucket_name=self.bucket_name,model_path=self.model_path)
        except Exception as e:
            raise MyException(e)
    def get_latest_model_path(self):
        try:
            bucket = self.s3.get_bucket(self.bucket_name)
            objects = list(bucket.objects.filter(Prefix="model/"))
            if len(objects) == 0:
                raise Exception("No model found in S3")
            paths = [obj.key for obj in objects if obj.key.endswith("model.pkl")]
            latest = sorted(paths, reverse=True)[0]
            print(f"Latest model path: {latest}")
            return latest
        except Exception as e:
            raise MyException(e)
    def predict(self, data: dict):
        try:
            df = pd.DataFrame([data])
            prediction = self.estimator.predict(df)
            return int(prediction)
        except Exception as e:
            raise MyException(e)