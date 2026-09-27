import requests
import os
import json
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=api_key)

def get_weather(lat, lng):
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=27.7017&longitude=85.3206&current_weather=true&hourly=temperature_2m,apparent_temperature,relative_humidity_2m,windspeed_10m,rain"

        response = requests.get(url)
        data = response.json()

        current_weather = data.get("current_weather", {})
        hourly_data = data.get("hourly", {})

        if not current_weather:
            return "Weather data not available for the specified location."

        result = {
            "current_weather": current_weather,
            "next_5_hours": [
                {
                "time": hourly_data["time"][i],
                "temperature_2m": hourly_data["temperature_2m"][i],
                "apparent_temperature": hourly_data["apparent_temperature"][i],
                "relative_humidity_2m": hourly_data["relative_humidity_2m"][i],
                "windspeed_10m": hourly_data["windspeed_10m"][i],
                "rain": hourly_data["rain"][i]
                }
                for i in range(min(5, len(hourly_data.get("time", []))))
            ]
        }
        return json.dumps(result, indent=4)
    except Exception as e:
        return f"An error occurred while fetching weather data: {str(e)}"


print(get_weather(27.7017, 85.3206)) 
def get_weather_properties():
    pass

def run_weather_tool():
    pass