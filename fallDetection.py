import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def detect_falls(accel_data, threshold=2.5, window_size=50, acceleration_threshold=20):
    """Detect falls in acceleration data using a threshold-based approach."""

    def smooth_data(data, window_size):
        """Smooth data using a simple moving average."""
        weights = np.ones(window_size) / window_size
        return np.convolve(data, weights, mode="valid")

    # Check if the array is empty
    if not accel_data.size:
        raise ValueError("The acceleration data array is empty.")

    # Check if the array is 1D, and reshape if necessary
    if accel_data.ndim == 1:
        accel_data = accel_data.reshape(-1, 1)

    # Compute the magnitude of acceleration
    magnitude = np.linalg.norm(accel_data, axis=1)

    # Smooth the magnitude data
    smoothed_data = smooth_data(magnitude, window_size)

    # Make sure both arrays have the same length
    min_length = min(len(smoothed_data), len(magnitude))
    magnitude = magnitude[:min_length]
    smoothed_data = smoothed_data[:min_length]

    # Find indices where the magnitude exceeds the threshold and acceleration is 20 or lower
    fall_indices = np.where(
        (smoothed_data > threshold) & (magnitude <= acceleration_threshold)
    )[0]

    return fall_indices, smoothed_data


# Function to read data from CSV file
def read_csv_data(file_path):
    try:
        with open(file_path, "r") as file:
            # Read lines from the CSV file, remove quotes and whitespace, and convert values to lists
            lines = [list(map(float, line.strip('[]" \n').split(","))) for line in file]
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        exit()
    return np.array(lines)


# Function to update the plot in real-time
def update(frame):
    global accel_data, ax
    accel_data = np.vstack([accel_data[1:], read_csv_data("arduino_data.csv")])
    fall_indices, smoothed_data = detect_falls(accel_data)

    # Clear the previous plot
    plt.clf()

    # Plot the smoothed magnitude of acceleration
    plt.subplot(3, 1, 3)  # Change here
    plt.plot(
        np.arange(len(smoothed_data)),
        smoothed_data,
        label="Movement",
        color="green",
    )
    plt.scatter(
        fall_indices, smoothed_data[fall_indices], color="red", label="Fall Detected"
    )
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Movement")

    plt.suptitle("Accelerometer Data with Fall Detection")

    # Update x-axis limits for scrolling effect
    ax = plt.gca()
    ax.set_xlim(frame, frame + len(accel_data))


# Initialize empty data for real-time update
accel_data = np.zeros((100, 3))

# Create an animation
animation = FuncAnimation(
    plt.figure(figsize=(50, 8)), update, frames=300, interval=1000
)

# Show the plot
plt.show()
