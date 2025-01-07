from flask import Flask, render_template
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Azure Blob Storage setup
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = os.getenv('AZURE_CONTAINER_NAME')
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

@app.route('/')
def index():
    blobs = container_client.list_blobs()
    weather_data = []

    for blob in blobs:
        blob_client = container_client.get_blob_client(blob)
        blob_data = blob_client.download_blob().readall()
        weather_data.append(json.loads(blob_data))

    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)