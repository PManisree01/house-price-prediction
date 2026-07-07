import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import os

# Load data
data = pd.read_csv('data/house_data.csv')

# Encode Location
data['Location_Encoded'] = data['Location'].map({'Suburb': 0, 'City Center': 1, 'Rural': 2})

# Features and Target
X = data[['Area', 'Bedrooms', 'Bathrooms', 'Age', 'Location_Encoded', 'Parking', 'Floor']]
y = data['Price']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train models
lr = LinearRegression()
rf = RandomForestRegressor(n_estimators=100, random_state=42)

lr.fit(X_train, y_train)
rf.fit(X_train, y_train)

# Evaluate
print("Linear Regression MAE:", mean_absolute_error(y_test, lr.predict(X_test)))
print("Random Forest MAE:", mean_absolute_error(y_test, rf.predict(X_test)))

# Save best model
os.makedirs('models', exist_ok=True)
with open('models/house_price_model.pkl', 'wb') as f:
    pickle.dump(rf, f)

print("✅ Model trained and saved!")

