import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from utils.data_loader import load_all_data
import matplotlib.pyplot as plt

# Load all datasets
data_directory = 'data'  # Adjust the path as necessary
data = load_all_data(data_directory)

# Extract datasets
races = data['races']
drivers = data['drivers']
constructors = data['constructors']
driver_standings = data['driver_standings']
constructor_standings = data['constructor_standings']

# Helper function: Ensure DataFrame has a specific column name
def ensure_column(df, possible_names, default_name):
    """
    Ensure that the DataFrame df has a column named default_name.
    If any of the possible_names exist, rename it to default_name.
    """
    for col in possible_names:
        if col in df.columns:
            if col != default_name:
                df.rename(columns={col: default_name}, inplace=True)
            return df
    st.error(f"DataFrame does not contain any of the expected columns: {possible_names}")
    return df

def predict_champion(driver_standings, races, drivers):
    """
    Predict the driver champion for 2025:
    1. Merge driver standings with race years.
    2. Aggregate season total points per driver.
    3. For each driver with at least 2 seasons of data, fit a linear regression
       on (year vs points) and forecast 2025 points.
    4. Return the driver with the highest predicted points.
    """
    ds = pd.merge(driver_standings, races[['raceId', 'year']], on='raceId', how='left')
    season_points = ds.groupby(['year', 'driverId'])['points'].sum().reset_index()
    
    predictions = []
    for driver in season_points['driverId'].unique():
        driver_data = season_points[season_points['driverId'] == driver].sort_values('year')
        if driver_data.shape[0] >= 2:
            X = driver_data[['year']].values
            y = driver_data['points'].values
            model = LinearRegression()
            model.fit(X, y)
            pred = model.predict(np.array([[2025]]))[0]
        else:
            pred = driver_data['points'].mean()
        predictions.append({'driverId': driver, 'predicted_points': pred})
    predictions_df = pd.DataFrame(predictions)
    
    champion_pred = predictions_df.loc[predictions_df['predicted_points'].idxmax()]
    champion_driver = drivers[drivers['driverId'] == champion_pred['driverId']]
    champion_name = champion_driver.iloc[0]['forename'] + " " + champion_driver.iloc[0]['surname']
    return champion_name, champion_pred['predicted_points'], predictions_df

def predict_constructor_champion(constructor_standings, races, constructors):
    """
    Predict the constructor champion for 2025:
    1. Merge constructor standings with race years.
    2. Aggregate season total points per constructor.
    3. For each constructor with at least 2 seasons of data, fit a linear regression
       on (year vs points) and forecast 2025 points.
    4. Return the constructor with the highest predicted points.
    """
    cs = pd.merge(constructor_standings, races[['raceId', 'year']], on='raceId', how='left')
    season_points = cs.groupby(['year', 'constructorId'])['points'].sum().reset_index()
    
    predictions = []
    for cons in season_points['constructorId'].unique():
        cons_data = season_points[season_points['constructorId'] == cons].sort_values('year')
        if cons_data.shape[0] >= 2:
            X = cons_data[['year']].values
            y = cons_data['points'].values
            model = LinearRegression()
            model.fit(X, y)
            pred = model.predict(np.array([[2025]]))[0]
        else:
            pred = cons_data['points'].mean()
        predictions.append({'constructorId': cons, 'predicted_points': pred})
    predictions_df = pd.DataFrame(predictions)
    
    # Debugging: Print the constructors DataFrame columns
    st.write("Constructors DataFrame Columns:", constructors.columns)
    
    # Ensure the constructorId column exists
    if 'constructorId' not in constructors.columns:
        st.error("The 'constructorId' column is missing from the constructors DataFrame.")
        return None, None, None
    
    champion_pred = predictions_df.loc[predictions_df['predicted_points'].idxmax()]
    champion_constructor = constructors[constructors['constructorId'] == champion_pred['constructorId']]
    champion_name = champion_constructor.iloc[0]['name']
    return champion_name, champion_pred['predicted_points'], predictions_df

def run(driver_standings, constructor_standings, races, drivers, constructors):
    st.title("F1 2025 Season Predictions: Champion Driver & Constructor")

    # --- Driver Championship Prediction ---
    st.header("Driver Championship Prediction")
    if st.button("Predict Driver Champion"):
        champ_driver, pred_points_driver, driver_preds = predict_champion(driver_standings, races, drivers)
        st.write(f"**Predicted Champion Driver for 2025:** {champ_driver}")
        st.write(f"**Predicted Season Points:** {pred_points_driver:.2f}")
        st.subheader("Driver Predictions (All)")
        st.dataframe(driver_preds)
        
        # Optional: Plot historical vs. predicted points for the predicted champion
        ds = pd.merge(driver_standings, races[['raceId', 'year']], on='raceId', how='left')
        season_points = ds.groupby(['year', 'driverId'])['points'].sum().reset_index()
        driver_id = driver_preds.loc[driver_preds['predicted_points'].idxmax(), 'driverId']
        driver_data = season_points[season_points['driverId'] == driver_id].sort_values('year')
        if not driver_data.empty:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(driver_data['year'], driver_data['points'], marker='o', label='Historical Points')
            ax.plot(2025, pred_points_driver, marker='X', markersize=10, color='red', label='Predicted 2025')
            ax.set_title(f"Historical & Predicted Points for {champ_driver}")
            ax.set_xlabel("Year")
            ax.set_ylabel("Total Season Points")
            ax.legend()
            st.pyplot(fig)

    # --- Constructor Championship Prediction ---
    st.header("Constructor Championship Prediction")
    if st.button("Predict Constructor Champion"):
        champ_constructor, pred_points_cons, cons_preds = predict_constructor_champion(constructor_standings, races, constructors)
        st.write(f"**Predicted Champion Constructor for 2025:** {champ_constructor}")
        st.write(f"**Predicted Season Points:** {pred_points_cons:.2f}")
        st.subheader("Constructor Predictions (All)")
        st.dataframe(cons_preds)
        
        # Optional: Plot historical vs. predicted points for the predicted champion
        cs = pd.merge(constructor_standings, races[['raceId', 'year']], on='raceId', how='left')
        season_points_cons = cs.groupby(['year', 'constructorId'])['points'].sum().reset_index()
        cons_id = cons_preds.loc[cons_preds['predicted_points'].idxmax(), 'constructorId']
        cons_data = season_points_cons[season_points_cons['constructorId'] == cons_id].sort_values('year')
        if not cons_data.empty:
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            ax2.plot(cons_data['year'], cons_data['points'], marker='o', label='Historical Points')
            ax2.plot(2025, pred_points_cons, marker='X', markersize=10, color='red', label='Predicted 2025')
            ax2.set_title(f"Historical & Predicted Points for {champ_constructor}")
            ax2.set_xlabel("Year")
            ax2.set_ylabel("Total Season Points")
            ax2.legend()
            st.pyplot(fig2)

if __name__ == "__main__":
    run(data['driver_standings'], data['constructor_standings'], races, drivers, constructors)
