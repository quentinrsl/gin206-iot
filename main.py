import pandas as pd
import matplotlib.pyplot as plt
from generate_data import *
from analyze import *
from poll import *

def plot_temperature_data(df, recent_count=None):
    plt.figure(figsize=(10, 5))
    
    # Check if recent_count is specified and valid
    if recent_count is not None and recent_count > 0:
        df = df.tail(recent_count)  # Slice the DataFrame to get the last 'recent_count' rows
    
    plt.plot(df['time'], df['value'], label='Temperature', color='tab:red')
    plt.title('Temperature Over Time')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)  # Rotates the x-axis labels to make them more readable
    plt.tight_layout()  # Adjusts subplot params so that the subplot(s) fits in to the figure area.
    plt.show()

# Load the data from the CSV file
df  = generate_greenhouse_data("datasets/greenhouse.csv")
plot_temperature_data(df)
df2 = sample_every_kth_point(df,50)

diff1 = distribution_of_differences(df, 'value')
diff2 = distribution_of_differences(df2, 'value')

diff1 = diff1[diff1 <= 10]
diff2 = diff2[diff2 <= 10]

plot_histogram(diff1,bins=20, title='Distribution of Absolute Differences (Original Data)')
plot_histogram(diff2, bins=20, title='Distribution of Absolute Differences (Sampled Data)')
