import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data

# Load all datasets
data_directory = 'data'  # Adjust this path as necessary
data = load_all_data(data_directory)

results = data['results']
drivers = data['drivers']
constructors = data['constructors']

def run(results, drivers, driver_standings):
    def analyze_hypothetical_driver_swaps():
        driver_avg = results.groupby('driverId')['positionOrder'].mean()
        driver_team = results.groupby('driverId')['constructorId'].agg(lambda x: x.mode()[0])
        constructor_avg = results.groupby('constructorId')['positionOrder'].mean()

        driver_performance = pd.DataFrame({'driver_avg': driver_avg, 'constructorId': driver_team})
        driver_performance['team_avg'] = driver_performance['constructorId'].map(constructor_avg)
        driver_performance['delta'] = driver_performance['driver_avg'] - driver_performance['team_avg']

        outperformers = driver_performance[driver_performance['delta'] < -1].sort_values('delta')
        underperformers = driver_performance[driver_performance['delta'] > 1].sort_values('delta', ascending=False)

        st.title("Hypothetical Driver Swaps Analysis")

        if not outperformers.empty and not underperformers.empty:
            best_outperformer = outperformers.iloc[0]
            worst_underperformer = underperformers.iloc[0]

            st.subheader("Drivers outperforming their team's average:")
            st.write(outperformers[['driver_avg', 'team_avg', 'delta']])

            st.subheader("Drivers underperforming relative to their team's average:")
            st.write(underperformers[['driver_avg', 'team_avg', 'delta']])

            st.subheader("Hypothetical Swap Suggestion:")
            st.write(f"Swap {best_outperformer.name} (delta={best_outperformer['delta']:.2f}) with {worst_underperformer.name} (delta={worst_underperformer['delta']:.2f})")
        else:
            st.write("No significant outperformers or underperformers found.")

    analyze_hypothetical_driver_swaps()