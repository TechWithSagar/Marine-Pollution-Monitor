import streamlit as st
import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT = os.getenv("WML_API_ENDPOINT")
API_KEY = os.getenv("WML_API_KEY")
IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"

@st.cache_data(ttl=3600) 
def get_iam_token(api_key):
    """Generates an IAM token from an IBM Cloud API key."""
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    data = {
        'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
        'apikey': api_key
    }
    try:
        response = requests.post(IAM_TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        return response.json()['access_token']
    except requests.exceptions.RequestException as e:
        st.error(f"Error getting IAM token: {e}")
        return None

def call_prediction_api(data, iam_token):
    """Calls the deployed Watson Machine Learning API with new data and a valid IAM token."""
    payload = {
        "input_data": [{
            "fields": list(data.keys()),
            "values": [list(data.values())]
        }]
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {iam_token}'
    }

    try:
        response = requests.post(API_ENDPOINT, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling API: {e}")
        return None

st.set_page_config(layout="wide", page_title="Marine Pollution Monitor")

st.title("🌊 Marine Pollution Monitoring Dashboard")
st.markdown("---")

st.write("Enter water quality parameters to predict potability:")

col1, col2, col3 = st.columns(3)
with col1:
    ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
    hardness = st.number_input("Hardness", min_value=0.0, value=180.0, step=1.0)
    solids = st.number_input("Solids", min_value=0.0, value=20000.0, step=100.0)
with col2:
    chloramines = st.number_input("Chloramines", min_value=0.0, value=7.0, step=0.1)
    sulfate = st.number_input("Sulfate", min_value=0.0, value=350.0, step=1.0)
    conductivity = st.number_input("Conductivity", min_value=0.0, value=400.0, step=1.0)
with col3:
    organic_carbon = st.number_input("Organic_carbon", min_value=0.0, value=12.0, step=0.1)
    trihalomethanes = st.number_input("Trihalomethanes", min_value=0.0, value=60.0, step=0.1)
    turbidity = st.number_input("Turbidity", min_value=0.0, value=4.0, step=0.1)

input_data = {
    "ph": ph,
    "Hardness": hardness,
    "Solids": solids,
    "Chloramines": chloramines,
    "Sulfate": sulfate,
    "Conductivity": conductivity,
    "Organic_carbon": organic_carbon,
    "Trihalomethanes": trihalomethanes,
    "Turbidity": turbidity
}

if st.button("Predict Potability"):
    with st.spinner("Predicting..."):
        iam_token = get_iam_token(API_KEY)
        if iam_token:
            prediction_result = call_prediction_api(input_data, iam_token)

            if prediction_result:
                try:
                    prediction = prediction_result['predictions'][0]['values'][0][0]
                    st.markdown("---")
                    st.subheader("Prediction Result:")
                    if prediction == 1:
                        st.success("✅ Water is predicted to be **POTABLE** (Safe for consumption).")
                        st.balloons()
                    else:
                        st.error("❌ Water is predicted to be **NON-POTABLE** (Not safe for consumption).")
                        st.warning("Warning: Water quality may be compromised. Further investigation recommended.")

                    st.markdown("#### Input Data Provided:")
                    st.json(input_data)

                    st.markdown("#### Raw API Response:")
                    st.json(prediction_result)

                except (KeyError, IndexError) as e:
                    st.error(f"Error parsing prediction result: {e}")
                    st.json(prediction_result)
            else:
                st.error("Failed to get prediction from the API.")
        else:
            st.error("Authentication failed. Could not get IAM token.")

st.markdown("---")
st.caption("This dashboard is part of a multi-agent AI system for marine pollution monitoring.")