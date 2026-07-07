import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Load model
@st.cache_resource
def load_model():
    with open('models/house_price_model.pkl', 'rb') as f:
        return pickle.load(f)

model = load_model()

st.title("🏠 House Price Prediction App")

col1, col2 = st.columns(2)

with col1:
    area = st.number_input("Area (Square Feet)", 500, 5000, 1500)
    bedrooms = st.number_input("Bedrooms", 1, 6, 3)
    bathrooms = st.number_input("Bathrooms", 1, 5, 2)
    parking = st.selectbox("Parking Availability", [0, 1, 2])  # 0=None, 1=1 Car, 2=2 Cars

with col2:
    age = st.number_input("Age of Property", 0, 50, 10)
    floor = st.number_input("Floor Number", 0, 15, 3)
    location = st.selectbox("Location", ["Suburb", "City Center", "Rural"])

if st.button("🔮 Predict Price", type="primary"):
    loc_encoded = {"Suburb":0, "City Center":1, "Rural":2}[location]
    input_data = np.array([[area, bedrooms, bathrooms, age, loc_encoded, parking, floor]])
    prediction = model.predict(input_data)[0]
    
    if prediction >= 10000000:
        price_str = f"₹ {prediction/10000000:.2f} Cr"
    else:
        price_str = f"₹ {prediction/100000:.2f} Lakh"
    
    st.success(f"**Predicted Price: {price_str}**")

# Bonus: Show data
if st.checkbox("Show Sample Data"):
    st.dataframe(pd.read_csv("data/house_data.csv"))