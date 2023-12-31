# -*- coding: utf-8 -*-
# Efficient Data anamoly detection
import numpy as np
import matplotlib.pyplot as plt
import time

# The Algos used for detecting the anomalies are moving z-score and CUSUM algo. Each has its advantages and disadvantages
# The moving z-score algo can give me all the sharp anomalies by keeping the window size small over which I find the mean and deviation
# Whereas the CUSUM algo can help detect the gradual and persistent shifts in the observation
# Both of these algos combined is quite effective in capturing the anomalies in real world time series data
# Regarding the Complexity, the CUSUM has a linear time complexity and in moving z-score as we keep a very small window size we can assume it to be linear time
# Hence looking at its fastness and efficiency I decided to move forward with this.

# Simulated data stream generator with adjusted parameters
def generate_data_stream(samples=1000, volatility=0.5, noise_level=0.1, anomaly_frequency=0.02):
    time_step = 0
    base_value = 1000

    for i in range(samples):
        volatility_change = np.random.normal(scale=volatility)
        base_value += volatility_change

        # Introducing anomalies
        if np.random.rand() < anomaly_frequency:
            anomaly = np.random.choice([-50, 50]) #The amplitude range of peak
            base_value += anomaly

        # Adding noise on the base graph to replicate real world situation
        noise = np.random.normal(scale=noise_level)
        data_point = base_value + noise

        yield data_point

        time_step += 1

        time.sleep(0.05)

# CUSUM anomaly detection
def detect_cusum(data, threshold=5, drift=1):
    mean = 0
    s = 0
    change_point = None
    anomalies = []

    for i, x in enumerate(data):
        s = max(0, s + x - mean - drift)
        mean = (i * mean + x) / (i + 1)
        #Anomaly condition
        if s > threshold:
            change_point = i
            anomalies.append(change_point)
            s = 0

    return anomalies

# Generate data stream with adjusted parameters
stream = generate_data_stream(samples=1000, volatility=2.0, noise_level=10, anomaly_frequency=0.03)
data = [point for point in stream]

# Moving Z-score anomaly detection
def detect_anomalies(data, window_size, threshold):
    anomalies = []
    for i in range(window_size, len(data)):
        window = data[i - window_size:i]
        mean = np.mean(window) #Finding the mean
        std = np.std(window) #Finding the standard deviation
        z_score = (data[i] - mean) / std if std != 0 else 0 # z-score formula
        #Anomaly Condition
        if abs(z_score) > threshold:
            anomalies.append(i)
    return anomalies

# Define parameters for Moving Z-score anomaly detection
window_size = 20 #Keeping a small window size to detect sharp changes
z_score_threshold = 3.0 #Threshold at which anomaly is detected (3 is often used as a standard for threshold in real world time series)

# Define parameters for CUSUM anomaly detection
cusum_threshold = 100  #The cumilative sum at which we start considering anomaly
cusum_drift = 10  #The threshold at which we detedt anomaly

# Detect anomalies using both Moving Z-score and CUSUM
z_score_anomalies = detect_anomalies(data, window_size, z_score_threshold)   #Finding the points using moving z-score and passing the params
cusum_anomalies = detect_cusum(data, threshold=cusum_threshold, drift=cusum_drift)  #Finding the points using CUSUM and passing the params

# Plotting the data stream with detected anomalies
plt.figure(figsize=(12, 6))
plt.plot(data, label='Data Stream', color='blue')
plt.scatter(cusum_anomalies, [data[i] for i in cusum_anomalies], color='green', label='CUSUM Anomalies', s=20)
plt.scatter(z_score_anomalies, [data[i] for i in z_score_anomalies], color='red', label='Moving Z-score Anomalies', s=20)
plt.title('Simulated Data Stream with Anomalies (Detected by Moving Z-score and CUSUM)')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()

