from src.exception import MyException
from src.logger import logging
from src.constants import *
import os
from src.entity.estimator import MyModel
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import ModelTrainerArtifact,RegressionMetricArtifact,DataTransformationArtifact
from src.utils.main_utils import read_yaml_file,load_numpy_array,save_object,load_object,write_yaml_file
from xgboost import XGBRegressor
import numpy as np

from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
            self._ModelSchema=read_yaml_file(filepath=MODEL_SCHEMA_FILE_NAME)
        except Exception as e:
            raise MyException(e) from e
    def training_model(self,X_train,Y_train,X_test,Y_test):
        try:
            #parameter=self._ModelSchema["Best"]
            model=XGBRegressor() 
            model.fit(X_train,Y_train)
            Y_pred=model.predict(X_test)
            mean_squared_error_val=float(mean_squared_error(Y_test,Y_pred))
            mean_absolute_error_val=float(mean_absolute_error(Y_test,Y_pred))
            r2_score_val=float(r2_score(Y_test,Y_pred))
            metric=RegressionMetricArtifact(mean_absolute_error=mean_absolute_error_val,mean_squared_error=mean_squared_error_val,r2_score=r2_score_val)
            report= {
                "mean_absolute_error": mean_absolute_error_val,
                "mean_squared_error": mean_squared_error_val,
                "r2_score": r2_score_val
            }
            return model,metric,report
        except Exception as e:
            raise MyException(e) from e
    def Iniciate_Model_Trainer(self):
        try:
            X_train=load_object(self.data_transformation_artifact.trained_transformed_X_filepath)
            Y_train=load_object(self.data_transformation_artifact.trained_transformed_Y_filepath)
            logging.info("train data loaded successfully")
            X_test=load_object(self.data_transformation_artifact.tested_transformed_X_filepath)
            Y_test=load_object(self.data_transformation_artifact.tested_transformed_Y_filepath)
            Y_train = np.ravel(Y_train)
            Y_test = np.ravel(Y_test)
            logging.info("test data loaded successfully")
            model,metric,report=self.training_model(X_train=X_train,Y_train=Y_train,X_test=X_test,Y_test=Y_test)
            logging.info("model trained successfully")
            preprocessing=load_object(filepath=self.data_transformation_artifact.preprocessing_file_object_filepath)
            real_model=MyModel(preprocessing_object=preprocessing,model=model)
            file=os.path.join(self.model_trainer_config.model_trainer_metric_dir,"metric.yaml")
            dir_name=os.path.dirname(file)
            os.makedirs(dir_name,exist_ok=True)
            write_yaml_file(filepath=file,content=report)
            logging.info("metrics are saved  successfully")
            file=os.path.join(self.model_trainer_config.trained_model_path)
            dir_name=os.path.dirname(file)
            os.makedirs(dir_name,exist_ok=True)
            save_object(filepath=file,content=real_model)
            model_trainer_artifact=ModelTrainerArtifact(trained_model=self.model_trainer_config.trained_model_path,metric_artifact=metric)
            logging.info("model trainer artifact  successfully")
            return model_trainer_artifact
        except Exception as e:
            raise MyException(e) from e