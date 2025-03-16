import streamlit as st
import requests
import json

try:
    from pint import UnitRegistry
except ImportError:
    st.error("The 'pint' library is required. Please install it using 'pip install pint'.")
    st.stop()

# Initialize Unit Registry
ureg = UnitRegistry()

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]  # Use the exact key name from secrets.toml
except KeyError:
    st.error("API key not found in Streamlit secrets. Please add it to secrets.toml.")
    st.stop()

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
        response.raise_for_status()  # Raise an error for bad status codes
        result = response.json()
        
        # Extract the AI response
        if "candidates" in result and result["candidates"]:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "AI Error: No valid response from the API."
    except requests.exceptions.RequestException as e:
        return f"AI Error: {str(e)}"
    except KeyError as e:
        return f"AI Error: Invalid response format. {str(e)}"

st.set_page_config(page_title="AI Unit Converter", page_icon="🔄", layout="centered")
st.title("🔄 AI-Powered Universal Unit Converter")

# Mode Selection
mode = st.radio("Choose Mode:", ["Simple", "Advanced"], horizontal=True)

# Define available units
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
    value = st.number_input("Enter value:", min_value=0.0, format="%.2f", placeholder="Enter a number")
    from_unit = st.selectbox("Select from unit:", units[category])
    to_unit = st.selectbox("Select to unit:", units[category])

    if st.button("Convert", use_container_width=True):
        if value is not None:
            result = unit_converter(value, from_unit, to_unit)
            st.success(f"**Result:** {result}")
        else:
            st.error("Please enter a valid value.")

else:
    # Advanced Mode: User types a conversion query
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