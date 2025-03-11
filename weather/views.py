import requests
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .openai_utils import create_openai_client

def index(request):
    return render(request, 'weather/index.html')

def get_weather(request):
    city = request.GET.get('city', 'London')
    description_type = request.GET.get('type', 'short')  # 'short' or 'long'
    api_key = settings.OPENWEATHER_API_KEY
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            weather_data = {
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'wind_speed': data['wind']['speed'],
                'city': data['name'],
                'country': data['sys']['country']
            }

            # Generate detailed description if requested
            if description_type == 'long':
                try:
                    # Use our utility function to create the OpenAI client
                    client = create_openai_client()
                    
                    prompt = f"""
                    Create a natural, conversational description of the current weather in {weather_data['city']}, {weather_data['country']}.
                    Use these details in your description:
                    - Temperature: {weather_data['temperature']}°C
                    - Conditions: {weather_data['description']}
                    - Humidity: {weather_data['humidity']}%
                    - Wind Speed: {weather_data['wind_speed']} m/s
                    Make it sound natural and informative, like a weather reporter would describe it.
                    """
                    
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a friendly weather reporter providing detailed weather information."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=200
                    )
                    weather_data['detailed_description'] = response.choices[0].message.content
                except Exception as e:
                    weather_data['detailed_description'] = f"Error generating description: {str(e)}"

            return JsonResponse(weather_data)
        else:
            return JsonResponse({'error': 'City not found'}, status=404)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
