# Weather App

A modern weather application built with Django that provides real-time weather information for any city using the OpenWeather API.

## Features

- Real-time weather data for any city
- Temperature in Celsius
- Feels like temperature
- Humidity percentage
- Wind speed
- Weather description with icon
- Modern, responsive UI
- Error handling for invalid cities

## Prerequisites

- Python 3.8 or higher
- OpenWeather API key

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the root directory and add your OpenWeather API key:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

## Running the App

1. Make sure your virtual environment is activated
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Start the development server:
   ```bash
   python manage.py runserver
   ```
4. Open your browser and navigate to `http://127.0.0.1:8000`

## Usage

1. Enter a city name in the search box
2. Click the "Search" button or press Enter
3. View the weather information for the specified city

## Technologies Used

- Django
- Python-dotenv
- Requests
- Tailwind CSS
- OpenWeather API 