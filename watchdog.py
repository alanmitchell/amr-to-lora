"""Script to determine if a successful meter read has occurred within a
reasonable amount of time.  If not, this script reboots the system.
"""
# The number of minutes since the last valid reading to post before a reboot
# should occur
TOO_LONG_TIME = 60   # minutes

import sys
import subprocess
import time
from pathlib import Path

# The number of seconds since rebooting
uptime = float( open('/proc/uptime').read().split()[0] )

# don't check before the system has been running long enough
if uptime < TOO_LONG_TIME * 60.0 + 120:
    sys.exit()

# filename of the file that gets updated when a meter read has occurred
plast = Path(__file__).resolve().parent / 'last-post'

# if no file present reboot
if not plast.exists():
    subprocess.call('sudo reboot now', shell=True)

# if the file is too old, reboot
if time.time() - plast.stat().st_mtime > TOO_LONG_TIME * 60.0:
    subprocess.call('sudo reboot now', shell=True)
