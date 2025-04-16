import streamlit as st
 
 # --- Conversion Data ---
 CONVERSION_FACTORS = {
     "Length": {
         "Meters (m)": 1.0,
         "Kilometers (km)": 1000.0,
         "Centimeters (cm)": 0.01,
         "Millimeters (mm)": 0.001,
         "Miles (mi)": 1609.34,
         "Yards (yd)": 0.9144,
         "Feet (ft)": 0.3048,
         "Inches (in)": 0.0254,
     },
     "Mass": {
         "Kilograms (kg)": 1.0,
         "Grams (g)": 0.001,
         "Milligrams (mg)": 1e-6,
         "Metric Tonnes (t)": 1000.0,
         "Pounds (lb)": 0.453592,
         "Ounces (oz)": 0.0283495,
     },
     "Temperature": {
         # Special handling needed for Temperature due to offset
         "Celsius (°C)": "celsius",
         "Fahrenheit (°F)": "fahrenheit",
         "Kelvin (K)": "kelvin",
     },
     "Time": {
         "Seconds (s)": 1.0,
         "Minutes (min)": 60.0,
         "Hours (hr)": 3600.0,
         "Days (d)": 86400.0,
         "Weeks (wk)": 604800.0,
     },
     "Area": {
         "Square Meters (m²)": 1.0,
         "Square Kilometers (km²)": 1e6,
         "Square Miles (mi²)": 2.59e6,
         "Acres (ac)": 4046.86,
         "Hectares (ha)": 10000.0,
         "Square Feet (ft²)": 0.092903,
         "Square Inches (in²)": 0.00064516,
     },
     "Volume": {
         "Cubic Meters (m³)": 1.0,
         "Liters (L)": 0.001,
         "Milliliters (mL)": 1e-6,
         "Gallons (US gal)": 0.00378541,
         "Quarts (US qt)": 0.000946353,
         "Pints (US pt)": 0.000473176,
         "Cups (US cup)": 0.000236588,
         "Fluid Ounces (US fl oz)": 2.95735e-5,
         "Cubic Feet (ft³)": 0.0283168,
         "Cubic Inches (in³)": 1.63871e-5,
     },
     "Speed": {
         "Meters per second (m/s)": 1.0,
         "Kilometers per hour (km/h)": 0.277778,
         "Miles per hour (mph)": 0.44704,
         "Feet per second (ft/s)": 0.3048,
         "Knots (kn)": 0.514444,
     },
 }
 
 # --- Temperature Conversion Functions ---
 def celsius_to_fahrenheit(c):
     return (c * 9/5) + 32
 
 def fahrenheit_to_celsius(f):
     return (f - 32) * 5/9
 
 def celsius_to_kelvin(c):
     return c + 273.15
 
 def kelvin_to_celsius(k):
     return k - 273.15
 
 def fahrenheit_to_kelvin(f):
     return celsius_to_kelvin(fahrenheit_to_celsius(f))
 
 def kelvin_to_fahrenheit(k):
     return celsius_to_fahrenheit(kelvin_to_celsius(k))
 
 # --- Core Conversion Logic ---
 def convert_units(value, from_unit, to_unit, category):
     """Converts a value between units within the same category."""
     if category == "Temperature":
         # Handle Temperature separately
         if from_unit == to_unit:
             return value
         if from_unit == "Celsius (°C)":
             if to_unit == "Fahrenheit (°F)": return celsius_to_fahrenheit(value)
             if to_unit == "Kelvin (K)": return celsius_to_kelvin(value)
         elif from_unit == "Fahrenheit (°F)":
             if to_unit == "Celsius (°C)": return fahrenheit_to_celsius(value)
             if to_unit == "Kelvin (K)": return fahrenheit_to_kelvin(value)
         elif from_unit == "Kelvin (K)":
             if to_unit == "Celsius (°C)": return kelvin_to_celsius(value)
             if to_unit == "Fahrenheit (°F)": return kelvin_to_fahrenheit(value)
         # Should not happen if UI is set up correctly
         raise ValueError("Invalid temperature conversion units")
     else:
         # Standard conversion using base unit (Meter for Length, Kg for Mass, etc.)
         factors = CONVERSION_FACTORS[category]
         from_factor = factors[from_unit]
         to_factor = factors[to_unit]
 
         # Convert 'from_unit' to base unit, then base unit to 'to_unit'
         base_value = value * from_factor
         converted_value = base_value / to_factor
         return converted_value
 
 # --- Streamlit UI ---
 st.set_page_config(layout="wide", page_title="Professional Unit Converter")
 
 st.title("🚀 Professional Unit Converter")
 
 
 # Category Selection
 category = st.selectbox("Select Conversion Category:", options=list(CONVERSION_FACTORS.keys()))
 
 # Unit Selection based on Category
 if category:
     units = list(CONVERSION_FACTORS[category].keys())
     col1, col2, col3 = st.columns(3)
 
     with col1:
         from_unit = st.selectbox("From Unit:", options=units, key=f"from_{category}")
     with col2:
         to_unit = st.selectbox("To Unit:", options=units, key=f"to_{category}")
     with col3:
          # Input Value using number_input for better validation
          # Use a format string to prevent excessive decimal places in the input widget
          value_str = st.text_input("Enter Value:", "1.0", key=f"value_{category}")
 
 
     # Perform Conversion and Display Result
     if from_unit and to_unit and value_str:
         try:
             # Attempt to convert input string to float
             value = float(value_str)
 
             # Check if units are the same
             if from_unit == to_unit:
                  result = value
             else:
                 # Perform conversion
                  result = convert_units(value, from_unit, to_unit, category)
 
             st.markdown("---")
             st.subheader("Result:")
 
             # Use columns for better layout of the result
             res_col1, res_col2 = st.columns(2)
             with res_col1:
                  st.metric(label=f"{from_unit}", value=f"{value:,.4f}") # Format input value
             with res_col2:
                  st.metric(label=f"{to_unit}", value=f"{result:,.4f}") # Format result value
 
             # Optional: Display the conversion formula for non-temperature units
             if category != "Temperature":
                  factors = CONVERSION_FACTORS[category]
                  from_f = factors[from_unit]
                  to_f = factors[to_unit]
                  st.caption(f"Calculation: ({value:,.4f} {from_unit} * {from_f}) / {to_f} ≈ {result:,.4f} {to_unit}")
 
 
         except ValueError:
              st.error("Invalid input. Please enter a valid number.")
         except Exception as e:
              st.error(f"An error occurred during conversion: {e}")
 
 
 # Add some padding at the bottom
 st.markdown("<br><br>", unsafe_allow_html=True)
 