import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_loader import load_all_data

# Load all datasets
data_directory = 'data'  # Adjust the path as necessary
data = load_all_data(data_directory)

drivers = data['drivers']
results = data['results']
races = data['races']

def run(results, races, drivers):
    # Function to analyze champion age trends
    def analyze_champion_age_trends():
        driver_season = pd.merge(results, races[['raceId', 'year']], on='raceId')
        season_points = driver_season.groupby(['year', 'driverId'])['points'].sum().reset_index()
        champions = season_points.loc[season_points.groupby('year')['points'].idxmax()].sort_values('year')

        champions = champions.merge(drivers[['driverId', 'dob']], on='driverId')
        champions['dob'] = pd.to_datetime(champions['dob'], errors='coerce')
        champions['age'] = champions['year'] - champions['dob'].dt.year

        return champions

    # Streamlit application layout
    st.title("Champion Age Trends Analysis")

    champion_data = analyze_champion_age_trends()

    if not champion_data.empty:
        st.subheader("Age Distribution of Championship Winners")
        fig, ax = plt.subplots()
        sns.histplot(champion_data['age'].dropna(), bins=15, kde=True, ax=ax)
        ax.set_xlabel("Age")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    else:
        st.write("No data available for analysis.")

run(results, races, drivers)