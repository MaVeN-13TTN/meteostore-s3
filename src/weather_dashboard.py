import os
import json
import boto3
import requests
import random
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        # Generate bucket name with random number
        random_number = random.randint(0, 32767)
        bucket_prefix = os.getenv("AWS_BUCKET_NAME", "weather-data")
        # Remove any trailing hyphens and ensure we have a valid bucket name
        bucket_prefix = bucket_prefix.rstrip("-")
        self.bucket_name = f"{bucket_prefix}-{random_number}"
        print(f"Debug - Using bucket name: {self.bucket_name}")
        self.s3_client = boto3.client("s3")

    def create_bucket_if_not_exists(self):
        """Create S3 bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} exists")
        except Exception as e:
            print(f"Debug - Head bucket error: {str(e)}")
            print(f"Creating bucket {self.bucket_name}")
        try:
            # Simpler creation for us-east-1
            self.s3_client.create_bucket(Bucket=self.bucket_name)
            print(f"Successfully created bucket {self.bucket_name}")
        except Exception as e:
            print(f"Error creating bucket: {e}")
            print(f"Debug - Bucket name length: {len(self.bucket_name)}")
            print(f"Debug - Bucket name characters: {[c for c in self.bucket_name]}")

    def fetch_weather(self, city):
        """Fetch weather data from OpenWeather API"""
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": self.api_key, "units": "imperial"}

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def save_to_s3(self, weather_data, city):
        """Save weather data to S3 bucket"""
        if not weather_data:
            return False

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        file_name = f"weather-data/{city}-{timestamp}.json"

        try:
            weather_data["timestamp"] = timestamp
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=json.dumps(weather_data),
                ContentType="application/json",
            )
            print(f"Successfully saved data for {city} to S3")
            return True
        except Exception as e:
            print(f"Error saving to S3: {e}")
            return False


def main():
    dashboard = WeatherDashboard()

    # Create bucket if needed
    dashboard.create_bucket_if_not_exists()

    cities = ["Nairobi", "Cape Town", "Dubai"]

    for city in cities:
        print(f"\nFetching weather for {city}...")
        weather_data = dashboard.fetch_weather(city)
        if weather_data:
            temp = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            humidity = weather_data["main"]["humidity"]
            description = weather_data["weather"][0]["description"]

            print(f"Temperature: {temp}°F")
            print(f"Feels like: {feels_like}°F")
            print(f"Humidity: {humidity}%")
            print(f"Conditions: {description}")

            # Save to S3
            success = dashboard.save_to_s3(weather_data, city)
            if success:
                print(f"Weather data for {city} saved to S3!")
        else:
            print(f"Failed to fetch weather data for {city}")


if __name__ == "__main__":
    main()
