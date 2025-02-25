import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data

# Load all datasets
data_directory = 'data'  # Adjust the path as necessary
data = load_all_data(data_directory)

constructors = data['constructors']
results = data['results']

def run(results, constructors):
    # Analyze struggling teams
    def analyze_struggling_teams():
        team_finish = results.groupby('constructorId')['positionOrder'].mean()
        constructor_names = constructors.set_index('constructorId')['name']
        team_finish = team_finish.rename(index=constructor_names)
        struggling_team = team_finish.sort_values(ascending=False).head(1)
        return struggling_team

    # Streamlit application layout
    st.title("Struggling Teams Analysis")

    if st.button("Analyze Struggling Teams"):
        struggling_team = analyze_struggling_teams()
        st.write("Team most likely to underperform based on average finishing position:")
        st.write(struggling_team)

