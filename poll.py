import datetime
from analyze import hourly_rate_of_change

def sample_every_kth_point(df, k):
    # Validate the input to ensure k is positive and does not exceed the DataFrame length
    if k <= 0:
        raise ValueError("k must be a positive integer.")
    if k > len(df):
        raise ValueError("k is greater than the number of rows in the DataFrame.")

    # Sample every k-th point
    sampled_df = df.iloc[::k]
    return sampled_df

def optimal_sample(df, threshold_dT=0.5):
    t0 = df["time"].iloc[0]
    indices = [0]
    times = [t0]
    for i in range(1, len(df)):
        dT = abs(df["value"].iloc[i] - df["value"].iloc[indices[-1]])
        if dT > threshold_dT:
            times.append(i)
            indices.append(i)
    return df.iloc[indices]
        
def sample_reglin(df,max_dT=0.5, max_poll_interval=2 * 3600):
    indices = []
    def get_first_point_after(date):
        if(df[df['time'] > date].empty):
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
        #add max_dT/s to t1
        new_t = t1 + datetime.timedelta(seconds=min(max_dT/s, max_poll_interval))
        try:
            new_t = get_first_point_after(new_t)["time"]
            indices.append(df[df["time"] == new_t].index[0])
            t0 = t1
            t1 = new_t
        except ValueError:
            break
    return df.loc[indices]

def sample_avg_rate_of_change(df,poll_rate):
    indices = [0]
    for i in range(len(df)):
        current_hour = df["time"].iloc[i].hour
        if(df["time"].iloc[i] - df["time"].iloc[indices[-1]] > datetime.timedelta(seconds = poll_rate.iloc[current_hour])):
            indices.append(i)
    return df.iloc[indices]
