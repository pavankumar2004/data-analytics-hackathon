import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from utils.data_loader import load_all_data

def run(qualifying, results, drivers):
    st.title("Qualifying vs Race Performance Analysis (Per Driver)")

    # Create a mapping of full driver name to driverId
    driver_mapping = {
        f"{row['forename']} {row['surname']}": row['driverId']
        for _, row in drivers.iterrows()
    }
    # Allow the user to select a driver by name
    selected_driver_name = st.selectbox("Select a Driver", list(driver_mapping.keys()))
    selected_driver_id = driver_mapping[selected_driver_name]

    # Filter qualifying and race data for the selected driver
    qualifying_driver = qualifying[qualifying['driverId'] == selected_driver_id]
    results_driver = results[results['driverId'] == selected_driver_id]

    # Check if sufficient data is available
    if qualifying_driver.empty or results_driver.empty:
        st.error("Not enough data available for this driver.")
        return

    # Merge qualifying and race results on raceId
    merged = pd.merge(
        qualifying_driver,
        results_driver[['raceId', 'positionOrder']],
        on='raceId',
        how='inner',
        suffixes=('_qualifying', '_race')
    )

    # Clean data: drop missing values and convert types
    merged = merged.dropna(subset=['position', 'positionOrder'])
    try:
        merged['position'] = merged['position'].astype(int)
    except Exception:
        st.error("Could not convert qualifying positions to numeric values.")
        return
    merged['positionOrder'] = merged['positionOrder'].astype(int)

    st.subheader(f"Data Overview for {selected_driver_name}")
    st.write("First 5 rows of merged data:")
    st.write(merged.head())

    if len(merged) < 5:
        st.warning("Not enough data points for a reliable analysis.")
        return

    # Calculate correlation between qualifying and race finish positions
    corr = merged['position'].corr(merged['positionOrder'])
    st.write(f"**Correlation** between qualifying position and race finish position: **{corr:.2f}**")

    # -----------------------------
    # Predictive Modeling with Linear Regression
    # -----------------------------
    X = merged[['position']].values  # Qualifying positions as features
    y = merged['positionOrder'].values  # Race finish positions as target

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    
    st.subheader("Predictive Model: Linear Regression")
    st.write(f"**Coefficient:** {model.coef_[0]:.2f}")
    st.write(f"**Intercept:** {model.intercept_:.2f}")
    st.write(f"**R-squared:** {r2:.2f}")
    st.write(f"**RMSE:** {rmse:.2f}")

    # -----------------------------
    # Visualization: Scatter Plot with Regression Line
    # -----------------------------
    st.subheader("Qualifying vs Race Finish Position")
    st.write("The red line indicates the regression line (predicted race finish position).")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='position', y='positionOrder', data=merged, ax=ax, color='blue', label="Actual Data")
    sns.lineplot(x=merged['position'], y=y_pred, color='red', ax=ax, label="Regression Line")
    ax.set_xlabel("Qualifying Position")
    ax.set_ylabel("Race Finish Position")
    ax.set_title(f"Qualifying vs Race Finish Position for {selected_driver_name}")
    st.pyplot(fig)

    # -----------------------------
    # Visualization: Residual Plot
    # -----------------------------
    st.subheader("Residual Analysis")
    residuals = y - y_pred
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x=y_pred, y=residuals, ax=ax2, color='purple')
    ax2.axhline(0, color='red', linestyle='--')
    ax2.set_xlabel("Predicted Race Finish Position")
    ax2.set_ylabel("Residuals")
    ax2.set_title("Residuals vs Predicted Values")
    st.pyplot(fig2)

    # -----------------------------
    # Interactive Prediction for the Selected Driver
    # -----------------------------
    st.subheader("Interactive Prediction")
    st.write("Enter a qualifying position to predict the race finish position for the selected driver.")
    qual_input = st.number_input("Qualifying Position", min_value=1, max_value=50, value=10)
    predicted_finish = model.predict(np.array([[qual_input]]))[0]
    st.write(f"Predicted Race Finish Position for Qualifying Position {qual_input}: **{predicted_finish:.2f}**")

if __name__ == "__main__":
    data = load_all_data('data')
    run(data['qualifying'], data['results'], data['drivers'])
