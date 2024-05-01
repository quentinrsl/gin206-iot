import pandas as pd
import matplotlib.pyplot as plt

def distribution_of_differences(df, column_name):
    # Check if the column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"The column '{column_name}' does not exist in the DataFrame.")
    
    # Calculate differences between consecutive rows for the specified column
    differences = df[column_name].diff().abs()

    # The first element of differences will be NaN since there's no previous element for the first row
    differences = differences.dropna()  # Remove NaN values

    return differences

def plot_histogram(data_series, bins=10, title="Distribution of Absolute Differences"):
    plt.figure(figsize=(8, 4))  # Set the figure size for better readability
    plt.hist(data_series, bins=bins, color='blue', alpha=0.7, edgecolor='black')
    plt.title(title)
    plt.xlabel('Absolute Difference')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()
