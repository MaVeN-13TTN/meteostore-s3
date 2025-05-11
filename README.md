# Weather Dashboard

Building a weather data collection system using AWS S3 and OpenWeather API

# Weather Data Collection System

## Project Overview
This project is a Weather Data Collection System that demonstrates core DevOps principles by combining:
- External API Integration (OpenWeather API)
- Cloud Storage (AWS S3)
- Infrastructure as Code
- Version Control (Git)
- Python Development
- Error Handling
- Environment Management

## Features
- Fetches real-time weather data for multiple cities
- Displays temperature (°F), humidity, and weather conditions
- Automatically stores weather data in AWS S3 with timestamps
- Supports multiple cities tracking
- Uses random bucket names for unique storage
- Timestamps all data for historical tracking

## Technical Architecture
- **Language:** Python 3.x
- **Cloud Provider:** AWS (S3)
- **External API:** OpenWeather API
- **Dependencies:**
  - boto3 (AWS SDK)
  - python-dotenv
  - requests

## Project Structure
```
meteostore-s3/
  src/
    __init__.py
    weather_dashboard.py
  tests/
    __init__.py
  data/
  delete_bucket.py
  .env
  .env.example
  .gitignore
  BLOG.md
  README.md
  requirements.txt
```

Note: The `data/` directory is intentionally empty as the application stores all weather data in AWS S3 rather than locally.

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/MaVeN-13TTN/meteostore-s3.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your actual API keys:
```ini
# OpenWeather API Configuration
OPENWEATHER_API_KEY=your_api_key_here

# AWS S3 bucket configuration
AWS_BUCKET_NAME=weather-data
```

4. Configure AWS credentials:
```bash
aws configure
```
This will prompt you to enter:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., us-east-1)
- Default output format

5. Run the application:
```bash
python src/weather_dashboard.py
```

## How It Works

1. **Environment Setup**
   - Loads configuration from `.env` file
   - Uses AWS credentials from `aws configure`

2. **Bucket Creation**
   - Creates a unique S3 bucket using the format: `weather-data-[random-number]`
   - Random number ensures unique bucket names for each run

3. **Weather Data Collection**
   - Fetches weather data for Nairobi, Cape Town, and Dubai
   - Displays current conditions including:
     - Temperature (°F)
     - Feels like temperature
     - Humidity percentage
     - Weather conditions

4. **Data Storage**
   - Saves weather data as JSON files in S3
   - Uses timestamp-based naming: `weather-data/[city]-[timestamp].json`
   - Includes metadata for historical tracking

## What I Learned
- AWS S3 bucket creation and management
- Environment variable management for secure API keys
- Python best practices for API integration
- Error handling and logging
- AWS credential management using `aws configure`

## Cleaning Up Resources

The application creates a new S3 bucket with a random name each time it runs. To help manage these resources and avoid unnecessary AWS charges, a cleanup script is provided:

### Using delete_bucket.py

This script allows you to list and delete S3 buckets created by the application.

1. **List all available buckets:**
   ```bash
   python delete_bucket.py --list
   ```
   This will show all S3 buckets in your AWS account.

2. **Delete a specific bucket:**
   ```bash
   python delete_bucket.py weather-data-12345
   ```
   Replace `weather-data-12345` with the actual name of the bucket you want to delete.

The script will:
- Verify the bucket exists
- Delete all objects in the bucket (including versions and delete markers)
- Delete the empty bucket
- Provide detailed feedback during the process

It's recommended to run this script after testing to clean up resources and avoid unnecessary AWS charges.

## Future Enhancements

- Add weather forecasting
- Implement data visualization
- Add more cities
- Create automated testing
- Set up CI/CD pipeline
