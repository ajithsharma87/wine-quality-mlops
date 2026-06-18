# Wine Quality Prediction — End-to-End MLOps Pipeline

> A production-grade machine learning system for predicting wine quality scores, built with a complete MLOps stack: experiment tracking, containerized deployment, and automated CI/CD to AWS.


This project implements the **full lifecycle of an ML model** — from raw data to a live, versioned, cloud-deployed prediction API. It uses physicochemical attributes of wine (acidity, alcohol content, pH, etc.) to predict a quality score, and wraps the entire workflow in MLOps best practices.

**What makes this project production-ready:**
- Experiment runs are tracked and compared in MLflow (hosted on DagsHub)
- Data and model versions are managed with DVC
- The app is containerized with Docker and deployed to AWS ECS via GitHub Actions
- Every push to `main` triggers an automated build, test, and deploy cycle

---

## Architecture

```
Raw Data (CSV)
     │
     ▼
Data Ingestion → Data Validation → Data Transformation
                                          │
                                          ▼
                               Model Training (ElasticNet)
                                          │
                                          ▼
                               MLflow Experiment Tracking
                               (DagsHub remote server)
                                          │
                                          ▼
                               Model Evaluation & Registration
                                          │
                                          ▼
                        Streamlit App → Docker Image → AWS ECR
                                                           │
                                                           ▼
                                              GitHub Actions CI/CD
                                                           │
                                                           ▼
                                                   AWS ECS (Fargate)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **ML Model** | Scikit-learn · ElasticNet regression |
| **Experiment Tracking** | MLflow · DagsHub |
| **Data Versioning** | DVC |
| **Web App** | Streamlit |
| **Containerization** | Docker |
| **Cloud Deployment** | AWS ECS (Fargate) · AWS ECR |
| **CI/CD** | GitHub Actions |

---

## Project Structure

```
├── .github/workflows/       # CI/CD pipeline definition
├── config/                  # Configuration files (paths, params)
├── research/                # Jupyter notebooks for exploration
├── src/                     # Core pipeline source code
│   ├── components/          # Data ingestion, transformation, training
│   ├── pipeline/            # Stage-by-stage execution scripts
│   ├── entity/              # Data classes and config schemas
│   └── utils/               # Helper functions
├── artifacts/               # Generated model files and data (git-ignored)
├── mlruns/                  # Local MLflow tracking (synced to DagsHub)
├── Dockerfile
├── main.py                  # Runs full training pipeline
├── app.py                   # Streamlit prediction app
├── params.yaml              # Model hyperparameters
├── schema.yaml              # Data schema definition
└── requirements.txt
```

---

## Quickstart

### Prerequisites
- Python 3.8
- Conda
- Docker (for containerized runs)
- AWS CLI (for deployment only)

### 1. Clone the repository

```bash
git clone https://github.com/WisdomAnalyst/End-to-end-Machine-Learning-Project-with-Mlflow.git
cd End-to-end-Machine-Learning-Project-with-Mlflow
```

### 2. Create and activate the environment

```bash
conda create -n wine-mlops python=3.8 -y
conda activate wine-mlops
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the training pipeline

```bash
python main.py
```

This executes all pipeline stages in sequence:
1. Data ingestion
2. Data validation
3. Data transformation
4. Model training
5. Model evaluation


## MLflow Experiment Tracking

Experiments are tracked remotely on DagsHub. To connect your own DagsHub instance:

```bash
export MLFLOW_TRACKING_URI=https://dagshub.com/<your-username>/End-to-end-Machine-Learning-Project-with-Mlflow.mlflow
export MLFLOW_TRACKING_USERNAME=<your-username>
export MLFLOW_TRACKING_PASSWORD=<your-dagshub-token>
```

Then run the pipeline and view results:

```bash
python main.py
mlflow ui   # View locally at http://localhost:5000
```

The MLflow dashboard lets you compare runs, inspect metrics (RMSE, MAE, R²), and register the best model for deployment.

---

## Deployment

### Docker (local)

```bash
# Build the image
docker build -t wine-quality-prediction .

# Run the container
docker run -p 8080:8080 wine-quality-prediction
```

App is available at `http://localhost:8080`.

### AWS ECS via GitHub Actions (automated)

Every push to `main` triggers the CI/CD pipeline automatically:

1. **Build** — Docker image is built from the latest code
2. **Push** — Image is pushed to AWS ECR
3. **Deploy** — ECS service is updated with the new image (zero-downtime)

To set this up in your own fork, add these secrets to your GitHub repository:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

The workflow file is at `.github/workflows/main.yaml`.

**AWS resources used:**
- ECR Repository: `wine-quality-prediction`
- ECS Cluster: `wine-quality-cluster`
- ECS Service: `wine-quality-service` (Fargate, 1 task)
- Port: `8080`

---

## Pipeline Stages

To run individual stages:

```bash
# Stage 1: Ingest data
python src/pipeline/stage_01_data_ingestion.py

# Stage 2: Validate schema
python src/pipeline/stage_02_data_validation.py

# Stage 3: Transform features
python src/pipeline/stage_03_data_transformation.py

# Stage 4: Train model
python src/pipeline/stage_04_model_trainer.py

# Stage 5: Evaluate and log to MLflow
python src/pipeline/stage_05_model_evaluation.py
```

---

## Model Performance

The ElasticNet model is evaluated on a held-out test set. Metrics are logged to MLflow on every run:

| Metric | Value |
|---|---|
| RMSE | tracked per run |
| MAE | tracked per run |
| R² | tracked per run |

To view the best run, open the MLflow UI and filter by lowest RMSE.

---

## Monitoring & Troubleshooting

- **CloudWatch Logs** — container output is streamed to CloudWatch for deployed instances
- **ECS Service Events** — check the ECS console for task health and deployment status
- **GitHub Actions** — build and deploy logs available in the Actions tab

---

## Author

**Akano Wisdom Onuoha**
AI Engineer · Data Scientist · Technical Writer

- GitHub: [@WisdomAnalyst](https://github.com/WisdomAnalyst)
- Substack: [Wisdom in AI and Automation](https://substack.com/@wisakanoautomation)
- LinkedIn: [wisdomanalyst](https://www.linkedin.com/in/wisdomanalyst)

---

## License

MIT License — see [LICENSE](LICENSE) for details.
