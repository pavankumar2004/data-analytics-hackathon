import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data

# Load all datasets
data_directory = 'data'  # Adjust the path as necessary
data = load_all_data(data_directory)

results = data['results']
races = data['races']
drivers = data['drivers']

def run(results, races, drivers):
    st.title("Driver Performance on Specific Tracks")

    # Create a mapping from driver's full name to driverId
    driver_options = {
        f"{row['forename']} {row['surname']}": row['driverId']
        for _, row in drivers.iterrows()
    }
    
    # Let the user select a driver by name
    selected_driver_name = st.selectbox("Select a Driver", list(driver_options.keys()))
    selected_driver_id = driver_options[selected_driver_name]

    # Filter results for the selected driver
    driver_results = results[results['driverId'] == selected_driver_id]

    # Merge with races to get track names
    driver_race_data = pd.merge(driver_results, races[['raceId', 'name']], on='raceId', how='left')

    # Calculate average finishing position by track
    track_performance = driver_race_data.groupby('name')['positionOrder'].mean().reset_index()
    track_performance.columns = ['Track', 'Average Finish Position']

    # Display the results
    st.subheader(f"Performance of {selected_driver_name} on Tracks")
    st.write(track_performance)

    # Visualize the performance as a bar chart
    st.bar_chart(track_performance.set_index('Track')['Average Finish Position'])
