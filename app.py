import streamlit as st
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt

# Load model
@st.cache_resource
def load_model():
    with open('models/house_price_model.pkl', 'rb') as f:
        return pickle.load(f)

model = load_model()

st.title("🏠 House Price Prediction App")
st.markdown("### AI-powered Real Estate Price Estimator")

col1, col2 = st.columns(2)

with col1:
    area = st.number_input("Area (Square Feet)", 500, 5000, 1500)
    bedrooms = st.number_input("Bedrooms", 1, 6, 3)
    bathrooms = st.number_input("Bathrooms", 1, 5, 2)
    parking = st.selectbox("Parking Availability", [0, 1, 2])

with col2:
    age = st.number_input("Age of Property (Years)", 0, 50, 10)
    floor = st.number_input("Floor Number", 0, 15, 3)
    location = st.selectbox("Location", ["Suburb", "City Center", "Rural"])

if st.button("🔮 Predict Price", type="primary", use_container_width=True):
    loc_encoded = {"Suburb":0, "City Center":1, "Rural":2}[location]
    input_data = np.array([[area, bedrooms, bathrooms, age, loc_encoded, parking, floor]])
    prediction = model.predict(input_data)[0]
    
    if prediction >= 10000000:
        price_str = f"₹ {prediction/10000000:.2f} Crore"
    else:
        price_str = f"₹ {prediction/100000:.2f} Lakh"
    
    st.success(f"**Predicted House Price: {price_str}**")

# Charts
st.subheader("📊 Market Insights")
data = pd.read_csv("data/house_data.csv")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(data["Area"], data["Price"]/100000, alpha=0.7, color='blue')
    ax.set_xlabel("Area (sq.ft)")
    ax.set_ylabel("Price (Lakh)")
    ax.set_title("Area vs Price")
    st.pyplot(fig)

with col2:
    avg_price = data.groupby("Location")["Price"].mean() / 100000
    st.bar_chart(avg_price, use_container_width=True)
    st.caption("Average Price by Location (₹ Lakh)")

st.caption("Built with ❤️ using Python & Streamlit")