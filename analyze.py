import pandas as pd
import matplotlib.pyplot as plt

def error(df, df_original, column_name):
    """
    Calculate the error between the values in a column of a DataFrame and the last value before each timestamp.

    Args:
        df (pandas.DataFrame): The DataFrame containing the values.
        df_original (pandas.DataFrame): The original DataFrame containing the timestamps and values.
        column_name (str): The name of the column to calculate the error for.

    Returns:
        list: A list of absolute differences between the values in the specified column and the last value before each timestamp.

    Raises:
        ValueError: If the specified column does not exist in the DataFrame.
    """
    
    diff = []
    # Check if the column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"The column '{column_name}' does not exist in the DataFrame.")

    def last_value_before(timestamp):
        if df[df['time'] <= timestamp].empty:
            raise ValueError("No point before the date")
        return df[df['time'] <= timestamp].iloc[-1]
    
    for i in range(1, len(df_original)):
        try:
            diff.append(abs(df_original["value"].iloc[i] - last_value_before(df_original["time"].iloc[i])["value"]))
        except ValueError:
                    continue

    return diff



def plot_histogram(data_series, bins=10, title="Distribution of Absolute Differences"):
    """
    Plots a histogram of the given data series.

    Parameters:
    - data_series (array-like): The data series to plot the histogram for.
    - bins (int): The number of bins to use for the histogram. Default is 10.
    - title (str): The title of the histogram plot. Default is "Distribution of Absolute Differences".

    Returns:
    None
    """
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 4))  # Set the figure size for better readability
    plt.hist(data_series, bins=bins, color='blue', alpha=0.7, edgecolor='black')
    plt.title(title)
    plt.xlabel('Absolute Difference')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

def compute_efficiency(df):
    """
    Compute the efficiency of a data frame. i.e the time taken to collect each data point.

    Parameters:
    df (pandas.DataFrame): The input data frame.

    Returns:
    float: The efficiency value.

    """
    # compute the time difference between the first and last point
    time_diff = df["time"].iloc[-1] - df["time"].iloc[0]
    # compute the number of points
    num_points = len(df)
    # compute the efficiency
    efficiency = time_diff.total_seconds() / num_points
    return efficiency

def hourly_rate_of_change(df):
    """
    Calculate the average absolute rate of change per hour for a given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.

    Returns:
        pandas.Series: A Series containing the average absolute rate of change per hour.

    Raises:
        ValueError: If the DataFrame does not include 'time' and 'value' columns, or if it is empty.
        ValueError: If the 'time' column is not of datetime type.

    """
    
    # Check if required columns exist
    if 'time' not in df.columns or 'value' not in df.columns:
        raise ValueError("DataFrame must include 'time' and 'value' columns.")
    
    # Check if the DataFrame is empty
    if df.empty:
        raise ValueError("The DataFrame is empty.")
    
    # Ensure 'time' is of datetime type
    if not pd.api.types.is_datetime64_any_dtype(df['time']):
        raise ValueError("'time' column must be of datetime type.")

    # Calculate the difference between consecutive entries
    df['time_diff'] = df['time'].diff().dt.total_seconds() / 3600  # Convert time difference to hours
    df['value_diff'] = df['value'].diff()

    # Calculate the rate of change in degrees per hour, and take the absolute value
    df['rate_of_change'] = (df['value_diff'] / df['time_diff']).abs()

    # Extract the hour from each datetime
    df['hour'] = df['time'].dt.hour

    # Group by hour and calculate the average absolute rate of change for each hour
    hourly_avg_abs_rate = df.groupby('hour')['rate_of_change'].mean()

    return hourly_avg_abs_rate
