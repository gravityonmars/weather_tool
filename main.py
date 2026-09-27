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


# print(get_weather(27.7017, 85.3206)) 

def get_weather_tool_properties():
    return {
        "type": "function",
        "function":{
            "name": "get_weather",
            "description": """Get the weather information of a city using the city's latitude and longitude. 
            it provides current weather and next 5 hours weather information.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {
                        "type": "number",
                        "description": "Latitude of the city"
                    },
                    "lng": {
                        "type": "number",
                        "description": "Longitude of the city"
                    }
                },
                "required": ["lat", "lng"]
            }
        }
    }

def run_weather_agent(user_input):
    system_prompt = {
        "role": "system",
        "content": """You are a helpful assistant that can answer questions about the weather in different cities. 
        If the user asks about the weather in a specific city, you should use relevant tools to get the inforamation.
        Anything not related to weather information should be answered based on your own knowledge."""
    }

    user_prompt = {
        "role": "user",
        "content": user_input
    }

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[system_prompt, user_prompt],
        max_tokens=1500,
        temperature=0.7,
        tools = [get_weather_tool_properties()],
        tool_choice ="auto"
    )

    tool_call_decisions = response.choices[0].message.tool_calls

    if tool_call_decisions:
        for tool_call in tool_call_decisions:
            if tool_call.function.name == "get_weather":
                lat = json.loads(tool_call.function.arguments).get("lat")
                lng = json.loads(tool_call.function.arguments).get("lng")
                weather_info = get_weather(lat, lng)

                tool_response = {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": "get_weather", 
                    "content": weather_info
                }
                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[system_prompt, user_prompt, tool_response],
                    max_tokens=1500,
                    temperature=0.7,
                    tools = [get_weather_tool_properties()],
                    tool_choice ="auto"
                )

                result = response.choices[0].message.content
    else:
        result = response.choices[0].message.content
    return result

result = run_weather_agent("What is the weather in Kathmandu Nepal?")

print(result)