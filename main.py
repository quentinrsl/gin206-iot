import pandas as pd
import matplotlib.pyplot as plt
from generate_data import *
from analyze import *
from poll import *

# sort two lists based on the first list
def sort(X,Y):
    return zip(*sorted(zip(X,Y)))

def plot_temperature_data(df, recent_count=None):
    plt.figure(figsize=(5, 5))
    
    # Check if recent_count is specified and valid
    if recent_count is not None and recent_count > 0:
        df = df.tail(recent_count)  # Slice the DataFrame to get the last 'recent_count' rows
    
    plt.plot(df['time'], df['value'], label='Temperature', color='tab:red', marker='x')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)  # Rotates the x-axis labels to make them more readable
    plt.tight_layout()  # Adjusts subplot params so that the subplot(s) fits in to the figure area.
    plt.show()

def test_sample_every_kth_point(df):
    X = np.arange(1, 10, 1)
    MEAN = []
    STD = []
    MEDIAN = []
    EFFICIENCY = []
    for x in X:
        print(x)
        df_sampled = sample_every_kth_point(df, int(x))
        # plot_temperature_data(df)

        diff = error(df_sampled, df, 'value')

        MEAN.append(np.mean(diff))
        STD.append(np.std(diff))
        MEDIAN.append(np.median(diff))
        EFFICIENCY.append(compute_efficiency(df_sampled))
    
    return X, EFFICIENCY, MEAN, MEDIAN, STD


def example_sample_every_kth_point(k=10):
    df  = generate_greenhouse_data("datasets/greenhouse.csv")
    df = df.tail(150)
    df = sample_every_kth_point(df, k)
    plot_temperature_data(df)

def example_sample_reglin():
    df  = generate_greenhouse_data("datasets/greenhouse.csv")
    df = df.tail(150)
    df = sample_reglin(df)
    plot_temperature_data(df)

def exaample_optimal_sample(dT = 0.3):
    df  = generate_greenhouse_data("datasets/greenhouse.csv")
    df = df.tail(150)
    df = optimal_sample(df, threshold_dT=dT)
    plot_temperature_data(df)

def example_sample_avg_rate_of_change():
    df  = generate_greenhouse_data("datasets/greenhouse.csv")
    hroc = hourly_rate_of_change(df)
    df = df.tail(150)
    df = sample_avg_rate_of_change(df, 3600 * 1 / hroc)
    plot_temperature_data(df)

def test_sample_reglin(df):
    X = np.arange(0.4, 3, 0.05)
    MEAN = []
    STD = []
    MEDIAN = []
    EFFICIENCY = []
    for x in X:
        print(x)
        df_sampled = sample_reglin(df, max_dT=x)
        # plot_temperature_data(df)

        diff = error(df_sampled, df, 'value')

        MEAN.append(np.mean(diff))
        STD.append(np.std(diff))
        MEDIAN.append(np.median(diff))
        EFFICIENCY.append(compute_efficiency(df_sampled))
    return X, EFFICIENCY, MEAN, MEDIAN, STD


def test_optimal_sample(df):
    X = np.arange(0.1, 3, 0.05)
    MEAN = []
    STD = []
    MEDIAN = []
    EFFICIENCY = []
    for x in X:
        print(x)
        df_sampeld= optimal_sample(df, threshold_dT=x)
        # plot_temperature_data(df)

        diff = error(df_sampeld,df, 'value')

        MEAN.append(np.mean(diff))
        STD.append(np.std(diff))
        MEDIAN.append(np.median(diff))
        EFFICIENCY.append(compute_efficiency(df_sampeld))
    return X, EFFICIENCY, MEAN, MEDIAN, STD

