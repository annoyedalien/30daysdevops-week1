# Weather Dashboard

This project fetches weather data from the OpenWeather API and saves it to Azure Blob Storage. It includes the creation of an Azure Resource Group, Storage Account, and Blob Container if they do not already exist.

## Prerequisites

- Python 3.6 or higher
- Azure subscription
- OpenWeather API key

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/annoyedalien/30daysdevops-week1.git
   cd week1
   ```
2. Create a virtual environment:
To create a virtual environment (venv) in Python, you don't need to install any additional packages if you're using Python 3.3 or later, as the venv module is included in the standard library. 
  ```bash
    python3 -m venv venv
    source venv/bin/activate
   ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## Create a .env file in the project directory and add your credentials:
```bash
vi .env
```
```
#.env
AZURE_SUBSCRIPTION_ID=your_subscription_id
AZURE_RESOURCE_GROUP=your_resource_group
AZURE_STORAGE_ACCOUNT=your_storage_account
AZURE_CONTAINER_NAME=your_container_name
OPENWEATHER_API_KEY=your_openweather_api_key
```
## Usage
Run the main script:
```
python main.py
```
This will:

Create the Azure Resource Group if it doesn't exist.
Create the Azure Storage Account if it doesn't exist.
Create the Azure Blob Container if it doesn't exist.
Fetch weather data for specified cities.
Save the weather data to Azure Blob Storage.
## Project Structure
```
src/
│
├── weather_dashboard/
│   └── __init__.py
│
├── main.py
├── requirements.txt
└── .env
```
## Dependencies
- azure-identity
- azure-mgmt-resource
- azure-mgmt-storage
- azure-storage-blob
- requests
- python-dotenv
