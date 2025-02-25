import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data

# Load all datasets
data_directory = 'data'  # Adjust the path as necessary
data = load_all_data(data_directory)

drivers = data['drivers']
results = data['results']

def run(results, drivers):
    st.title("Head-to-Head Driver Analysis")

    head_to_head = {}
    for race, group in results.groupby('raceId'):
        race_results = group.sort_values('positionOrder')
        drivers_in_race = race_results['driverId'].tolist()
        for i in range(len(drivers_in_race)):
            for j in range(i + 1, len(drivers_in_race)):
                pair = (drivers_in_race[i], drivers_in_race[j])
                head_to_head[pair] = head_to_head.get(pair, 0) + 1

    head_to_head_df = pd.DataFrame([
        {'driver1': pair[0], 'driver2': pair[1], 'head_to_head_wins': wins}
        for pair, wins in head_to_head.items()
    ])

    driver_names = drivers.set_index('driverId').apply(lambda row: f"{row['forename']} {row['surname']}", axis=1)
    head_to_head_df['driver1_name'] = head_to_head_df['driver1'].map(driver_names)
    head_to_head_df['driver2_name'] = head_to_head_df['driver2'].map(driver_names)

    st.write("Head-to-Head Rivalries among Drivers:")
    st.dataframe(head_to_head_df.sort_values(by='head_to_head_wins', ascending=False))

    # Dropdowns to compare any two drivers
    driver_list = drivers.apply(lambda row: f"{row['forename']} {row['surname']}", axis=1).tolist()
    driver1 = st.selectbox("Select First Driver", driver_list, index=0, key='asdfasdf')
    driver2 = st.selectbox("Select Second Driver", driver_list, index=1, key='adsedg')

    # Get driver IDs
    driver1_id = drivers.loc[drivers['forename'] + ' ' + drivers['surname'] == driver1, 'driverId'].values[0]
    driver2_id = drivers.loc[drivers['forename'] + ' ' + drivers['surname'] == driver2, 'driverId'].values[0]

    # Filter head-to-head data
    comparison = head_to_head_df[((head_to_head_df['driver1'] == driver1_id) & (head_to_head_df['driver2'] == driver2_id)) | 
                                  ((head_to_head_df['driver1'] == driver2_id) & (head_to_head_df['driver2'] == driver1_id))]

    if not comparison.empty:
        st.write(f"Head-to-Head Record between {driver1} and {driver2}:")
        st.dataframe(comparison)
    else:
        st.write(f"No direct head-to-head data available for {driver1} and {driver2}.")
