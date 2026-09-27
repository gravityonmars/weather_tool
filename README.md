# Streamlit AI Weather Agent

An interactive weather assistant application built with Streamlit, Groq API, and the Open-Meteo API. The app uses an AI agent equipped with function-calling capabilities to fetch live weather data and 5-hour forecasts based on geographical coordinates.

---

## Features

- **AI-Powered Chat Interface**: Conversational UI powered by Groq's LLM (`openai/gpt-oss-120b`).
- **Function Calling / Tool Use**: Automatically extracts latitude and longitude to request live weather data.
- **Real-Time Data**: Integrates with the free Open-Meteo API (no extra API key needed for weather).
- **Conversation Memory**: Maintains recent context (`k=10` turns) for follow-up questions.

---

## Prerequisites

- Python 3.8+
- A [Groq API Key](https://console.groq.com/)

---

## Installation & Setup

1. **Clone the repository** (or navigate to your project directory):
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create and activate a virtual environment** *(optional but recommended)*:
   ```bash
   python -m venv venv
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install the required packages**:
   ```bash
   pip install streamlit groq python-dotenv requests
   ```

4. **Set up Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

---

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```


---

## Example Prompts

- *"What's the current weather in Tokyo?"* (Lat: 35.6762, Lng: 139.6503)
- *"Can you check the forecast for latitude 40.7128 and longitude -74.0060?"*
- *"Will it rain in the next few hours based on those coordinates?"*