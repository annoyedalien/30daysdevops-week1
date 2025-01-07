# weather_dashboard/__init__.py

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobServiceClient, ContentSettings

# Load environment variables
load_dotenv()

class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
        self.resource_group_name = os.getenv('AZURE_RESOURCE_GROUP')
        self.storage_account_name = os.getenv('AZURE_STORAGE_ACCOUNT')
        self.container_name = os.getenv('AZURE_CONTAINER_NAME')
        self.credential = DefaultAzureCredential()
        self.resource_client = ResourceManagementClient(self.credential, self.subscription_id)
        self.storage_client = StorageManagementClient(self.credential, self.subscription_id)
        self.blob_service_client = None

    def create_resource_group_if_not_exists(self):
        """Create Azure Resource Group if it doesn't exist"""
        try:
            self.resource_client.resource_groups.get(self.resource_group_name)
            print(f"Resource group '{self.resource_group_name}' exists")
        except Exception as e:
            print(f"Creating resource group '{self.resource_group_name}'")
            try:
                self.resource_client.resource_groups.create_or_update(
                    self.resource_group_name,
                    {"location": "eastus"}
                )
                print(f"Successfully created resource group '{self.resource_group_name}'")
            except Exception as e:
                print(f"Error creating resource group: {e}")

    def create_storage_account_if_not_exists(self):
        """Create Azure Storage account if it doesn't exist"""
        try:
            storage_async_operation = self.storage_client.storage_accounts.begin_create(
                self.resource_group_name,
                self.storage_account_name,
                {
                    "location": "eastus",
                    "sku": {"name": "Standard_LRS"},
                    "kind": "StorageV2",
                    "properties": {},
                },
            )
            storage_account = storage_async_operation.result()
            print(f"Storage account '{self.storage_account_name}' created successfully.")
        except Exception as e:
            print(f"Error creating storage account: {e}")

    def get_storage_account_key(self):
        """Get the storage account key"""
        keys = self.storage_client.storage_accounts.list_keys(self.resource_group_name, self.storage_account_name)
        storage_keys = {v.key_name: v.value for v in keys.keys}
        return storage_keys['key1']

    def create_container_if_not_exists(self):
        """Create Azure Blob container if it doesn't exist"""
        try:
            self.blob_service_client = BlobServiceClient(
                account_url=f"https://{self.storage_account_name}.blob.core.windows.net",
                credential=self.get_storage_account_key(),
            )
            container_client = self.blob_service_client.get_container_client(self.container_name)
            container_client.get_container_properties()
            print(f"Container {self.container_name} exists")
        except Exception as e:
            print(f"Creating container {self.container_name}")
            try:
                self.blob_service_client.create_container(self.container_name)
                print(f"Successfully created container {self.container_name}")
            except Exception as e:
                print(f"Error creating container: {e}")

    def fetch_weather(self, city):
        """Fetch weather data from OpenWeather API"""
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def save_to_blob(self, weather_data, city):
        """Save weather data to Azure Blob Storage"""
        if not weather_data:
            return False
            
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"weather-data/{city}-{timestamp}.json"
        
        try:
            weather_data['timestamp'] = timestamp
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=file_name)
            content_settings = ContentSettings(content_type="application/json")
            blob_client.upload_blob(json.dumps(weather_data), blob_type="BlockBlob", content_settings=content_settings)
            print(f"Successfully saved data for {city} to Azure Blob Storage")
            return True
        except Exception as e:
            print(f"Error saving to Azure Blob Storage: {e}")
            return False