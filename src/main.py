import streamlit as st
import os
from utils.data_loader import load_all_data

# Load all datasets
data_directory = os.path.join('data')
data = load_all_data(data_directory)

# Custom CSS to enhance the UI
st.markdown("""
<style>
    .sidebar .sidebar-content {
        background-color: #1f2937;
        color: white;
    }
    .sidebar-content .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .sidebar .sidebar-content .stSelectbox label {
        color: white !important;
    }
    .sidebar .sidebar-content .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }
    .category-header {
        font-weight: bold;
        font-size: 18px;
        color: #facc15;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    .stButton button {
        background-color: #facc15;
        color: black;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏎️ F1 Driver and Team Performance Analysis")

# Sidebar for navigation
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg", width=200)
    st.title("Navigation")
    st.markdown("---")

    # Define session state to track selected menu
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None

    with st.expander("🏁 Driver Analysis"):
        if st.button("Driver Performance"):
            st.session_state.selected_option = "Driver Performance"
        if st.button("Driver Consistency"):
            st.session_state.selected_option = "Driver Consistency"
        if st.button("Head-to-Head Analysis"):
            st.session_state.selected_option = "Head-to-Head Analysis"
        if st.button("Driver Track Struggles"):
            st.session_state.selected_option = "Driver Track Struggles"
    
    with st.expander("🚥 Race Analysis"):
        if st.button("Qualifying vs Race Performance"):
            st.session_state.selected_option = "Qualifying vs Race Performance"
        if st.button("Pit Stop Strategies"):
            st.session_state.selected_option = "Pit Stop Strategies"
        if st.button("Lap Time Efficiency"):
            st.session_state.selected_option = "Lap Time Efficiency"
    
    with st.expander("🏎️ Team Analysis"):
        if st.button("Team Performance"):
            st.session_state.selected_option = "Team Performance"
        if st.button("Best Team Lineup"):
            st.session_state.selected_option = "Best Team Lineup"
        if st.button("Struggling Teams"):
            st.session_state.selected_option = "Struggling Teams"
    
    with st.expander("📊 Predictions and Trends"):
        if st.button("Predict 2025 Season"):
            st.session_state.selected_option = "Predict 2025 Season"
        if st.button("Championship Retention"):
            st.session_state.selected_option = "Championship Retention"
        if st.button("Champion Age Trends"):
            st.session_state.selected_option = "Champion Age Trends"
    
    with st.expander("🔮 Special Analysis"):
        if st.button("Hypothetical Driver Swaps"):
            st.session_state.selected_option = "Hypothetical Driver Swaps"
        if st.button("Driver Movements"):
            st.session_state.selected_option = "Driver Movements"
    
    st.markdown("---")
    st.markdown("Made by Pavan Kumar")

# Display content based on selection
if st.session_state.selected_option:
    st.subheader(f"🔍 {st.session_state.selected_option}")
    
    if st.session_state.selected_option == "Driver Performance":
        import models.driver_performance as driver_performance
        driver_performance.run(data['drivers'], data['results'], data['driver_standings'],data['races'])
    elif st.session_state.selected_option == "Qualifying vs Race Performance":
        import models.qualifying_vs_race as qualifying_vs_race
        qualifying_vs_race.run(data['qualifying'], data['results'],data['drivers'])
    elif st.session_state.selected_option == "Pit Stop Strategies":
        import models.pit_stop_strategies as pit_stop_strategies
        pit_stop_strategies.run(data['pit_stops'], data['results'])
    elif st.session_state.selected_option == "Head-to-Head Analysis":
        import models.head_to_head as head_to_head
        head_to_head.run(data['results'], data['drivers'])
    elif st.session_state.selected_option == "Hypothetical Driver Swaps":
        import models.hypothetical_swaps as hypothetical_swaps
        hypothetical_swaps.run(data['results'], data['drivers'], data['driver_standings'])
    elif st.session_state.selected_option == "Driver Movements":
        import models.driver_movements as driver_movements
        driver_movements.run(data['results'], data['drivers'], data['constructors'],data['races'])
    elif st.session_state.selected_option == "Team Performance":
        import models.team_performance as team_performance
        team_performance.run(data['results'], data['constructors'])
    elif st.session_state.selected_option == "Driver Consistency":
        import models.driver_consistency as driver_consistency
        driver_consistency.run(data['results'], data['drivers'],data['constructors'])
    elif st.session_state.selected_option == "Lap Time Efficiency":
        import models.lap_time_efficiency as lap_time_efficiency
        lap_time_efficiency.run(data['lap_times'], data['races'])
    elif st.session_state.selected_option == "Best Team Lineup":
        import models.best_team_lineup as best_team_lineup
        best_team_lineup.run()
    elif st.session_state.selected_option == "Predict 2025 Season":
        import models.predict_2025 as predict_2025
        predict_2025.run(data['driver_standings'], data['results'], data['races'],data['drivers'],data['races'])
    elif st.session_state.selected_option == "Struggling Teams":
        import models.struggling_teams as struggling_teams
        struggling_teams.run(data['results'], data['constructors'])
    elif st.session_state.selected_option == "Driver Track Struggles":
        import models.track_struggles as track_struggles
        track_struggles.run(data['results'], data['races'], data['drivers'])
    elif st.session_state.selected_option == "Championship Retention":
        import models.championship_retention as championship_retention
        championship_retention.run()
    elif st.session_state.selected_option == "Champion Age Trends":
        import models.champion_age_trends as champion_age_trends
        champion_age_trends.run(data['driver_standings'], data['races'], data['drivers'])