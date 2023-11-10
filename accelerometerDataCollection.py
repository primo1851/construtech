import serial
import csv

serial_port = "/dev/ttyACM0"
baud_rate = 9600

# Open the serial port
ser = serial.Serial(serial_port, baud_rate)

# Create a CSV file for writing
csv_file = open("arduino_data.csv", "w", newline="")
csv_writer = csv.writer(csv_file)

try:
    while True:
        # Read data from the serial port
        data = ser.readline().decode("utf-8").strip()

        # Print the data to the console
        print(data)

        # Write the data to the CSV file
        csv_writer.writerow([data])

except KeyboardInterrupt:
    print("Data collection has been stopped")

finally:
    # Close the serial port and CSV file
    ser.close()
    csv_file.close()
