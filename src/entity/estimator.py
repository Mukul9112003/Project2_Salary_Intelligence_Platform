import pandas as pd
class MyModel:
    def __init__(self,preprocessing_object,model):
        self.preprocessing_object=preprocessing_object
        self.model=model
    def predict(self,dataframe:pd.DataFrame):
        transform_df=self.preprocessing_object.transform(dataframe)
        result=self.model.predict(transform_df)
        return result