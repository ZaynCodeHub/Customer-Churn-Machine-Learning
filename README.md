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
