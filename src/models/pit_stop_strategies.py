import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from utils.data_loader import load_all_data
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def run(pit_stops, results):
    st.title("Pit Stop Strategies Analysis & Predictive Modeling")

    # ---------------------------
    # Pit Stop Analysis
    # ---------------------------
    # Compute pit stop counts and total durations per driver per race
    pit_stop_counts = pit_stops.groupby(['raceId', 'driverId']).size().reset_index(name='pit_stop_count')
    pit_stop_durations = pit_stops.groupby(['raceId', 'driverId'])['milliseconds'].sum().reset_index(name='total_pit_time')
    
    # Merge counts and durations
    pit_analysis = pd.merge(pit_stop_counts, pit_stop_durations, on=['raceId', 'driverId'])
    
    # Visualize pit stop count distribution
    st.subheader("Distribution of Pit Stop Counts per Race")
    fig1, ax1 = plt.subplots()
    sns.histplot(pit_analysis['pit_stop_count'], bins=range(1, pit_analysis['pit_stop_count'].max() + 2), ax=ax1)
    ax1.set_title("Distribution of Pit Stop Counts")
    ax1.set_xlabel("Number of Pit Stops")
    st.pyplot(fig1)
    
    # Visualize total pit stop durations distribution (convert ms to seconds)
    st.subheader("Distribution of Total Pit Stop Durations (s)")
    fig2, ax2 = plt.subplots()
    sns.histplot(pit_analysis['total_pit_time'] / 1000, bins=30, kde=True, ax=ax2)
    ax2.set_title("Distribution of Total Pit Stop Durations (s)")
    ax2.set_xlabel("Total Pit Stop Duration (s)")
    st.pyplot(fig2)
    
    # ---------------------------
    # Merge with Race Results for Predictive Modeling
    # ---------------------------
    # Merge pit stop analysis with race results to get finishing position (assumed to be in 'positionOrder')
    merged_data = pd.merge(pit_analysis, results[['raceId', 'driverId', 'positionOrder']], on=['raceId', 'driverId'])
    merged_data = merged_data.dropna(subset=['positionOrder'])
    merged_data['positionOrder'] = merged_data['positionOrder'].astype(int)
    
    st.subheader("Merged Pit Stop and Race Performance Data")
    st.write(merged_data.head())
    
    # Convert pit stop total time from ms to seconds for modeling
    merged_data['total_pit_time_s'] = merged_data['total_pit_time'] / 1000
    
    # ---------------------------
    # Predictive Modeling: Race Finish Position
    # ---------------------------
    st.subheader("Predicting Race Finish Position Based on Pit Stop Strategy")
    st.write("A Random Forest model is trained to predict the finishing position from pit stop count and total pit stop duration (in seconds).")
    
    # Define features and target
    X = merged_data[['pit_stop_count', 'total_pit_time_s']]
    y = merged_data['positionOrder']
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    st.write(f"**RMSE:** {rmse:.2f}")
    st.write(f"**R-squared:** {r2:.2f}")
    
    # Plot Actual vs Predicted Finish Positions
    fig3, ax3 = plt.subplots(figsize=(8,6))
    ax3.scatter(y_test, y_pred, alpha=0.7, color='teal')
    ax3.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    ax3.set_xlabel("Actual Finish Position")
    ax3.set_ylabel("Predicted Finish Position")
    ax3.set_title("Actual vs Predicted Race Finish Position")
    st.pyplot(fig3)
    
    # ---------------------------
    # Interactive Prediction
    # ---------------------------
    st.subheader("Interactive Prediction")
    st.write("Enter pit stop strategy details to predict the race finish position:")
    input_pit_stop_count = st.number_input("Number of Pit Stops", min_value=0, max_value=10, value=2)
    input_total_pit_time = st.number_input("Total Pit Stop Duration (seconds)", min_value=0.0, max_value=300.0, value=60.0)
    
    # Prepare input features and predict
    input_features = pd.DataFrame({
        'pit_stop_count': [input_pit_stop_count],
        'total_pit_time_s': [input_total_pit_time]
    })
    predicted_position = model.predict(input_features)[0]
    st.write(f"Predicted Race Finish Position: **{predicted_position:.2f}**")
    
if __name__ == "__main__":
    data = load_all_data('data')
    run(data['pit_stops'], data['results'])
