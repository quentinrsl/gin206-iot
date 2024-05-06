import datetime
from analyze import hourly_rate_of_change

def sample_every_kth_point(df, k):
    """
    Sample every k-th point from a DataFrame.

    Parameters:
    - df: pandas DataFrame
        The DataFrame from which to sample the points.
    - k: int
        The interval between sampled points.

    Returns:
    - sampled_df: pandas DataFrame
        The DataFrame containing the sampled points.
    Raises:
    - ValueError: If k is not a positive integer or if k exceeds the number of rows in the DataFrame.
    """

    # Validate the input to ensure k is positive and does not exceed the DataFrame length
    if k <= 0:
        raise ValueError("k must be a positive integer.")
    if k > len(df):
        raise ValueError("k is greater than the number of rows in the DataFrame.")

    # Sample every k-th point
    sampled_df = df.iloc[::k]
    return sampled_df

def optimal_sample(df, threshold_dT=0.5):
    """
    Returns a subset of the input DataFrame `df` containing rows that have a significant change in value.

    Parameters:
        df (pandas.DataFrame): The input DataFrame.
        threshold_dT (float, optional): The threshold value for the change in value. Defaults to 0.5.

    Returns:
        pandas.DataFrame: A subset of the input DataFrame `df` containing rows with significant changes in value.
    """
    
    t0 = df["time"].iloc[0]
    indices = [0]
    times = [t0]
    for i in range(1, len(df)):
        dT = abs(df["value"].iloc[i] - df["value"].iloc[indices[-1]])
        if dT > threshold_dT:
            times.append(i)
            indices.append(i)
    return df.iloc[indices]
        
def sample_reglin(df, max_dT=0.5, max_poll_interval=2 * 3600):
    """
    Returns a subset of the input DataFrame `df` by sampling points based on a linear regression algorithm.

    Parameters:
    - df (pandas.DataFrame): The input DataFrame containing the time series data.
    - max_dT (float): The value difference that should be considered significant enough to add a new value.
                      Defaults to 0.5.
    - max_poll_interval (int): The maximum time interval allowed between the first and last point in the subset.
                               Defaults to 2 hours (2 * 3600 seconds).

    Returns:
    - pandas.DataFrame: A subset of the input DataFrame `df` containing the sampled points.

    Raises:
    - ValueError: If there is no point before the specified date.

    """
    indices = []

    def get_first_point_after(date):
        if df[df['time'] > date].empty:
            raise ValueError("No point before the date")
        return df[df['time'] > date].iloc[0]

    # Get first two points
    t0 = df["time"].iloc[0]
    t1 = df["time"].iloc[1]

    while True:
        v0 = df[df["time"] == t0]["value"].values[0]
        v1 = df[df["time"] == t1]["value"].values[0]

        # Calculate the slope
        s = abs((v1 - v0) / (t1 - t0).total_seconds())

        # Add max_dT/s to t1
        new_t = t1 + datetime.timedelta(seconds=min(max_dT / s, max_poll_interval))

        try:
            new_t = get_first_point_after(new_t)["time"]
            indices.append(df[df["time"] == new_t].index[0])
            t0 = t1
            t1 = new_t
        except ValueError:
            break

    return df.loc[indices]

def sample_avg_rate_of_change(df, poll_rate):
    """
    Calculate the sample average rate of change for a given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        poll_rate (pandas.Series): The Series containing the poll rates for each hour.

    Returns:
        pandas.DataFrame: The subset of the DataFrame with the indices where the rate of change exceeds the poll rate.

    """
    indices = [0]
    for i in range(len(df)):
        current_hour = df["time"].iloc[i].hour
        if df["time"].iloc[i] - df["time"].iloc[indices[-1]] > datetime.timedelta(seconds=poll_rate.iloc[current_hour]):
            indices.append(i)
    return df.iloc[indices]