def test_sample_avg_rate_of_change(df,hourly_rate_of_change):
    X = np.arange(0.01, 3, 0.05)
    MEAN = []
    STD = []
    MEDIAN = []
    EFFICIENCY = []
    for x in X:
        print(x)
        df_sampled = sample_avg_rate_of_change(df, 3600 * x / hourly_rate_of_change)
        # plot_temperature_data(df)

        diff = error(df_sampled, df, 'value')

        MEAN.append(np.mean(diff))
        STD.append(np.std(diff))
        MEDIAN.append(np.median(diff))
        EFFICIENCY.append(compute_efficiency(df_sampled))
    return X, EFFICIENCY, MEAN, MEDIAN, STD

def comparaison_mean(df,limit=1000):
    plt.figure(figsize=(10, 5))
    hroc = hourly_rate_of_change(df)
    df = df.tail(limit)
    X, EFFICIENCY, MEAN, MEDIAN, STD = test_sample_every_kth_point(df)
    MEAN, EFFICIENCY = sort(MEAN, EFFICIENCY)
    plt.plot( MEAN,EFFICIENCY, label="Constant Polling Interval", marker='x')

    X, EFFICIENCY, MEAN, MEDIAN, STD = test_sample_reglin(df)
    MEAN, EFFICIENCY = sort(MEAN, EFFICIENCY)
    plt.plot( MEAN,EFFICIENCY, label="Linear Regression", marker='x')

    X, EFFICIENCY, MEAN, MEDIAN, STD = test_optimal_sample(df)
    MEAN, EFFICIENCY = sort(MEAN, EFFICIENCY)
    plt.plot( MEAN,EFFICIENCY, label="Optimal Polling rate", marker='x')

    X, EFFICIENCY, MEAN, MEDIAN, STD = test_sample_avg_rate_of_change(df,hroc)
    MEAN, EFFICIENCY = sort(MEAN, EFFICIENCY)
    plt.plot( MEAN,EFFICIENCY, label="Hourly Rate of Change", marker='x')

    plt.ylabel("Average seconds between polls")
    plt.xlabel("Average error")
    plt.ylim(0, 8000)
    plt.xlim(0,1.3)

    plt.legend()
    plt.show()

def example_optimal_sample(dT = 0.3):
    df  = generate_greenhouse_data("datasets/greenhouse.csv")
    df = df.tail(1000)
    df = optimal_sample(df, threshold_dT=dT)
    plt.plot(df['time'], df['value'], label='Temperature', color='tab:red', marker='x')
    plt.title('Temperature Over Time')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.legend()
    plt.show()

def histogram_sample_every_kth_point(k=10):
    df  = generate_greenhouse_data("datasets/greenhouse.csv")
    df = df.tail(1000)
    df_sampled = sample_every_kth_point(df, k)
    diff = error(df, df_sampled, 'value')
    plot_histogram(diff)

# histogram_sample_every_kth_point(1)
# df  = generate_greenhouse_data("datasets/greenhouse.csv")
# df = df.tail(1000)

#Comparaison of the mean error with simplex
# df = generate_simplex(interval=600, frequency=10)
# plt.plot(df['time'], df['value'], label='Temperature', color='tab:red', marker='x')
# plt.show()
# comparaison_mean(df)
#Same thing with the greenhouse data
# df = generate_greenhouse_data("datasets/greenhouse.csv")
# df = df.tail(1000)
# plt.plot(df['time'], df['value'], label='Temperature', color='tab:red', marker='x')
# plt.show()
# comparaison_mean(df)

# Temperature rate of change over the day
# df = generate_greenhouse_data("datasets/greenhouse.csv")
# hcor = hourly_rate_of_change(df)
# hcor.plot()
# plt.xlabel("Hour of the day")
# plt.ylabel("Average absolute rate of change (°C/hour)")
# plt.show()
# plt.ylabel("Aboslute rate of change of the temperature (°C/hour)")
# plt.xlabel("Hour of the day")
# plt.show()

df = generate_greenhouse_data("datasets/greenhouse.csv")
comparaison_mean(df, 1000)

# example_sample_every_kth_point(1)
# example_sample_every_kth_point(10)
# exaample_optimal_sample()
# example_sample_reglin()
# example_sample_avg_rate_of_change()
    # Calculate differences between consecutive rows for the specified column