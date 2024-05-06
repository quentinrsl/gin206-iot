import pandas as pd
import matplotlib.pyplot as plt
from generate_data import *
from analyze import *
from poll import *

def sort(X, Y):
    """
    Sorts two lists X and Y in ascending order based on the values in X.

    Args:
        X (list): The first list to be sorted.
        Y (list): The second list to be sorted.

    Returns:
        tuple: A tuple containing the sorted X and Y lists.

    Example:
        X = [3, 1, 2]
        Y = ['c', 'a', 'b']
        sorted_X, sorted_Y = sort(X, Y)
        # sorted_X: [1, 2, 3]
        # sorted_Y: ['a', 'b', 'c']
    """
    return zip(*sorted(zip(X, Y)))

def plot_temperature_data(df, recent_count=None):
    """
    Plots the temperature data from a DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the temperature data.
        recent_count (int, optional): The number of recent data points to plot. If specified, only the last 'recent_count' rows will be plotted. Defaults to None.

    Returns:
        None
    """
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
    """
    Test the sample_every_kth_point function with different values of k.

    Parameters:
    - df: The input DataFrame containing the data.

    Returns:
    - X: The array of values used for sampling.
    - EFFICIENCY: The efficiency values for each sampling.
    - MEAN: The mean error values for each sampling.
    - MEDIAN: The median error values for each sampling.
    - STD: The standard deviation of error values for each sampling.
    """
    
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
    """
    Example function that demonstrates how to sample every kth point from a dataframe and plot the temperature data.

    Parameters:
    k (int): The sampling interval. Default is 10.

    Returns:
    None
    """
    df  = generate_greenhouse_data("datasets/greenhouse.csv")
    df = df.tail(150)
    df = sample_every_kth_point(df, k)
    plot_temperature_data(df)

def example_sample_reglin():
    """
    This function demonstrates the usage of the sample_reglin function.
    It generates greenhouse data, selects the last 150 rows, applies the sample_reglin function,
    and plots the temperature data.
    """
    df  = generate_greenhouse_data("datasets/greenhouse.csv")
    df = df.tail(150)
    df = sample_reglin(df)
    plot_temperature_data(df)

def example_optimal_sample(dT = 0.3):
    """
    Example function that demonstrates the usage of the optimal_sample function.
    
    Parameters:
        dT (float): The threshold value for temperature difference. Default is 0.3.
    
    Returns:
        None
    """
    df  = generate_greenhouse_data("datasets/greenhouse.csv")
    df = df.tail(150)
    df = optimal_sample(df, threshold_dT=dT)
    plot_temperature_data(df)

def example_sample_avg_rate_of_change():
    """
    This function demonstrates how to calculate the sample average rate of change for temperature data.
    It generates greenhouse data, calculates the hourly rate of change, selects the last 150 records,
    and then calculates the sample average rate of change based on the hourly rate of change.
    Finally, it plots the temperature data.

    Parameters:
    None

    Returns:
    None
    """
    df  = generate_greenhouse_data("datasets/greenhouse.csv")
    hroc = hourly_rate_of_change(df)
    df = df.tail(150)
    df = sample_avg_rate_of_change(df, 3600 * 1 / hroc)
    plot_temperature_data(df)

def test_sample_reglin(df):
    """
    Perform a test on the sample_reglin function with different values of max_dT.

    Parameters:
    - df: DataFrame
        The input DataFrame containing temperature data.

    Returns:
    - X: ndarray
        An array of values ranging from 0.4 to 3 with a step of 0.05.
    - EFFICIENCY: list
        A list of efficiency values calculated for each max_dT value.
    - MEAN: list
        A list of mean error values calculated for each max_dT value.
    - MEDIAN: list
        A list of median error values calculated for each max_dT value.
    - STD: list
        A list of standard deviation error values calculated for each max_dT value.
    """
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
    """
    Test the optimal sample function with different threshold values.

    Args:
        df (pandas.DataFrame): The input DataFrame containing temperature data.

    Returns:
        tuple: A tuple containing the following lists:
            - X (numpy.ndarray): An array of threshold values.
            - EFFICIENCY (list): A list of efficiency values for each threshold.
            - MEAN (list): A list of mean error values for each threshold.
            - MEDIAN (list): A list of median error values for each threshold.
            - STD (list): A list of standard deviation error values for each threshold.
    """
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

