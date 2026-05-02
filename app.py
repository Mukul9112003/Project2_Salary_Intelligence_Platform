from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from src.pipeline.prediction_pipeline import PredictionPipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ❌ REMOVE this
# pipeline = PredictionPipeline()

# ✅ GLOBAL VARIABLE
pipeline = None

# ✅ LOAD SAFELY AT STARTUP
@app.on_event("startup")
def load_pipeline():
    global pipeline
    try:
        print("Loading pipeline...")
        pipeline = PredictionPipeline()
        print("Pipeline loaded successfully")
    except Exception as e:
        print(f"Pipeline failed to load: {e}")

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
    job_skills: str
    job_posted_date: str


@app.get("/")
def home():
    return {"message": "Salary Prediction API Running "}


@app.post("/predict")
def predict(data: SalaryRequest):
    try:
        if pipeline is None:
            return {"error": "Pipeline not loaded"}

        input_dict = data.dict()
        prediction = pipeline.predict(input_dict)

        return {
            "predicted_salary": float(prediction)
        }

    except Exception as e:
        return {"error": str(e)}