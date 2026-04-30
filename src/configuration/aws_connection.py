import boto3
from src.logger import logging
from src.constants import AWS_ACCESS_KEY_ID_ENV_KEY,AWS_SECRET_ACCESS_KEY_ENV_KEY,REGION_NAME
from src.exception import MyException
import os
class S3Client:
    s3_client=None
    s3_resource=None
    def __init__(self,region_name=REGION_NAME):
        try:
            if S3Client.s3_client is None or S3Client.s3_resource is None:
                _access_key_id=os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
                _secrect_access_key=os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)
                if _access_key_id is None:
                    msg=f"Envirnment variable {AWS_ACCESS_KEY_ID_ENV_KEY} is not set"
                    logging.error(msg)
                    raise Exception(msg)
                if _secrect_access_key is None:
                    msg=f"Envirnment variable {AWS_ACCESS_KEY_ID_ENV_KEY} is not set"
                    logging.error(msg)
                    raise Exception(msg)
                S3Client.s3_resource=boto3.resource('s3',aws_access_key_id=_access_key_id,aws_secret_access_key=_secrect_access_key,region_name=region_name)
                S3Client.s3_client=boto3.client('s3',aws_access_key_id=_access_key_id,aws_secret_access_key=_secrect_access_key,region_name=region_name)
            self.s3_client=S3Client.s3_client
            self.s3_resource=S3Client.s3_resource
        except Exception as e:
            raise MyException(e) from e