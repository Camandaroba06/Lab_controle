import serial
import csv
import time
import matplotlib.pyplot as plt
import numpy as np

# Configure the serial connection (the parameters might need adjustment)
ser = serial.Serial("COM4", 115200)  # Replace 'COM3' with your actual COM port
ser.flushInput()

# Open CSV file for writing data
with open("data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "RPM", "Setpoint"])

    start_time = time.time()
    while time.time() - start_time <= 6:  # Collect data for 10 seconds
        try:
            line = ser.readline().decode("utf-8").strip()
            data = line.split(",")
            if len(data) == 3:
                writer.writerow(data)
                print(data)
        except Exception as e:
            print(f"Error: {e}")

ser.close()

# Read data from CSV file
times = []
rpms = []
setpoints = []

with open("data.csv", mode="r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        times.append(int(row[0]))
        rpms.append(float(row[1]))
        setpoints.append(float(row[2]))


# Apply moving average filter
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode="valid")


window_size = 15  # Adjust the window size as needed
filtered_rpms = moving_average(rpms, window_size)

# Adjust times and setpoints for the filtered data length
filtered_times = times[window_size - 1 :]
filtered_setpoints = setpoints[window_size - 1 :]

# Plot raw and filtered data
plt.figure(figsize=(12, 6))
# plt.plot(times, rpms, label="Raw RPM", alpha=0.5)
plt.plot(filtered_times, filtered_rpms, label="Filtered RPM", linewidth=2)
plt.plot(times, setpoints, label="Setpoint", linestyle="--", alpha=0.7)
plt.xlabel("Time (us)")
plt.ylabel("RPM")
plt.title("RPM vs Time")
plt.legend()
plt.grid(True)
plt.show()
