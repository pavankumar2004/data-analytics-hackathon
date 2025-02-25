import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data
def run():
    # Load all datasets
    data_directory = 'data'  # Adjust this path as necessary
    data = load_all_data(data_directory)

    drivers = data['drivers']
    results = data['results']
    driver_standings = data['driver_standings']

    # Compute average points per race for each driver
    driver_races = results.groupby('driverId')['raceId'].nunique()
    driver_points = driver_standings.groupby('driverId')['points'].sum()
    performance = (driver_points / driver_races).sort_values(ascending=False)

    # Build the best team lineup
    best_lineup = performance.head(2)
    driver_names = drivers.set_index('driverId').apply(lambda row: f"{row['forename']} {row['surname']}", axis=1)
    best_lineup = best_lineup.rename(index=driver_names)

    # Streamlit application layout
    st.title("Best Team Lineup")
    st.write("The following drivers are the best team lineup based on average points per race:")
    st.table(best_lineup)