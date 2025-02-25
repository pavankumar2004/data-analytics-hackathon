import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.data_loader import load_all_data

data_directory = 'data'  # Adjust the path as necessary
data = load_all_data(data_directory)
races = data['races']
constructors = data['constructors']
results = data['results']

def run(results, constructors):
    st.title("F1 Team Performance Analysis")

    # Select a constructor for analysis
    constructor_names = constructors['name'].tolist()
    selected_constructor = st.selectbox("Select a Constructor", constructor_names)

    # Filter results for the selected constructor
    constructor_id = constructors[constructors['name'] == selected_constructor]['constructorId'].values[0]
    constructor_results = results[results['constructorId'] == constructor_id]

    # Calculate average finishing position
    average_position = constructor_results['positionOrder'].mean()
    st.write(f"Average Finishing Position for {selected_constructor}: {average_position:.2f}")
    # Display results for each race
    st.subheader("Race Results")
    race_results = constructor_results[['raceId', 'positionOrder']].merge(
        data['races'][['raceId', 'name']], on='raceId'
    )
    race_results = race_results.rename(columns={'name': 'Race Name', 'positionOrder': 'Finishing Position'})
    st.dataframe(race_results)

    # Visualize the performance
    st.subheader("Performance Over the Season")
    plt.figure(figsize=(10, 5))
    plt.plot(race_results['Race Name'], race_results['Finishing Position'], marker='o')
    plt.xticks(rotation=45)
    plt.title(f"{selected_constructor} Finishing Positions Over the Season")
    plt.xlabel("Race")
    plt.ylabel("Finishing Position")
    plt.grid()
    st.pyplot(plt)
