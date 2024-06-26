import serial
import csv
import time
import matplotlib.pyplot as plt

# Configure the serial connection (the parameters might need adjustment)
ser = serial.Serial("COM4", 115200)  # Replace 'COM3' with your actual COM port
ser.flushInput()

# Open CSV file for writing data
with open("data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "RPM", "Setpoint"])

    start_time = time.time()
    while time.time() - start_time <= 10:  # Collect data for 10 seconds
        try:
            line = ser.readline().decode("utf-8").strip()
            data = line.split(",")
            if len(data) == 3:
                writer.writerow(data)
                print(data)
        except Exception as e:
            print(f"Error: {e}")

ser.close()

# Read data from CSV file and plot it
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

plt.figure(figsize=(10, 5))
plt.plot(times, rpms, label="RPM")
plt.plot(times, setpoints, label="Setpoint", linestyle="--")
plt.xlabel("Time (ms)")
plt.ylabel("RPM")
plt.title("RPM vs Time")
plt.legend()
plt.grid(True)
plt.show()
