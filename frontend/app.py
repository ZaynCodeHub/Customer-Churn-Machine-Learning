import requests
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Telco Churn AI Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Custom CSS Theme & Styling
st.markdown(
    """
    <style>
    /* Global Container Styles */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #9CA3AF;
        margin-bottom: 2rem;
    }
    
    /* Metric Card Customization */
    [data-testid="stMetricValue"] {
        font-size: 2.4rem;
        font-weight: 800;
    }
    
    /* Action Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #2563EB 0%, #7C3AED 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.39);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #1D4ED8 0%, #6D28D9 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(37, 99, 235, 0.55);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Sidebar Information
with st.sidebar:
    st.image(
        "https://img.icons8.com/isometric/512/artificial-intelligence.png",
        width=80,
    )
    st.title("Model Dashboard")
    st.markdown("**Engine:** Logistic Regression (Balanced)")
    st.markdown("**API Status:** `http://127.0.0.1:8000`")
    st.divider()
    st.markdown("### Risk Thresholds")
    st.caption("🟢 **Low Risk:** < 30% Probability")
    st.caption("🟡 **Medium Risk:** 30% - 60% Probability")
    st.caption("🔴 **High Risk:** ≥ 60% Probability")
    st.divider()
    st.info("💡 **Tip:** Fiber Optic + Month-to-Month contracts heavily drive churn probability.")

# 4. Main Title Section
st.markdown(
    '<div class="main-header">⚡ Telecom Customer Churn AI Platform</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Real-time ML inference engine for customer risk scoring and proactive retention strategy.</div>',
    unsafe_allow_html=True,
)

API_URL = "http://api:8000/predict"

# 5. Input Forms Grid
st.markdown("### 📋 Customer Profile Inputs")

tab1, tab2, tab3 = st.tabs([
    "👤 Demographics & Account",
    "📶 Telecom Services",
    "💳 Contract & Billing",
])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        gender = st.radio("Gender", ["Female", "Male"], horizontal=True)
        senior_citizen = st.radio(
            "Senior Citizen", ["No", "Yes"], horizontal=True
        )
    with col2:
        partner = st.radio("Has Partner", ["No", "Yes"], horizontal=True)
        dependents = st.radio("Has Dependents", ["No", "Yes"], horizontal=True)

with tab2:
    col1, col2, col3 = st.columns(3)
    with col1:
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox(
            "Multiple Lines", ["No", "Yes", "No phone service"]
        )
        internet_service = st.selectbox(
            "Internet Service", ["Fiber optic", "DSL", "No"]
        )
    with col2:
        online_security = st.selectbox(
            "Online Security", ["No", "Yes", "No internet service"]
        )
        online_backup = st.selectbox(
            "Online Backup", ["No", "Yes", "No internet service"]
        )
        device_protection = st.selectbox(
            "Device Protection", ["No", "Yes", "No internet service"]
        )
    with col3:
        tech_support = st.selectbox(
            "Tech Support", ["No", "Yes", "No internet service"]
        )
        streaming_tv = st.selectbox(
            "Streaming TV", ["No", "Yes", "No internet service"]
        )
        streaming_movies = st.selectbox(
            "Streaming Movies", ["No", "Yes", "No internet service"]
        )

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        contract = st.selectbox(
            "Contract Type", ["Month-to-month", "One year", "Two year"]
        )
        paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment_method = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)",
            ],
        )
    with col2:
        tenure_months = st.slider("Tenure Length (Months)", 0, 72, 12)
        monthly_charges = st.number_input(
            "Monthly Charges ($)", min_value=18.0, max_value=120.0, value=75.0
        )
        total_charges = st.number_input(
            "Calculated Total Charges ($)",
            min_value=0.0,
            value=float(monthly_charges * tenure_months),
        )

st.write("")

# 6. Evaluation Trigger
if st.button("🚀 Calculate Churn Probability"):
    payload = {
        "Gender": gender,
        "Senior_Citizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "Phone_Service": phone_service,
        "Multiple_Lines": multiple_lines,
        "Internet_Service": internet_service,
        "Online_Security": online_security,
        "Online_Backup": online_backup,
        "Device_Protection": device_protection,
        "Tech_Support": tech_support,
        "Streaming_TV": streaming_tv,
        "Streaming_Movies": streaming_movies,
        "Contract": contract,
        "Paperless_Billing": paperless_billing,
        "Payment_Method": payment_method,
        "Tenure_Months": float(tenure_months),
        "Monthly_Charges": float(monthly_charges),
        "Total_Charges": float(total_charges),
    }

    with st.spinner("Analyzing customer behavioral features..."):
        try:
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                result = response.json()
                prob = result["churn_probability"]
                risk = result["risk_level"]

                st.divider()
                st.markdown("### 📊 Inference Results")

                res_col1, res_col2, res_col3 = st.columns([1, 1, 2])

                with res_col1:
                    st.metric(
                        label="Churn Score",
                        value=f"{prob * 100:.1f}%",
                        delta=f"{'High' if prob >= 0.5 else 'Normal'} Risk Level",
                        delta_color="inverse",
                    )

                with res_col2:
                    st.metric(label="Risk Stratification", value=risk)

                with res_col3:
                    st.write("**Probability Spectrum:**")
                    st.progress(prob)

                # Strategic Business Advice Box
                st.write("")
                if risk == "High Risk":
                    st.error(
                        "🔴 **High Flight Risk Detected!**\n\n"
                        "**Recommended Retention Action:** Offer an immediate 15% annual contract discount or assign a dedicated account manager."
                    )
                elif risk == "Medium Risk":
                    st.warning(
                        "🟡 **Watchlist Customer (Moderate Risk)**\n\n"
                        "**Recommended Retention Action:** Send a targeted email offering free Tech Support or Online Backup add-ons."
                    )
                else:
                    st.success(
                        "🟢 **Stable / Low Risk Customer**\n\n"
                        "**Recommended Retention Action:** No promotional discounts necessary. Standard engagement workflow."
                    )

            else:
                st.error(
                    f"API Request Failed with Status Code: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "❌ Could not connect to FastAPI server at `http://127.0.0.1:8000`. Make sure Uvicorn is running in your terminal!"
            )