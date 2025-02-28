import streamlit as st
import requests

# Custom CSS for professional UI/UX, gradient background, and dark mode
st.markdown("""
    <style>
    /* Gradient background */
    body {
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        font-family: 'Arial', sans-serif;
        color: #ffffff;
    }
    .stApp {
        background: transparent;
    }
    /* General styling */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stSelectbox>div>div>div {
        color: #4CAF50;
    }
    .stNumberInput>div>div>input {
        color: #4CAF50;
    }
    .stMarkdown h1 {
        color: #ffffff;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .stMarkdown h2 {
        color: #ffffff;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    .stMarkdown h3 {
        color: #ffffff;
        font-size: 1.75rem;
        margin-bottom: 1rem;
    }
    .css-1d391kg {
        padding: 1.5rem;
        border-radius: 12px;
        background-color: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    /* Dark mode styling */
    .dark-mode {
        background: linear-gradient(135deg, #1e1e1e, #2d2d2d);
        color: #ffffff;
    }
    .dark-mode .stMarkdown h1, .dark-mode .stMarkdown h2, .dark-mode .stMarkdown h3 {
        color: #4CAF50;
    }
    .dark-mode .css-1d391kg {
        background-color: rgba(45, 45, 45, 0.8);
        color: #ffffff;
    }
    .dark-mode .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .dark-mode .stButton>button:hover {
        background-color: #45a049;
    }
    .dark-mode .stSelectbox>div>div>div {
        color: #4CAF50;
    }
    .dark-mode .stNumberInput>div>div>input {
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# Dark mode toggle
dark_mode = st.sidebar.checkbox("Dark Mode 🌙")

if dark_mode:
    st.markdown('<div class="dark-mode">', unsafe_allow_html=True)

# Title
st.title("📏 Ultimate Unit Converter")

# Sidebar for unit categories
unit_category = st.sidebar.selectbox("Select Unit Category", [
    "Length", "Weight", "Temperature", "Volume", "Time", "Speed", "Currency"
])

# Conversion functions
def convert_length(value, from_unit, to_unit):
    length_conversions = {
        "Meter": 1,
        "Kilometer": 0.001,
        "Centimeter": 100,
        "Millimeter": 1000,
        "Inch": 39.3701,
        "Foot": 3.28084,
        "Yard": 1.09361,
        "Mile": 0.000621371
    }
    return value * (length_conversions[to_unit] / length_conversions[from_unit])

def convert_weight(value, from_unit, to_unit):
    weight_conversions = {
        "Kilogram": 1,
        "Gram": 1000,
        "Milligram": 1e+6,
        "Pound": 2.20462,
        "Ounce": 35.274
    }
    return value * (weight_conversions[to_unit] / weight_conversions[from_unit])

def convert_temperature(value, from_unit, to_unit):
    if from_unit == "Celsius":
        if to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif to_unit == "Kelvin":
            return value + 273.15
        else:
            return value
    elif from_unit == "Fahrenheit":
        if to_unit == "Celsius":
            return (value - 32) * 5/9
        elif to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
        else:
            return value
    elif from_unit == "Kelvin":
        if to_unit == "Celsius":
            return value - 273.15
        elif to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32
        else:
            return value

def convert_volume(value, from_unit, to_unit):
    volume_conversions = {
        "Liter": 1,
        "Milliliter": 1000,
        "Gallon": 0.264172,
        "Quart": 1.05669,
        "Pint": 2.11338,
        "Cup": 4.22675,
        "Fluid Ounce": 33.814
    }
    return value * (volume_conversions[to_unit] / volume_conversions[from_unit])

def convert_time(value, from_unit, to_unit):
    time_conversions = {
        "Second": 1,
        "Minute": 1/60,
        "Hour": 1/3600,
        "Day": 1/86400,
        "Week": 1/604800,
        "Month": 1/2.628e+6,
        "Year": 1/3.154e+7
    }
    return value * (time_conversions[to_unit] / time_conversions[from_unit])

def convert_speed(value, from_unit, to_unit):
    speed_conversions = {
        "Meter/Second": 1,
        "Kilometer/Hour": 3.6,
        "Mile/Hour": 2.23694,
        "Foot/Second": 3.28084,
        "Knot": 1.94384
    }
    return value * (speed_conversions[to_unit] / speed_conversions[from_unit])

def convert_currency(value, from_unit, to_unit):
    API_KEY = "03f89d713e8e162d6a456a7d"  # Replace with your API key
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_unit}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes (4xx, 5xx)
        data = response.json()
        
        if data["result"] == "error":
            st.error(f"API Error: {data['error-type']}")
            return None
        
        rate = data["conversion_rates"].get(to_unit)
        if rate is None:
            st.error(f"Currency '{to_unit}' not found in the API response.")
            return None
        
        return value * rate
    
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

# Unit options based on category
if unit_category == "Length":
    units = ["Meter", "Kilometer", "Centimeter", "Millimeter", "Inch", "Foot", "Yard", "Mile"]
    conversion_function = convert_length
elif unit_category == "Weight":
    units = ["Kilogram", "Gram", "Milligram", "Pound", "Ounce"]
    conversion_function = convert_weight
elif unit_category == "Temperature":
    units = ["Celsius", "Fahrenheit", "Kelvin"]
    conversion_function = convert_temperature
elif unit_category == "Volume":
    units = ["Liter", "Milliliter", "Gallon", "Quart", "Pint", "Cup", "Fluid Ounce"]
    conversion_function = convert_volume
elif unit_category == "Time":
    units = ["Second", "Minute", "Hour", "Day", "Week", "Month", "Year"]
    conversion_function = convert_time
elif unit_category == "Speed":
    units = ["Meter/Second", "Kilometer/Hour", "Mile/Hour", "Foot/Second", "Knot"]
    conversion_function = convert_speed
elif unit_category == "Currency":
    units = ["USD", "EUR", "GBP", "INR", "JPY", "AUD", "CAD", "PKR"]  # Added PKR here
    conversion_function = convert_currency

# Input fields
col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("From", units)
with col2:
    to_unit = st.selectbox("To", units)

value = st.number_input("Enter value", value=1.0)

# Real-time conversion
if value is not None:
    converted_value = conversion_function(value, from_unit, to_unit)
    if converted_value is not None:
        st.success(f"**Converted Value:** {converted_value:.2f} {to_unit}")

# History feature
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Add to History"):
    if converted_value is not None:
        st.session_state.history.append(
            f"{value} {from_unit} = {converted_value:.2f} {to_unit}"
        )

if st.session_state.history:
    st.subheader("Conversion History")
    for item in st.session_state.history:
        st.write(item)

# Dark mode closing tag
if dark_mode:
    st.markdown('</div>', unsafe_allow_html=True)