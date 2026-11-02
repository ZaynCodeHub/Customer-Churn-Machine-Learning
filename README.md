# 📊 Telco Customer Churn Prediction Engine

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.34.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Microservices-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.5.0+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)

An end-to-end, production-grade Machine Learning microservices application designed to analyze customer attributes, score churn risk in real-time, and log raw JSON payload records for model monitoring and retraining.

---

## 🏗️ System Architecture

The project follows a microservices architecture orchestrated with Docker Compose. The Streamlit dashboard communicates asynchronously with the FastAPI REST server, which manages feature transformation, model inference, and database persistent logging.

```text
                  +-----------------------+
                  |  Streamlit Dashboard  | (Frontend Service - Port 8501)
                  +-----------+-----------+
                              |
                              | HTTP POST /predict
                              v
                  +-----------------------+
                  |    FastAPI Backend    | (API Service - Port 8000)
                  +-----------+-----------+
                              |
                     +--------+--------+
                     |                 |
                     v                 v
            +-----------------+  +----------------------+
            |  Scikit-Learn   |  |   SQLite Database    |
            |   ML Pipeline   |  | (churn_predictions)  |
            +-----------------+  +----------------------+

---

## ✨ Features

* **Real-Time Predictive Engine:** Balanced Logistic Regression pipeline trained across 19 demographic, service, and billing features with automated scaling and one-hot encoding.
* **Risk Stratification Engine:** Categorizes customer churn likelihood into three business risk levels:
* 🟢 **Low Risk:** $< 30\%$ Probability
* 🟡 **Medium Risk:** $30\% - 60\%$ Probability
* 🔴 **High Risk:** $\ge 60\%$ Probability


* **JSON Envelope Logging:** Utilizes a dynamic `input_payload` JSON column in SQLite via SQLAlchemy, preserving all 19 features per request without requiring SQL schema migrations when features change.
* **Audit & History Tracking:** Includes a `/history` GET endpoint returning recent logged predictions, timestamps, and feature parameters.
* **Microservices Containerization:** Fully containerized setup featuring custom `Dockerfile.api` and `Dockerfile.frontend` images synchronized with persistent host volume mapping.

---

## 🛠️ Tech Stack

* **Machine Learning:** Scikit-Learn, Pandas, Joblib
* **Backend Framework:** FastAPI, Uvicorn, Pydantic
* **Database & ORM:** SQLite, SQLAlchemy
* **Frontend UI:** Streamlit, Requests
* **DevOps & Infrastructure:** Docker, Docker Compose, Git

---

## 📁 Repository Structure

```text
Customer-Churn-Machine-Learning/
│
├── api/
│   ├── database.py       # SQLAlchemy engine, session maker & JSON payload table schema
│   └── main.py           # FastAPI server routes (/predict, /history) & DB handler
│
├── frontend/
│   └── app.py            # Streamlit dashboard interface
│
├── models/
│   └── churn_prediction_pipeline.pkl  # Trained ML pipeline export
│
├── data/
│   └── raw/              # Raw Telco Customer Churn dataset
│
├── Dockerfile.api        # Docker container build configuration for FastAPI
├── Dockerfile.frontend   # Docker container build configuration for Streamlit
├── docker-compose.yml    # Microservices network topology & volume mapping
├── requirements.txt      # Locked dependency specifications
├── .gitignore            # Git untracked path rules
└── README.md             # Project documentation

```

---

## 🚀 Execution & Setup

### 1. Docker Compose Execution (Recommended)

Ensure Docker Desktop is open and running on your machine.

```bash
# Clone the repository
git clone [https://github.com/ZaynCodeHub/Customer-Churn-Machine-Learning.git](https://github.com/ZaynCodeHub/Customer-Churn-Machine-Learning.git)
cd Customer-Churn-Machine-Learning

# Build and start microservice containers
docker compose up --build

```

Access services:

* **Streamlit Dashboard:** `http://localhost:8501`
* **Swagger API Documentation:** `http://localhost:8000/docs`
* **Database History Endpoint:** `http://localhost:8000/history`

---

### 2. Local Execution (Native Python)

```bash
# Create and activate virtual environment
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch FastAPI server (Terminal 1)
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload

# Launch Streamlit dashboard (Terminal 2)
streamlit run frontend/app.py

```

---

## 🔌 API Endpoints Reference

### 1. Health Check

`GET /`

```json
{
  "status": "API is online and Database is connected."
}

```

### 2. Predict Customer Churn

`POST /predict`

*Request Payload:*

```json
{
  "Gender": "Female",
  "Senior_Citizen": "No",
  "Partner": "Yes",
  "Dependents": "No",
  "Phone_Service": "Yes",
  "Multiple_Lines": "No",
  "Internet_Service": "Fiber optic",
  "Online_Security": "No",
  "Online_Backup": "Yes",
  "Device_Protection": "No",
  "Tech_Support": "No",
  "Streaming_TV": "Yes",
  "Streaming_Movies": "Yes",
  "Contract": "Month-to-month",
  "Paperless_Billing": "Yes",
  "Payment_Method": "Electronic check",
  "Tenure_Months": 12.0,
  "Monthly_Charges": 85.5,
  "Total_Charges": 1026.0
}

```

*Response Payload:*

```json
{
  "churn_prediction": true,
  "churn_probability": 0.7421,
  "risk_level": "High Risk"
}

```

### 3. Prediction History Log

`GET /history`

Returns the 10 most recent logged database entries along with timestamps and full feature dictionaries.

---

## ☁️ Cloud Deployment Guide (Render)

1. **Deploy Backend (`churn_api`):**
* Create a **Web Service** on Render connected to `ZaynCodeHub/Customer-Churn-Machine-Learning`.
* Set **Language / Runtime** to `Docker` and **Dockerfile Path** to `./Dockerfile.api`.


2. **Update Frontend Endpoint:**
* Copy the live backend URL (e.g., `https://churn-api-backend.onrender.com`).
* Update `API_URL` inside `frontend/app.py` to point to the live Render backend `/predict` route and push changes to GitHub.


3. **Deploy Frontend (`churn_frontend`):**
* Create a second **Web Service** on Render.
* Set **Language / Runtime** to `Docker` and **Dockerfile Path** to `./Dockerfile.frontend`.



---

## 👨‍💻 Author

**Syed Zain Afaq**

* **GitHub:** [@ZaynCodeHub](https://github.com/ZaynCodeHub)

```

```
