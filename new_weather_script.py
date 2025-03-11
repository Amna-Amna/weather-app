import requests
import os
import sys
from dotenv import load_dotenv
import time

# Load environment variables first
load_dotenv()

# Important: Explicitly set API keys from environment variables
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENWEATHER_API_KEY or not OPENAI_API_KEY:
    raise ValueError("API keys not found in environment variables")

# Import OpenAI after setting up environment
try:
    import openai
    # Configure the OpenAI API key
    openai.api_key = OPENAI_API_KEY.strip()
except ImportError:
    print("Error: Could not import the OpenAI module. Make sure it's installed with 'pip install openai==0.28.1'")
    sys.exit(1)

def get_weather(city):
    """Get weather data from OpenWeatherMap API"""
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'q': city,
        'units': 'metric',
        'appid': OPENWEATHER_API_KEY.strip()
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)  # Added timeout
        response.raise_for_status()  # Raises exception for 4XX/5XX responses
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
    
    except requests.exceptions.RequestException as e:
        return {'error': f"Network error: {str(e)}"}
    except (KeyError, ValueError, TypeError) as e:
        return {'error': f"Data processing error: {str(e)}"}
    except Exception as e:
        return {'error': f"Error: {str(e)}"}

def display_temperature(weather_data):
    """Display temperature prominently"""
    city = weather_data['city']
    country = weather_data['country']
    temp = weather_data['temperature']
    desc = weather_data['description']
    
    # Create a visually prominent display of the temperature
    print("\n" + "=" * 50)
    print(f"  CURRENT TEMPERATURE IN {city.upper()}, {country}")
    print(f"  {temp}°C")
    print(f"  {desc.capitalize()}")
    print("=" * 50 + "\n")

def generate_weather_description(weather_data):
    """Generate natural language description using OpenAI"""
    prompt = f"""
    Create a natural, conversational description of the current weather in {weather_data['city']}, {weather_data['country']}.
    Use these details in your description:
    - Temperature: {weather_data['temperature']}°C
    - Conditions: {weather_data['description']}
    - Humidity: {weather_data['humidity']}%
    - Wind Speed: {weather_data['wind_speed']} m/s
    Make it sound natural and informative, like a weather reporter would describe it.
    """
    
    try:
        # OpenAI API call with version 0.28.1
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly weather reporter providing detailed weather information."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200,
            request_timeout=30  # Added timeout
        )
        return response.choices[0].message['content']
    except openai.error.AuthenticationError:
        return "Error: Invalid OpenAI API key. Please check your API key and try again."
    except openai.error.RateLimitError:
        return "Error: OpenAI API rate limit exceeded. Please try again later."
    except openai.error.ServiceUnavailableError:
        return "Error: OpenAI service is currently unavailable. Please try again later."
    except openai.error.APIError:
        return "Error: OpenAI API returned an error. Please try again later."
    except Exception as e:
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
        
        # Display temperature prominently immediately after fetching
        display_temperature(weather_data)
        
        # Print raw weather data
        print("\nRaw Weather Data:")
        print("-----------------")
        for key, value in weather_data.items():
            print(f"{key.capitalize()}: {value}")
        
        # Generate and print natural language description
        print("\nGenerating detailed weather description...")
        time.sleep(1)  # Short pause for better UX
        print("\nGenerated Weather Description:")
        print("-----------------------------")
        description = generate_weather_description(weather_data)
        print(description)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == '__main__':
    main() 