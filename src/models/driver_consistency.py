import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from utils.data_loader import load_all_data

# Load all datasets
data_directory = 'data'  
data = load_all_data(data_directory)

results = data['results']
drivers = data['drivers']

# Analyze driver consistency
def analyze_driver_consistency():
    driver_finish_std = results.groupby('driverId')['positionOrder'].std()
    driver_finish_mean = results.groupby('driverId')['positionOrder'].mean()
    race_counts = results.groupby('driverId')['raceId'].nunique()
    
    consistent_drivers = pd.DataFrame({
        'mean_finish': driver_finish_mean, 
        'std_finish': driver_finish_std, 
        'races': race_counts
    })
    consistent_drivers = consistent_drivers[consistent_drivers['races'] >= 20]
    consistent_drivers = consistent_drivers.sort_values('std_finish')
    
    driver_names = drivers.set_index('driverId').apply(lambda row: f"{row['forename']} {row['surname']}", axis=1)
    consistent_drivers['driver_name'] = consistent_drivers.index.map(driver_names)
    
    return consistent_drivers

# Predictive Model for Driver Performance
def train_performance_model():
    # Creating a binary classification: 1 (Top 5 finish), 0 (Other)
    results['top_5'] = (results['positionOrder'] <= 5).astype(int)

    features = results[['grid', 'laps', 'milliseconds']].fillna(0)  
    target = results['top_5']

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return model, accuracy

# Streamlit UI
def run(drivers,results,constructors):
    st.title("Driver Performance & Consistency Analysis")
    st.write("This dashboard provides insights on driver consistency and performance predictions.")

    consistent_drivers = analyze_driver_consistency()
    st.subheader("Top 10 Most Consistent Drivers")
    st.dataframe(consistent_drivers[['driver_name', 'mean_finish', 'std_finish', 'races']].head(10))

    # Predictive Model
    model, accuracy = train_performance_model()
    st.subheader(f"Driver Performance Prediction Model (Accuracy: {accuracy:.2f})")

    # User input for predictions
    st.write("Predict whether a driver will finish in the Top 5:")
    grid = st.number_input("Grid Position", min_value=1, max_value=20, value=10)
    laps = st.number_input("Laps Completed", min_value=30, max_value=80, value=50)
    milliseconds = st.number_input("Total Time (ms)", min_value=50000, max_value=200000, value=100000)

    prediction = model.predict(np.array([[grid, laps, milliseconds]]))[0]
    result = "Top 5 Finish" if prediction == 1 else "Below Top 5"
    st.write(f"Prediction: **{result}**")

# Run Streamlit App
if __name__ == "__main__":
    run()
