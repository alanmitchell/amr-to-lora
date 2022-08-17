"""Settings file for the application.
"""
from pathlib import Path

# List of Meter IDs to listen for and post
METER_IDS = [38517635]

# Minimum number of minutes between posted meter readings
METER_POST_INTERVAL = 10.0

# Serial port where the SEEED E5 board is connected
E5_PORT = '/dev/ttyUSB0'

# Path to the the rtl_tcp executable.  The default below should be correct for
# most systems.
RTL_TCP_PATH = '/usr/local/bin/rtl_tcp'

# Path to the rtlamr executable.  The default below should be correct for most
# systems.
RTLAMR_PATH = Path.home() / 'go/bin/rtlamr'
