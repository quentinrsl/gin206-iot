import pandas as pd
import numpy as np
from opensimplex import OpenSimplex
import datetime

def generate_greenhouse_data(filepath):
    """
    Generate filtered greenhouse data from a CSV file.
    
    Parameters:
    filepath (str): The path to the CSV file.
    
    Returns:
    pandas.DataFrame: The filtered greenhouse data.
    """
    
    # Rest of the code...
def generate_greenhouse_data(filepath):

    # Read the CSV file into a DataFrame, parsing 'time' as datetime
    df = pd.read_csv(filepath, parse_dates=["time"], dtype={"id": str, "value": float})
    
    # Compute the absolute differences between consecutive temperature readings
    df['diff'] = df['value'].diff().abs()
    
    # Initial value for 'diff' will be NaN; we can fill it with 0 or a small number
    df['diff'] = df['diff'].fillna(0)
    
    # Filter the DataFrame:
    # 1. Exclude temperature values that are too high (>50) or too low (<-10)
    # 2. Exclude rows where the difference from the previous reading is greater than 6
    filtered_df = df[(df['value'] > 0) & (df['value'] < 50) & (df['diff'] <= 6)]
    
    # Drop the 'diff' column as it's no longer needed after filtering
    filtered_df = filtered_df.drop(columns=['diff'])
    
    return filtered_df


def generate_simplex(start_time=None, end_time=None, interval=600, max_temp=30, min_temp=10, frequency=10):
    """
    Generate a DataFrame with time and temperature values using Simplex noise.

    Parameters:
    - start_time (datetime): The start time for generating the data. If not provided, it defaults to 1 day before the end_time.
    - end_time (datetime): The end time for generating the data. If not provided, it defaults to the current time.
    - interval (int): The time interval in seconds between each data point. Defaults to 600 seconds (10 minutes).
    - max_temp (float): The maximum temperature value. Defaults to 30.
    - min_temp (float): The minimum temperature value. Defaults to 10.
    - frequency (int): The frequency parameter for the Simplex noise generator. Defaults to 10.

    Returns:
    - df (DataFrame): A pandas DataFrame with 'time' and 'value' columns representing the generated time and temperature values.
    """
    
    # Default time settings if none provided
    if end_time is None:
        end_time = datetime.datetime.now()
    if start_time is None:
        start_time = end_time - datetime.timedelta(days=1)
    
    # Calculate the number of samples needed based on the interval
    total_seconds = int((end_time - start_time).total_seconds())
    steps = total_seconds // interval
    
    # Time array
    times = [start_time + datetime.timedelta(seconds=i * interval) for i in range(steps + 1)]
    
    # Simplex noise generator
    simplex = OpenSimplex(seed=np.random.randint(0, 1000))
    
    # Generate noise values and scale them
    temperatures = [simplex.noise2(x=i / frequency, y=0) for i in range(steps + 1)]
    
    # Map Simplex noise output (usually in range [-1, 1]) to the [min_temp, max_temp]
    scaled_temperatures = min_temp + (np.array(temperatures) + 1) / 2 * (max_temp - min_temp)
    
    # Create DataFrame
    df = pd.DataFrame({'time': times, 'value': scaled_temperatures})
    return df
