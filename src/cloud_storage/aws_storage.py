from src.configuration.aws_connection import S3Client
from io import StringIO
from typing import Union
import os
from src.logger import logging
from mypy_boto3_s3.service_resource import Bucket
from src.exception import MyException
from botocore.exceptions import ClientError
from pandas import DataFrame, read_csv
import dill 
class SimpleStorageService:
    def __init__(self):
        s3_client = S3Client()
        self.s3_resource = s3_client.s3_resource
        self.s3_client = s3_client.s3_client
    def s3_key_path_available(self, bucket_name: str, s3_key: str) -> bool:
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = list(bucket.objects.filter(Prefix=s3_key))
            return len(file_objects) > 0
        except Exception as e:
            raise MyException(e)
    @staticmethod
    def read_object(object_name, decode: bool = True, make_readable: bool = False) -> Union[StringIO, bytes, str]:
        try:
            data = object_name.get()["Body"].read()
            if decode:
                data = data.decode()
            if make_readable:
                return StringIO(data)
            return data
        except Exception as e:
            raise MyException(e)
    def get_bucket(self, bucket_name: str) -> Bucket:
        try:
            return self.s3_resource.Bucket(bucket_name)
        except Exception as e:
            raise MyException(e)
    def get_file_object(self, filename: str, bucket_name: str):
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = list(bucket.objects.filter(Prefix=filename))
            if len(file_objects) == 0:
                raise Exception(f"No file found at {filename}")
            if len(file_objects) > 1:
                logging.warning(f"Multiple files found for {filename}, using first")

            return file_objects[0]
        except Exception as e:
            raise MyException(e)
    def load_model(self, model_name: str, bucket_name: str, model_dir: str = None):
        try:
            model_file = f"{model_dir}/{model_name}" if model_dir else model_name
            file_object = self.get_file_object(model_file, bucket_name)
            model_bytes = self.read_object(file_object, decode=False)
            model = dill.loads(model_bytes)  
            logging.info("Model loaded from S3 successfully")
            return model
        except Exception as e:
            raise MyException(e)
    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        try:
            self.s3_resource.Object(bucket_name, folder_name).load()
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                self.s3_client.put_object(Bucket=bucket_name, Key=f"{folder_name}/")
    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = False):
        try:
            logging.info(f"Uploading {from_filename} -> {to_filename}")
            self.s3_resource.meta.client.upload_file(from_filename,bucket_name,to_filename)
            logging.info("Upload successful")
            if remove:
                os.remove(from_filename)
                logging.info("Local file removed")
        except Exception as e:
            raise MyException(e)
    def upload_df_as_csv(self, data_frame: DataFrame, local_filename: str, bucket_filename: str, bucket_name: str):
        try:
            data_frame.to_csv(local_filename, index=False)
            self.upload_file(local_filename, bucket_filename, bucket_name)
        except Exception as e:
            raise MyException(e)
    def get_df_from_object(self, object_) -> DataFrame:
        try:
            content = self.read_object(object_, make_readable=True)
            return read_csv(content, na_values="na")
        except Exception as e:
            raise MyException(e)
    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:
        try:
            obj = self.get_file_object(filename, bucket_name)
            return self.get_df_from_object(obj)
        except Exception as e:
            raise MyException(e)