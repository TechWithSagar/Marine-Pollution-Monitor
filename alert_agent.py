import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('WML_API_KEY')
API_ENDPOINT = os.getenv("WML_API_ENDPOINT")
IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"

def get_iam_token(api_key):
    """Get IAM access token using IBM Cloud API key."""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "apikey": api_key,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }

    response = requests.post(IAM_TOKEN_URL, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def call_prediction_api(data, access_token):
    """Call IBM Watson Machine Learning prediction API."""
    payload = {
        "input_data": [{
            "fields": list(data.keys()),
            "values": [list(data.values())]
        }]
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()

def main():
    sample_data = {
        "ph": 4.5,
        "Hardness": 150.0,
        "Solids": 20000.0,
        "Chloramines": 5.0,
        "Sulfate": 300.0,
        "Conductivity": 450.0,
        "Organic_carbon": 10.0,
        "Trihalomethanes": 55.0,
        "Turbidity": 9.0
    }

    try:
        access_token = get_iam_token(API_KEY)
        prediction_result = call_prediction_api(sample_data, access_token)

        prediction = prediction_result['predictions'][0]['values'][0][0]
        print(f"Prediction result: Potability = {prediction}")

        if prediction == 1:
            print("--- ALERT: Water is predicted to be POTABLE ---")
        else:
            print("--- ALERT: Water is predicted to be NON-POTABLE ---")
            print("Warning: Water quality may be compromised.")
            for key, value in sample_data.items():
                print(f"  - {key}: {value}")

    except Exception as e:
        print(f"Error calling API: {e}")

if __name__ == '__main__':
    main()
