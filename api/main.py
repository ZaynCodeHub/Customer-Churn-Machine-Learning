from fastapi import FastAPI
from pathlib import Path
import joblib
import pandas as pd
from pydantic import BaseModel
from sqlalchemy.orm import Session

#Import our new database configuration
from api.database import PredictionLog, SessionLocal, init_db

app = FastAPI(title="Customer Churn Prediction API", version="1.0")
init_db()

# load model
MODEL_PATH = "models/churn_prediction_pipeline.pkl"
pipeline = joblib.load(MODEL_PATH)

# define the request schema using pydantic
class CustomerData(BaseModel):
    #categorical features
    Gender: str
    Senior_Citizen: str
    Partner: str
    Dependents: str
    Phone_Service: str
    Multiple_Lines: str
    Internet_Service: str
    Online_Security: str
    Online_Backup: str
    Device_Protection: str
    Tech_Support: str
    Streaming_TV: str
    Streaming_Movies: str
    Contract: str
    Paperless_Billing: str
    Payment_Method: str

    # Numerical features
    Tenure_Months: float
    Monthly_Charges: float
    Total_Charges: float


#create our first endpoint
@app.get("/")
def health_check():
    return{"Status": "API is running",
           "Message": "Welcome to Customer Churn Prediction Engine"
           }


@app.post("/predict")
def predict_churn(customer: CustomerData):

    #pack all 19 features into a single python dictionary
    raw_payload = customer.dict()

    # Convert Pydantic object to a dictionary matching our training column names
    input_dict = {
        "Gender": customer.Gender,
        "Senior Citizen": customer.Senior_Citizen,
        "Partner": customer.Partner,
        "Dependents": customer.Dependents,
        "Tenure Months": customer.Tenure_Months,
        "Phone Service": customer.Phone_Service,
        "Multiple Lines": customer.Multiple_Lines,
        "Internet Service": customer.Internet_Service,
        "Online Security": customer.Online_Security,
        "Online Backup": customer.Online_Backup,
        "Device Protection": customer.Device_Protection,
        "Tech Support": customer.Tech_Support,
        "Streaming TV": customer.Streaming_TV,
        "Streaming Movies": customer.Streaming_Movies,
        "Contract": customer.Contract,
        "Paperless Billing": customer.Paperless_Billing,
        "Payment Method": customer.Payment_Method,
        "Monthly Charges": customer.Monthly_Charges,
        "Total Charges": customer.Total_Charges,
    }

    #convert dictionary to Pandas DataFrame (single row)
    input_df = pd.DataFrame([input_dict])

    # Make prediction using our pipeline
    prediction = int(pipeline.predict(input_df)[0])
    probabilities = pipeline.predict_proba(input_df)[0]
    churn_probability = round(float(probabilities[1]), 4)

    # Determine granular business risk tier
    if churn_probability >= 0.60:
        risk_level = "High Risk"
    elif churn_probability >= 0.30:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    # write prediction results to the database
    db: Session = SessionLocal()
    try:
        log_entry = PredictionLog(
            input_payload=raw_payload,  # We drop the whole envelope in here!
            churn_prediction=prediction,
            churn_probability=churn_probability,
            risk_level=risk_level,
        )
        db.add(log_entry)
        db.commit()
    finally:
        db.close()

    return {
        "churn_prediction": bool(prediction),
        "churn_probability": churn_probability,
        "risk_level": risk_level,
    }

# 4. New Endpoint: View the last 10 predictions stored in the database
@app.get("/history")
def get_prediction_history():
    db: Session = SessionLocal()
    try:
        logs = (
            db.query(PredictionLog)
            .order_by(PredictionLog.timestamp.desc())
            .limit(10)
            .all()
        )
        return logs
    finally:
        db.close()