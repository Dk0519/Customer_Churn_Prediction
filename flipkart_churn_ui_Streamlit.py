import streamlit as st
import pandas as pd
import joblib

# Load both model and feature names
model_bundle = joblib.load("rf_churn_model.pkl")
model = model_bundle["model"]
feature_order = model_bundle["features"]

st.set_page_config(page_title="Flipkart Churn Predictor", layout="centered")
st.markdown("<h1 style='text-align: center; color: #FF6F00;'>📦 Flipkart Customer Churn Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Estimate the probability of customer churn using behavioral data.</p>", unsafe_allow_html=True)

# Input Form
with st.form("input_form"):
    st.markdown("### 🔍 Enter Customer Details")
    col1, col2 = st.columns(2)

    with col1:
        total_orders = st.number_input("🛒 Total Orders", min_value=0)
        avg_review_score = st.slider("⭐ Average Review Score", 1.0, 5.0, step=0.1)

    with col2:
        avg_order_value = st.number_input("💵 Average Order Value", min_value=0.0)
        avg_delivery_time = st.number_input("🚚 Avg Delivery Time (days)", min_value=0)

    days_since_last_order = st.number_input("📆 Days Since Last Order", min_value=0)

    submitted = st.form_submit_button("Predict Churn")

if submitted:
    input_data = pd.DataFrame({
        'total_orders': [total_orders],
        'avg_review_score': [avg_review_score],
        'avg_order_value': [avg_order_value],
        'avg_delivery_time': [avg_delivery_time],
        'days_since_last_order': [days_since_last_order]
    })

    # Reorder columns to match training data
    input_data = input_data[feature_order]

    # Predict
    prediction = model.predict(input_data)[0]
    prob = model.predict_proba(input_data)[0][1]

    st.markdown("---")
    if prediction == 1:
        st.error(f"⚠️ This customer is likely to churn.\n\n🧠 **Churn Probability: {prob:.2f}**")
    else:
        st.success(f"✅ This customer is likely to stay.\n\n🧠 **Retention Probability: {1 - prob:.2f}**")
