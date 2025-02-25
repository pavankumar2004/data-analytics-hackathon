import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_loader import load_all_data

# Load all datasets
data_directory = 'data'  # Adjust the path as necessary
data = load_all_data(data_directory)

lap_times = data['lap_times']
races = data['races']

def run(lap_times, races):
    st.title("Lap Time Efficiency Analysis")

    # Calculate average lap time by circuit
    lap_times['lap_time_sec'] = lap_times['milliseconds'] / 1000
    circuit_avg = lap_times.groupby('raceId')['lap_time_sec'].mean().reset_index()

    # Merge with race names
    circuit_avg = circuit_avg.merge(races[['raceId', 'name']], on='raceId')

    # Display average lap time by circuit
    st.subheader("Average Lap Time by Circuit")
    st.bar_chart(circuit_avg.set_index('name')['lap_time_sec'])

    # Display detailed statistics
    st.subheader("Detailed Statistics")
    st.write(circuit_avg[['name', 'lap_time_sec']].sort_values(by='lap_time_sec'))

