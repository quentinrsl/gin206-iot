def sample_every_kth_point(df, k):
    # Validate the input to ensure k is positive and does not exceed the DataFrame length
    if k <= 0:
        raise ValueError("k must be a positive integer.")
    if k > len(df):
        raise ValueError("k is greater than the number of rows in the DataFrame.")

    # Sample every k-th point
    sampled_df = df.iloc[::k]
    return sampled_df