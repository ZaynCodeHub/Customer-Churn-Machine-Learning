Customer Churn Machine Learning & Prediction SystemA production-ready, end-to-end Machine Learning microservices application for predicting telecommunications customer churn. Built with Scikit-Learn, FastAPI, SQLite, Streamlit, and Docker Compose.🏗️ System ArchitectureThe application uses a decoupled microservices architecture orchestrating two containers via Docker Compose with volume-mapped persistent database logging.Plaintext                  +-----------------------+
                  |  Streamlit Dashboard  | (Frontend Container - Port 8501)
                  +-----------+-----------+
                              |
                              | HTTP POST /predict
                              v
                  +-----------------------+
                  |    FastAPI Server     | (Backend Container - Port 8000)
                  +-----------+-----------+
                              |
                     +--------+--------+
                     |                 |
                     v                 v
            +-----------------+  +----------------------+
            |  Scikit-Learn   |  |   SQLite Database    |
            |   ML Pipeline   |  | (churn_predictions)  |
            +-----------------+  +----------------------+
✨ FeaturesML Inference Engine: Balanced Logistic Regression pipeline trained on 19 customer features with feature scaling and categorical one-hot encoding.Risk Stratification: Classifies churn probabilities into actionable risk tiers:Low Risk: $< 30\%$ Churn ProbabilityMedium Risk: $30\% - 60\%$ Churn ProbabilityHigh Risk: $\ge 60\%$ Churn ProbabilityJSON Envelope Database Logging: Every prediction is logged in SQLite (prediction_logs table) via SQLAlchemy, storing full 19-feature JSON payloads alongside timestamps and risk levels.Interactive Frontend: Styled Streamlit dashboard featuring multi-tab inputs and live model scoring.Microservices Containerization: Isolated build environments using Dockerfile.api and Dockerfile.frontend orchestrated via docker-compose.yml.🛠️ Tech StackMachine Learning: Scikit-Learn, Pandas, JoblibBackend API: FastAPI, Uvicorn, PydanticDatabase & ORM: SQLite, SQLAlchemyFrontend UI: Streamlit, RequestsContainerization: Docker, Docker Compose📁 Project StructurePlaintextCustomer-Churn-Machine-Learning/
│
├── api/
│   ├── database.py       # SQLAlchemy ORM schema and SQLite session setup
│   └── main.py           # FastAPI application endpoints (/predict, /history)
│
├── frontend/
│   └── app.py            # Streamlit dashboard interface
│
├── models/
│   └── churn_prediction_pipeline.pkl  # Trained ML pipeline export
│
├── data/
│   └── raw/              # Telco Customer Churn dataset
│
├── Dockerfile.api        # Docker container build script for FastAPI backend
├── Dockerfile.frontend   # Docker container build script for Streamlit frontend
├── docker-compose.yml    # Microservices orchestration and volume binding
├── requirements.txt      # Production Python dependencies
├── .gitignore            # Git exclusion rules
└── README.md             # Project documentation
🚀 Getting StartedOption 1: Running with Docker Compose (Recommended)Prerequisite: Ensure Docker Desktop is installed and running.Clone the repository:Bashgit clone https://github.com/ZaynCodeHub/Customer-Churn-Machine-Learning.git
cd Customer-Churn-Machine-Learning
Launch containers:Bashdocker compose up --build
Access services:Streamlit Dashboard: http://localhost:8501FastAPI Docs (Swagger UI): http://localhost:8000/docsPrediction History Endpoint: http://localhost:8000/historyOption 2: Running Locally Without DockerCreate and activate virtual environment:Bashpython -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
Install dependencies:Bashpip install -r requirements.txt
Start the FastAPI Backend:Bashuvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
Start the Streamlit Frontend (in a new terminal):Bashstreamlit run frontend/app.py
🔌 API Documentation1. Health CheckEndpoint: GET /Response:JSON{
  "status": "API is online and Database is connected."
}
2. Predict Customer ChurnEndpoint: POST /predictSample Request Body:JSON{
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
Sample Response:JSON{
  "churn_prediction": true,
  "churn_probability": 0.7421,
  "risk_level": "High Risk"
}
3. Prediction HistoryEndpoint: GET /historyDescription: Fetches the 10 most recent logged predictions from the SQLite database containing timestamps, risk levels, and complete feature input payloads.☁️ Cloud Deployment (Render)Deploy Backend (churn_api):Create a new Web Service on Render.com.Connect repository ZaynCodeHub/Customer-Churn-Machine-Learning.Select Docker environment and set Dockerfile path to ./Dockerfile.api.Update Frontend API Endpoint:Modify API_URL in frontend/app.py to point to the live Render backend URL (https://<your-backend-service>[.onrender.com/predict](https://.onrender.com/predict)).Deploy Frontend (churn_frontend):Create a second Web Service on Render.Select Docker environment and set Dockerfile path to ./Dockerfile.frontend.👨‍💻 AuthorSyed Zain AfaqGitHub: @ZaynCodeHub
