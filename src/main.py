# main.py

from weather_dashboard import WeatherDashboard

def main():
    dashboard = WeatherDashboard()
    
    # Create resource group if needed
    dashboard.create_resource_group_if_not_exists()
    
    # Create storage account if needed
    dashboard.create_storage_account_if_not_exists()
    
    # Create container if needed
    dashboard.create_container_if_not_exists()
    
    cities = ["Philadelphia", "Seattle", "New York"]
    
    for city in cities:
        print(f"\nFetching weather for {city}...")
        weather_data = dashboard.fetch_weather(city)
        if weather_data:
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            
            print(f"Temperature: {temp}°F")
            print(f"Feels like: {feels_like}°F")
            print(f"Humidity: {humidity}%")
            print(f"Conditions: {description}")
            
            # Save to Azure Blob Storage
            success = dashboard.save_to_blob(weather_data, city)
            if success:
                print(f"Weather data for {city} saved to Azure Blob Storage!")
        else:
            print(f"Failed to fetch weather data for {city}")

if __name__ == "__main__":
    main()