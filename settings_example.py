"""Settings file for the application.
"""

# List of Meter IDs to listen for and post
METER_IDS = [38517635]

# Minimum number of minutes between posted meter readings
METER_POST_INTERVAL = 10.0

# If you are using slow processor, such as the Pi Zero, set the following to
# True otherwise False.
SLOW_CPU = False

#----------------------------------
# Changes to the following settings are unlikely, unless you are not using a
# Raspberry Pi.

# Serial port where the SEEED E5 board is connected
E5_PORT = '/dev/ttyUSB0'

# Path to the rtlamr executable.  It probably resides underneath the Home
# directory that was used during install.  Make sure that component of the
# path below is correct.
RTLAMR_PATH = '/home/pi/go/bin/rtlamr'

# Path to the the rtl_tcp executable.  The default below should be correct for
# most systems.
RTL_TCP_PATH = '/usr/local/bin/rtl_tcp'
