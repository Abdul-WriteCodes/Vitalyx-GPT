# gpt_advice_openrouter.py

import requests

# --- Load API Key ---
try:
    import streamlit as st
    OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY")
except ImportError:
    import os
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# --- GPT Advice Function ---
def get_health_advice_openrouter(condition, value):
    if not OPENROUTER_API_KEY:
        return "❌ API key is missing. Please set OPENROUTER_API_KEY in .streamlit/secrets.toml or as an environment variable."

    prompt = (
        f"You are a friendly health assistant. Provide short, helpful advice in bullet points "
        f"for a person with a health condition: {condition}. Their risk score is {value}. "
        f"Focus on practical, supportive lifestyle or medical advice."
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "Vitalyx-GPT"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )

        data = response.json()

        if response.status_code == 200 and "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            # Show the error message from OpenRouter if available
            return f"❌ Error: {data.get('error', 'Unexpected response')}"
    except Exception as e:
        return f"⚠️ Exception while fetching advice: {str(e)}"
