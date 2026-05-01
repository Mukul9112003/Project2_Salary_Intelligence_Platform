import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import dill
import pandas as pd

model_path = "artifact/01_05_2026_17_51_43/Model_Trainer/Model/model.pkl"

with open(model_path, "rb") as f:
    model = dill.load(f)

data = {
    "job_title": "Senior Data Engineer",
    "job_title_short": "Data Engineer",
    "job_location": "San Francisco, CA",
    "job_country": "United States",
    "company_name": "Google",
    "job_schedule_type": "Full-time",
    "job_work_from_home": 0,
    "job_no_degree_mention": 0,
    "job_health_insurance": 1,
    "job_skills": "python, sql, airflow",
    "job_via": "LinkedIn",
    "job_posted_date": "2023-12-01"
}

df = pd.DataFrame([data])

pred = model.predict(df)

print("Prediction:", pred)