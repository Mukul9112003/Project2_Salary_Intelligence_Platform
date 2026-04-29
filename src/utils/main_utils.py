import yaml
import pandas as pd
import dill
import numpy as np
from src.exception import MyException
def read_yaml_file(filepath):
    try:
        with open(filepath,"r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise MyException(e) from e
def read_csv_file(filepath):
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        raise MyException(e) from e
def write_yaml_file(filepath,content):
    try:
        with open(filepath,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise MyException(e) from e
def save_object(filepath,content):
    try:
        with open(filepath,"wb") as file:
            dill.dump(content,file)
    except Exception as e:
        raise MyException(e) from e
def load_object(filepath):
    try:
        with open(filepath,"rb") as file:
            return dill.load(file)
    except Exception as e:
        raise MyException(e) from e
def save_numpy_array(filepath,content):
    try:
        np.save(filepath,content)
    except Exception as e:
        raise MyException(e) from e
def load_numpy_array(filepath):
    try:
        return np.load(filepath,allow_pickle=True)
    except Exception as e:
        raise MyException(e) from e