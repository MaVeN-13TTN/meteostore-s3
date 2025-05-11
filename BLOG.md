# Building a Weather Dashboard with Python, AWS S3, and OpenWeather API: A Complete Guide

Welcome to this comprehensive guide on setting up and running the Weather Dashboard project! This project combines Python programming with cloud services to create a system that fetches and stores weather data. Let's walk through the setup process step by step.

## Prerequisites

Before we begin, make sure you have:
- A GitHub account
- Python installed on your system
- Basic familiarity with command line operations
- An AWS account (free tier is sufficient)
- An OpenWeather API key (free tier)

## Step 1: Fork and Clone the Repository

1. First, visit the project repository:
   ```
   https://github.com/MaVeN-13TTN/meteostore-s3.git
   ```

2. Click the "Fork" button in the top-right corner to create your copy of the repository

3. Clone your forked repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/meteostore-s3.git
   cd meteostore-s3
   ```

## Step 2: Set Up Conda Environment

1. Install Miniconda if you haven't already:
   - Download from: https://docs.conda.io/en/latest/miniconda.html
   - Follow the installation instructions for your operating system

2. Create a new conda environment:
   ```bash
   conda create -n weather-dashboard python=3.9
   ```

3. Activate the environment:
   ```bash
   conda activate weather-dashboard
   ```

## Step 3: Install Required Packages

1. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install the AWS CLI:
   ```bash
   conda install -c conda-forge awscli
   ```

## Step 4: Configure AWS Credentials

1. Get your AWS credentials:
   - Log into AWS Console
   - Go to IAM (Identity and Access Management)
   - Create a new user or select an existing one
   - Create access keys under "Security credentials"
   - Note down the Access Key ID and Secret Access Key

2. Configure AWS CLI:
   ```bash
   aws configure
   ```
   You'll be prompted to enter:
   ```
   AWS Access Key ID [None]: YOUR_ACCESS_KEY
   AWS Secret Access Key [None]: YOUR_SECRET_KEY
   Default region name [None]: us-east-1
   Default output format [None]: json
   ```

## Step 5: Set Up OpenWeather API

1. Sign up for a free API key:
   - Visit: https://openweathermap.org/api
   - Create an account
   - Generate an API key (it may take a few hours to activate)

2. Configure environment variables:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   ```

3. Edit the `.env` file:
   ```ini
   # OpenWeather API Configuration
   OPENWEATHER_API_KEY=your_api_key_here

   # AWS S3 bucket configuration
   AWS_BUCKET_NAME=weather-data
   ```

## Step 6: Run the Application

1. Make sure you're in the project directory and your conda environment is activated:
   ```bash
   conda activate weather-dashboard
   ```

2. Run the weather dashboard:
   ```bash
   python src/weather_dashboard.py
   ```

The application will:
- Create a unique S3 bucket with a random suffix
- Fetch weather data for Nairobi, Cape Town, and Dubai
- Display the current weather conditions
- Save the data to your S3 bucket

## Understanding the Output

When you run the application, you'll see output like this:
```
Debug - Using bucket name: weather-data-12345
Creating bucket weather-data-12345
Successfully created bucket weather-data-12345

Fetching weather for Philadelphia...
Temperature: 28.35°F
Feels like: 15.75°F
Humidity: 51%
Conditions: broken clouds
Successfully saved data for Philadelphia to S3
...
```

## Troubleshooting Common Issues

1. **AWS Credentials Error**
   - Verify your credentials are correct in `~/.aws/credentials`
   - Ensure you have sufficient permissions in AWS IAM

2. **OpenWeather API Key Error**
   - Check if your API key is activated (can take a few hours)
   - Verify the key is correctly set in `.env`

3. **Bucket Creation Error**
   - Ensure your AWS user has S3 permissions
   - Try a different region if you encounter naming conflicts

4. **Python Package Issues**
   - Make sure your conda environment is activated
   - Try reinstalling requirements: `pip install -r requirements.txt --force-reinstall`

## Next Steps

Now that your Weather Dashboard is running, you might want to:
1. Add more cities to monitor
2. Modify the data storage format
3. Create visualizations of the weather data
4. Set up automated running using cron or AWS Lambda
5. Add error notifications via email or Slack

## Conclusion

You now have a functioning weather dashboard that demonstrates several key DevOps concepts:
- Environment management with Conda
- Cloud service integration with AWS
- API integration with OpenWeather
- Secure credential management
- Error handling and logging

Feel free to modify and extend the project to suit your needs. Happy coding!

## Resources

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/index.html)
- [OpenWeather API Documentation](https://openweathermap.org/api)
- [Python Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Conda Documentation](https://docs.conda.io/)
