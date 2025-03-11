import requests
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import logging

# Set environment variables to disable proxies
os.environ['no_proxy'] = '*'
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

# Enable logging for debugging
logging.basicConfig(level=logging.INFO)

load_dotenv()

# Load API keys
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENWEATHER_API_KEY or not OPENAI_API_KEY:
    raise ValueError("API keys not found in environment variables")

def get_weather(city):
    """Get weather data from OpenWeatherMap API"""
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'q': city,
        'units': 'metric',
        'appid': OPENWEATHER_API_KEY.strip()
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            return {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
        else:
            return {'error': f"Error: {data.get('message', 'Unknown error')}"}
    
    except Exception as e:
        return {'error': f"Error: {str(e)}"}

def generate_weather_description(weather_data):
    """Generate natural language description using ChatGPT"""
    try:
        # Create OpenAI client with minimal configuration
        client = OpenAI(api_key=OPENAI_API_KEY.strip())
        logging.info("OpenAI client created successfully")
        
        prompt = f"""
        Create a natural, conversational description of the current weather in {weather_data['city']}, {weather_data['country']}.
        Use these details in your description:
        - Temperature: {weather_data['temperature']}°C
        - Conditions: {weather_data['description']}
        - Humidity: {weather_data['humidity']}%
        - Wind Speed: {weather_data['wind_speed']} m/s
        Make it sound natural and informative, like a weather reporter would describe it.
        """
        
        logging.info("Sending request to OpenAI API")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly weather reporter providing detailed weather information."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        logging.info("Response received from OpenAI API")
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error in generate_weather_description: {str(e)}")
        return f"Error generating description: {str(e)}"

def main():
    try:
        # Get city name from command line or user input
        if len(sys.argv) > 1:
            city = sys.argv[1]
        else:
            city = input("Enter city name: ")
        
        print(f"\nFetching weather data for {city}...")
        
        # Get weather data
        weather_data = get_weather(city)
        
        if 'error' in weather_data:
            print(weather_data['error'])
            return
        
        # Print raw weather data
        print("\nRaw Weather Data:")
        print("-----------------")
        for key, value in weather_data.items():
            print(f"{key.capitalize()}: {value}")
        
        # Generate and print natural language description
        print("\nGenerated Weather Description:")
        print("-----------------------------")
        description = generate_weather_description(weather_data)
        print(description)
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main() 