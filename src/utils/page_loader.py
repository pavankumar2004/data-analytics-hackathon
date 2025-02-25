import streamlit as st
import importlib

def load_page(page, data):
    page_module = page.lower().replace(" ", "_")
    try:
        module = importlib.import_module(f"pages.{page_module}")
        if hasattr(module, 'run'):
            if page == "Driver Performance":
                module.run(data['drivers'], data['results'], data['driver_standings'])
            elif page == "Qualifying vs Race Performance":
                module.run(data['qualifying'], data['results'])
            elif page == "Pit Stop Strategies":
                module.run(data['pit_stops'], data['results'])
            elif page == "Head-to-Head Analysis":
                module.run(data['results'], data['drivers'])
            elif page == "Hypothetical Driver Swaps":
                module.run(data['results'], data['drivers'], data['driver_standings'])
            elif page == "Driver Movements":
                module.run(data['results'], data['drivers'], data['constructors'])
            elif page == "Team Performance":
                module.run(data['results'], data['constructors'])
            elif page == "Driver Consistency":
                module.run(data['results'], data['drivers'])
            elif page == "Lap Time Efficiency":
                module.run(data['lap_times'], data['races'])
            elif page == "Best Team Lineup":
                module.run(data['results'], data['driver_standings'], data['drivers'])
            elif page == "Predict 2025 Season":
                module.run(data['driver_standings'], data['results'], data['races'])
            elif page == "Struggling Teams":
                module.run(data['results'], data['constructors'])
            elif page == "Driver Track Struggles":
                module.run(data['results'], data['races'], data['drivers'])
            elif page == "Championship Retention":
                module.run(data['driver_standings'], data['races'])
            elif page == "Champion Age Trends":
                module.run(data['driver_standings'], data['races'], data['drivers'])
            else:
                st.error(f"No run function found for {page}")
        else:
            st.error(f"No run function found in {page_module}.py")
    except ImportError:
        st.error(f"Failed to import {page_module}.py")