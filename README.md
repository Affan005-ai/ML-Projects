## End to End Machine Learning Project

---

# From Model to Production: Dual AWS Deployment (Elastic Beanstalk + Docker/ECR/EC2 CI/CD)

# Student Math Score Predictor

This repository is the **Elastic Beanstalk deployment track** on AWS for the Student Math Score Predictor project.  
The Docker + ECR + EC2 CI/CD track is maintained in a separate companion repository.

## Repository Map

1. Elastic Beanstalk deployment (this repo): `https://github.com/Affan005-ai/ML-Projects`
2. Docker + ECR + EC2 CI/CD repo: `https://github.com/Affan005-ai/AWS-CI-CD-Projects`

## Problem Statement

Predict a student’s math score from:

1. Gender
2. Race/Ethnicity
3. Parental level of education
4. Lunch type
5. Test preparation course
6. Reading score
7. Writing score

## Project Features

1. End-to-end ML pipeline from ingestion to artifact generation
2. Flask web app for live prediction
3. Multi-model regression training
4. Hyperparameter tuning with `RandomizedSearchCV`
5. AWS Elastic Beanstalk deployment setup
6. Real commit-driven iteration and fixes

## End-to-End Architecture

1. Data ingestion reads `Notebook/data/StudentsPerformance.csv`
2. Train-test split saved to `artifacts/train.csv` and `artifacts/test.csv`
3. Transformation pipeline handles imputation, encoding, and scaling
4. Multiple regressors are trained and tuned
5. Best model + preprocessor saved in `artifacts/`
6. Flask app serves inference via `/predict`
7. Elastic Beanstalk hosts the application

## ML Pipeline (Deep Dive)

### 1) Data Ingestion

Implemented in `src/components/data_ingestion.py`:

1. Reads source dataset
2. Saves raw/train/test CSV artifacts
3. Uses deterministic split with `random_state=42`

### 2) Data Transformation

Implemented in `src/components/data_transformation.py`:

1. Numerical features: impute median + standard scaling
2. Ordinal features: impute most frequent + ordered encoding
3. Nominal features: impute most frequent + one-hot encoding

### 3) Model Training and Selection

Implemented in `src/components/model_trainer.py`:

1. Trains multiple regressors
2. Compares test R2 scores
3. Selects best model above quality threshold

### 4) Hyperparameter Tuning

Implemented in `src/utils.py` via `evaluate_models(...)`:

1. Uses `RandomizedSearchCV`
2. `n_iter=9`, `cv=3`, `scoring='r2'`, `n_jobs=-1`
3. Picks best estimator per model
4. Saves best overall model artifact

## Inference Layer

`application.py` exposes:

1. `/` for UI
2. `/predict` for form-based prediction

Artifacts loaded at runtime:

1. `artifacts/model_1.pkl`
2. `artifacts/preprocessor_1.pkl`

## Deployment Track (Primary in This Repo): Elastic Beanstalk

Key files:

1. `.elasticbeanstalk/config.yml`
2. `.ebextensions/python.config`
3. `Procfile`
4. `application.py`

Why this track:

1. Managed platform lifecycle
2. Faster app hosting with less infra overhead

## Deployment Track (Related Repo): Docker + ECR + EC2 + GitHub Actions

Companion repo: `https://github.com/Affan005-ai/AWS-CI-CD-Projects`

What that track covers:

1. Docker image build
2. Push to Amazon ECR
3. Deploy on EC2 self-hosted runner
4. CI/CD automation in GitHub Actions

## Production-Grade Improvements

1. Use Gunicorn-based runtime consistently
2. Add CI quality gates (real tests/linting)
3. Add image vulnerability scanning
4. Use OIDC/IAM role instead of long-lived keys
5. Add CloudWatch logging and alarms
6. Add health checks and rollback strategy

## One Screenshot Proof

![Deployment Proof](docs/screenshots/proof/deployment-proof.png)

## Quick Start

```bash
pip install -r requirements.txt
python application.py
Open:

http://127.0.0.1:5000
```

## Credits

- This project and deployment learning journey were inspired by Krish Naik and his end-to-end ML engineering guidance.

## Acknowledgment

- Thanks to the open-source Python, scikit-learn, Flask, Docker, and AWS communities for documentation and tooling support.
