from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from src.pipeline.prediction_pipeline import PredictionPipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
pipeline = PredictionPipeline()

class SalaryRequest(BaseModel):
    job_title: str
    job_title_short: str
    job_location: str
    job_country: str
    company_name: str
    job_schedule_type: str
    job_work_from_home: int
    job_no_degree_mention: int
    job_health_insurance: int
    job_skills: str   # "python sql ml"
    job_posted_date: str  # "2023-08-01"


@app.get("/")
def home():
    return {"message": "Salary Prediction API Running "}


@app.post("/predict")
def predict(data: SalaryRequest):
    try:
        input_dict = data.dict()
        prediction = pipeline.predict(input_dict)
        return {
            "predicted_salary": float(prediction)
        }
    except Exception as e:
        return {"error": str(e)}