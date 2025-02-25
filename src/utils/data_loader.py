import pandas as pd
import os
import numpy as np

def clean_data(df):
    """Cleans and preprocesses a dataframe."""
    df = df.replace("\\N", np.nan)  # Replace missing values represented as '\N' with NaN
    df = df.apply(pd.to_numeric, errors='ignore')  # Convert numerical columns properly
    df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces in column names

    # Fill missing values
    for col in df.columns:
        if df[col].dtype == 'object':  # Categorical column
            df[col] = df[col].fillna(df[col].mode()[0])  # Fill with mode (most frequent value)
        else:  # Numeric column
            df[col] = df[col].fillna(df[col].median())  # Fill with median

    return df

def load_all_data(data_directory):
    """Loads and cleans all datasets from the given directory."""
    
    datasets = {
        'drivers': 'drivers.csv',
        'constructors': 'constructors.csv',
        'results': 'results.csv',
        'races': 'races.csv',
        'pit_stops': 'pit_stops.csv',
        'lap_times': 'lap_times.csv',
        'driver_standings': 'driver_standings.csv',
        'constructor_standings': 'constructor_standings.csv',
        'qualifying': 'qualifying.csv'
    }

    data = {}

    for key, file_name in datasets.items():
        file_path = os.path.join(data_directory, file_name)
        df = pd.read_csv(file_path)
        data[key] = clean_data(df)  # Apply cleaning function to each dataset

    return data
