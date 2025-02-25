import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_loader import load_all_data
from sklearn.linear_model import LinearRegression
import numpy as np

def driver_performance(driver_id, results, driver_standings):
    # Filter data for the selected driver
    driver_results = results[results['driverId'] == driver_id]
    driver_standings_data = driver_standings[driver_standings['driverId'] == driver_id]

    # Calculate performance metrics
    total_races = driver_results['raceId'].nunique()
    total_wins = driver_results[driver_results['positionOrder'] == 1].shape[0]
    total_podiums = driver_results[driver_results['positionOrder'] <= 3].shape[0]
    total_points = driver_standings_data['points'].sum()
    
    return total_races, total_wins, total_podiums, total_points

def predict_future_performance(driver_id, results, races):
    # Merge results with races to get the 'year'
    driver_results = results[results['driverId'] == driver_id].merge(
        races[['raceId', 'year']], on='raceId', how='left'
    )

    # Group by year to sum points per season
    yearly_points = driver_results.groupby('year')['points'].sum().reset_index()

    if len(yearly_points) < 5:
        return None  # Not enough data for prediction
    
    X = yearly_points['year'].values.reshape(-1, 1)
    y = yearly_points['points'].values
    model = LinearRegression()
    model.fit(X, y)
    
    # Generate future years based on the latest year in the data
    latest_year = yearly_points['year'].max()
    future_years = np.array([[latest_year + i] for i in range(1, 4)])
    predictions = model.predict(future_years)
    
    return future_years.flatten(), predictions

def run(drivers, results, driver_standings, races):
    st.title("F1 Driver Performance Analysis")
    st.sidebar.header("User Input")
    
    # Map driver full names to driver IDs
    driver_options = {
        f"{row['forename']} {row['surname']}": row['driverId']
        for _, row in drivers.iterrows()
    }
    selected_driver_name = st.sidebar.selectbox("Select Driver", list(driver_options.keys()))
    selected_driver_id = driver_options[selected_driver_name]
    
    # Get and display performance metrics
    total_races, total_wins, total_podiums, total_points = driver_performance(
        selected_driver_id, results, driver_standings
    )
    
    st.subheader(f"Performance Metrics for {selected_driver_name}")
    st.write(f"Total Races: {total_races}")
    st.write(f"Total Wins: {total_wins}")
    st.write(f"Total Podiums: {total_podiums}")
    st.write(f"Total Points: {total_points}")
    
    # Performance Visualization: Finishing Positions
    st.subheader("Driver Performance Visualization")
    performance_data = results[results['driverId'] == selected_driver_id]
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.countplot(ax=ax1, data=performance_data, x='positionOrder', palette='viridis')
    ax1.set_title(f"Finishing Positions for {selected_driver_name}")
    ax1.set_xlabel("Finishing Position")
    ax1.set_ylabel("Count")
    st.pyplot(fig1)
    
    # Future Performance Prediction
    prediction = predict_future_performance(selected_driver_id, results, races)
    if prediction is not None:
        future_years, predicted_points = prediction
        st.subheader("Predicted Future Performance")
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.plot(future_years, predicted_points, marker='o', linestyle='dashed', 
                 color='red', label='Predicted Points')
        ax2.set_xlabel("Year")
        ax2.set_ylabel("Predicted Points")
        ax2.set_title(f"Predicted Points for {selected_driver_name} in Future Seasons")
        ax2.legend()
        st.pyplot(fig2)
    else:
        st.write("Not enough data to predict future performance.")

if __name__ == "__main__":
    data_directory = '../data'  # Adjust the path as necessary
    data = load_all_data(data_directory)
    run(data['drivers'], data['results'], data['driver_standings'], data['races'])
