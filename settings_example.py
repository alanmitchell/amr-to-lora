"""Settings file for the application.
"""

# List of Meter IDs to listen for and post
METER_IDS = [38517635]

# Minimum number of minutes between posted meter readings
METER_POST_INTERVAL = 10.0

# Serial port where the SEEED E5 board is connected
E5_PORT = '/dev/ttyUSB0'