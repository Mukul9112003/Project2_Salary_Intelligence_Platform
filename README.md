# Salary Intelligence Platform

## Overview
The Salary Intelligence Platform analyzes and predicts salary trends across industries, job roles, and experience levels. The system combines machine learning predictions with business intelligence dashboards to provide actionable insights.

---

## Features

- Modular data pipeline architecture
- AWS MySQL database integration
- Ensemble machine learning models
- MLflow experiment tracking
- Power BI salary dashboards
- FastAPI prediction API
- Docker containerization
- CI/CD deployment on AWS

---

## Project Architecture

Data Source → MySQL Database → Data Ingestion → Data Validation → Data Transformation → Model Training → Model Evaluation → FastAPI → Docker → AWS EC2

---

## Machine Learning Models

- Random Forest
- XGBoost
- Gradient Boosting

MLflow is used to track experiments and automatically select the best model.

---

## Analytics Layer

The platform provides interactive dashboards built using Power BI to analyze:

- Salary distribution by industry
- Experience level salary trends
- Location-based salary comparisons

---

## Technologies Used

- Python
- MySQL (AWS RDS)
- SQL
- MLflow
- Scikit-learn
- Power BI
- Excel
- Docker
- FastAPI
- AWS
- GitHub Actions

---

## Deployment

The application is deployed using Docker containers on AWS EC2 with CI/CD pipelines.

---

## Future Improvements

- Add salary prediction API for recruiters
- Integrate job market datasets
- Implement automated data updates
