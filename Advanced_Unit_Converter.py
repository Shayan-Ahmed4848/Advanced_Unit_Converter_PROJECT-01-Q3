import streamlit as st
import pyttsx3
import requests
import json
from pint import UnitRegistry

# Initialize unit registry and text-to-speech engine
ureg = UnitRegistry()
engine = pyttsx3.init()

# Set Gemini API Key
API_KEY = "AIzaSyAKAxs8wCaBD2WkXJwHIPpD9UyR05lZ_DQ"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def unit_converter(value, from_unit, to_unit):
    try:
        result = (value * ureg(from_unit)).to(to_unit)
        return f"{value} {from_unit} is {result:.4f} {to_unit}"
    except Exception as e:
        return f"Error: {str(e)}"

def ai_response(prompt):
    try:
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": f"Please convert {prompt}. Provide only the numerical result with units, no additional text."}]
            }]
        }
        
        response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"AI Error: {response.text}"
    except Exception as e:
        return f"AI Error: {str(e)}"

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Text-to-speech error: {str(e)}")

# Streamlit app configuration
st.set_page_config(page_title="AI Unit Converter", page_icon="🔄", layout="centered")
st.title("🔄 AI-Powered Universal Unit Converter")

# Mode selection
mode = st.radio("Choose Mode:", ["Simple", "Advanced"], horizontal=True)

units = {
    "Length": ["meters", "feet", "inches", "kilometers", "miles"],
    "Weight": ["grams", "kilograms", "pounds", "ounces"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Volume": ["liters", "milliliters", "gallons", "cups"],
    "Speed": ["meters per second", "kilometers per hour", "miles per hour"],
    "Area": ["square meters", "square feet", "acres", "hectares"],
    "Time": ["seconds", "minutes", "hours", "days"]
}

if mode == "Simple":
    category = st.selectbox("Select Category:", list(units.keys()))
    value = st.number_input("Enter value:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("Select from unit:", units[category])
    to_unit = st.selectbox("Select to unit:", units[category])

    if st.button("Convert", use_container_width=True):
        result = unit_converter(value, from_unit, to_unit)
        st.success(f"**Result:** {result}")

else:
    user_input = st.text_input("Enter conversion query:", placeholder="e.g., Convert 100 meters to feet")
    if st.button("Convert", use_container_width=True):
        if user_input.strip():
            with st.spinner("Processing with AI..."):
                ai_result = ai_response(user_input)
                st.success(f"**AI Response:** {ai_result}")
                speak(ai_result)
        else:
            st.error("Please enter a valid query.")

# Footer
st.markdown("---")
st.caption("Powered by Gemini API | Developed by Muhammad Shayan Ahmed")
