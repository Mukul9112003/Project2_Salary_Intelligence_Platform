import yaml
import pandas as pd
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