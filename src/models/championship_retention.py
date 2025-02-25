import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data

# Load all datasets
data_directory = 'data'  # Adjust the path as necessary
data = load_all_data(data_directory)

drivers = data['drivers']
results = data['results']
races = data['races']

# Championship Retention Analysis
def analyze_championship_retention():
    driver_season = pd.merge(results, races[['raceId', 'year']], on='raceId')
    season_points = driver_season.groupby(['year', 'driverId'])['points'].sum().reset_index()
    champions = season_points.loc[season_points.groupby('year')['points'].idxmax()].sort_values('year')

    champions['prev_champion'] = champions['driverId'].shift(1)
    champions['retained'] = (champions['driverId'] == champions['prev_champion'])
    retention_rate = champions['retained'].mean()

    return retention_rate
def run():
    # Streamlit application layout
    st.title("F1 Championship Retention Probability Analysis")

    # Analyze and display retention probability
    retention_probability = analyze_championship_retention()
    st.write(f"Championship Retention Probability: {retention_probability * 100:.2f}%")