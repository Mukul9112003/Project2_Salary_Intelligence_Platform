from dataclasses import dataclass
@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    tested_file_path:str
@dataclass
class DataValidationArtifact:
    status:bool
    message:str
    validation_report_file_path:str
@dataclass
class DataTransformationArtifact:
    trained_transformed_X_filepath:str
    trained_transformed_Y_filepath:str
    tested_transformed_X_filepath:str
    tested_transformed_Y_filepath:str
    preprocessing_file_object_filepath:str