def test_sample_avg_rate_of_change(df, hourly_rate_of_change):
    """
    Test the sample average rate of change.

    This function takes a DataFrame `df` and the `hourly_rate_of_change` as input.
    It performs a series of calculations on the data and returns the results.

    Parameters:
    - df (pandas.DataFrame): The input DataFrame containing the data.
    - hourly_rate_of_change (float): The hourly rate of change.

    Returns:
    - X (numpy.ndarray): An array of values ranging from 0.01 to 3 with a step of 0.05.
    - EFFICIENCY (list): A list of efficiency values calculated for each sample.
    - MEAN (list): A list of mean values calculated for each sample.
    - MEDIAN (list): A list of median values calculated for each sample.
    - STD (list): A list of standard deviation values calculated for each sample.
    """
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

def comparaison_mean(df, limit=1000):
    """
    Compare different sampling methods based on their mean and efficiency.

    Parameters:
    - df: DataFrame
        The input DataFrame containing the data.
    - limit: int, optional
        The number of rows to consider from the end of the DataFrame. Default is 1000.

    Returns:
    None
    """
    plt.figure(figsize=(10, 5))
    hroc = hourly_rate_of_change(df)
    df = df.tail(limit)
    X, EFFICIENCY, MEAN, MEDIAN, STD = test_sample_every_kth_point(df)
    MEAN, EFFICIENCY = sort(MEAN, EFFICIENCY)
    plt.plot(MEAN, EFFICIENCY, label="Constant Polling Interval", marker='x')

    X, EFFICIENCY, MEAN, MEDIAN, STD = test_sample_reglin(df)
    MEAN, EFFICIENCY = sort(MEAN, EFFICIENCY)
    plt.plot(MEAN, EFFICIENCY, label="Linear Regression", marker='x')

    X, EFFICIENCY, MEAN, MEDIAN, STD = test_optimal_sample(df)
    MEAN, EFFICIENCY = sort(MEAN, EFFICIENCY)
    plt.plot(MEAN, EFFICIENCY, label="Optimal Polling rate", marker='x')

    X, EFFICIENCY, MEAN, MEDIAN, STD = test_sample_avg_rate_of_change(df, hroc)
    MEAN, EFFICIENCY = sort(MEAN, EFFICIENCY)
    plt.plot(MEAN, EFFICIENCY, label="Hourly Rate of Change", marker='x')

    plt.ylabel("Average seconds between polls")
    plt.xlabel("Average error")
    plt.ylim(0, 8000)
    plt.xlim(0, 1.3)

    plt.legend()
    plt.show()

def example_optimal_sample(dT = 0.3):
    """
    This function demonstrates how to use the `optimal_sample` function to generate an optimal sample of greenhouse data.
    
    Parameters:
        dT (float): The threshold value for temperature difference. Default is 0.3.
    
    Returns:
        None
    """
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
    """
    Generate a histogram of the differences between the original data and the sampled data.
    
    Parameters:
    - k (int): The sampling interval. Only every kth point will be included in the sampled data.
    
    Returns:
    None
    """
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
# print(hcor)
# hcor.plot()
# plt.xlabel("Hour of the day")
# plt.ylabel("Average absolute rate of change (°C/hour)")
# plt.show()
# plt.ylabel("Aboslute rate of change of the temperature (°C/hour)")
# plt.xlabel("Hour of the day")
# plt.show()

# df = generate_greenhouse_data("datasets/greenhouse.csv")
# comparaison_mean(df, 1000)

# example_sample_every_kth_point(1)
# example_sample_every_kth_point(10)
# exaample_optimal_sample()
# example_sample_reglin()
# example_sample_avg_rate_of_change()
    # Calculate differences between consecutive rows for the specified column