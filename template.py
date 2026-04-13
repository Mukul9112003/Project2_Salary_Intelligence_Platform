import os
from pathlib import Path
program_name="src"
test_file="test"
list_of_files=[
    f"{program_name}/components/__init__.py",
    f"{program_name}/components/data_ingestion.py",
    f"{program_name}/pipeline/__init__.py",
    f"{program_name}/pipeline/training_pipeline.py",
    f"{program_name}/constants/__init__.py",
    f"{program_name}/logger/__init__.py",
    f"{program_name}/entity/__init__.py",
    f"{program_name}/entity/config_entity.py",
    f"{program_name}/entity/artifact_entity.py",
    f"{program_name}/configuration/__init__.py",
    f"{program_name}/configuration/mongo_db_connection.py",
    f"{program_name}/data_access/__init__.py",
    f"{program_name}/data_access/salary.py",
    f"{program_name}/exception/__init__.py",
    f"{program_name}/utils/__init__.py",
    f"{program_name}/utils/main_utils.py",
    f"config/Schema.yaml",
    f"config/Model.yaml",
    ".github/workflows/aws.yaml",
    "app.py",
    f"{test_file}/__init__.py",
    "dockerfile",
    "demo.py",
    "setup.py",
    "config/model.yaml",
    "config/schema.yaml",
]
for filepath in list_of_files:
    filepath=Path(filepath)
    filedir,filename=os.path.split(filepath)
    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
    if (not os.path.exists(filepath)) or os.path.getsize(filepath)==0:
        with open(filepath,"a") as file:
            pass
    else:
        print(f"File Exist by the name {filepath}")