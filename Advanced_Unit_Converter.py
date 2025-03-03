import streamlit as st
import requests
import json
from pint import UnitRegistry

# Initialize Unit Registry
ureg = UnitRegistry()

# ✅ Store API Key securely using Streamlit secrets (Avoid hardcoding!)
API_KEY = st.secrets["GEMINI_API_KEY"]  # Use the exact key name from secrets.toml
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def unit_converter(value, from_unit, to_unit):
    """Convert units using Pint library."""
    try:
        result = (value * ureg(from_unit)).to(to_unit)
        return f"{value} {from_unit} is {result:.4f} {to_unit}"
    except Exception as e:
        return f"Error: {str(e)}"

def ai_response(prompt):
    """Get conversion response from Gemini AI."""
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

# ✅ Streamlit App Configuration
st.set_page_config(page_title="AI Unit Converter", page_icon="🔄", layout="centered")
st.title("🔄 AI-Powered Universal Unit Converter")

# Mode Selection
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
        else:
            st.error("Please enter a valid query.")

# Footer
st.markdown("---")
st.caption("Powered by Gemini API | Developed by Muhammad Shayan Ahmed")