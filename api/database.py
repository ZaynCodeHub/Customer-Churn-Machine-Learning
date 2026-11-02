from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, JSON, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Database Connection URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./churn_predictions.db"

# 2. Database Engine & Session setup
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. The Table Schema (The blueprint for our database)
class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    # Meta-data (Automatically generated)
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # THE ENVELOPE: One column to hold all 19 customer inputs
    input_payload = Column(JSON)

    # THE RESULTS: What the ML model decided
    churn_prediction = Column(Integer)     # 0 (No Churn) or 1 (Churn)
    churn_probability = Column(Float)      # exact decimal, e.g., 0.8142
    risk_level = Column(String)            # "High Risk", "Medium Risk", "Low Risk"

# 4. Helper function to physically create the database file
def init_db():
    Base.metadata.create_all(bind=engine)