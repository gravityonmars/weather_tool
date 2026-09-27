import requests
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=api_key)

def get_weather(lat, lng):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&current_weather=true&hourly=temperature_2m,apparent_temperature,relative_humidity_2m,windspeed_10m,rain"

        response = requests.get(url)
        data = response.json()

        current_weather = data.get("current_weather", {})
        hourly_data = data.get("hourly", {})

        if not current_weather:
            return "Weather data not available."

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
        return f"Error: {str(e)}"


def get_weather_tool_properties():
    return {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather information using latitude and longitude.",
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


k = 10
history = []


def run_weather_agent(user_input):
    system_prompt = {
        "role": "system",
        "content": """You are a helpful weather assistant.
        Use the get_weather tool when the user asks about weather.
        Use previous conversation context to understand follow-up questions."""
    }

    user_prompt = {
        "role": "user",
        "content": user_input
    }

    history.append(user_prompt)

    memory_context = [system_prompt] + history[-(k * 2):]

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=memory_context,
        max_tokens=1500,
        temperature=0.7,
        tools=[get_weather_tool_properties()],
        tool_choice="auto"
    )

    assistant_message = response.choices[0].message

    if assistant_message.tool_calls:
        history.append(assistant_message)

        for tool_call in assistant_message.tool_calls:
            if tool_call.function.name == "get_weather":
                arguments = json.loads(tool_call.function.arguments)

                lat = arguments.get("lat")
                lng = arguments.get("lng")

                weather_info = get_weather(lat, lng)

                tool_response_msg = {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": weather_info
                }

                history.append(tool_response_msg)

        full_context = [system_prompt] + history[-(k * 2):]

        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=full_context,
            max_tokens=1500,
            temperature=0.7
        )

        result = response.choices[0].message.content

    else:
        result = assistant_message.content

    history.append({
        "role": "assistant",
        "content": result
    })

    return result

while True:
    user = input("User: ")
    result = run_weather_agent(user)
    print(f"Assistant: {result}\n")