import os
import ibm_boto3
from ibm_botocore.client import Config
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Retrieve credentials from environment variables
COS_API_KEY_ID = os.getenv("COS_API_KEY_ID")
COS_SERVICE_INSTANCE_ID = os.getenv("COS_SERVICE_INSTANCE_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# These are standard endpoints for IBM Cloud Object Storage
# You can find your specific endpoint in the IBM Cloud dashboard
COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud"

# --- Agent Logic ---
def get_cos_client():
    """Returns a client object to interact with IBM Cloud Object Storage."""
    return ibm_boto3.client(
        's3',
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=COS_SERVICE_INSTANCE_ID,
        config=Config(signature_version='oauth'),
        endpoint_url=COS_ENDPOINT
    )

def read_local_data(file_path):
    """Reads a local file and returns its content."""
    print(f"Reading data from local file: {file_path}...")
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def upload_to_cos(client, data, bucket_name, object_name):
    """Uploads data to a specified bucket in Cloud Object Storage."""
    print(f"Uploading data to bucket '{bucket_name}' with name '{object_name}'...")
    try:
        client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=data
        )
        print("Upload successful.")
    except Exception as e:
        print(f"Error uploading data: {e}")

def main():
    # Name of the file located in the same directory as the script
    local_file_name = "water_potability.csv"
    object_name = "raw_water_potability_data.csv"

    # Get the data from the local file
    data_content = read_local_data(local_file_name)
    if data_content:
        # Get the COS client
        cos_client = get_cos_client()
        # Upload the data
        upload_to_cos(cos_client, data_content, BUCKET_NAME, object_name)

if __name__ == "__main__":
    main()