"""Script to determine if a successful meter read has occurred within a
reasonable amount of time.  If not, this script reboots the system.
"""
# The number of minutes since the last valid reading to post before a reboot
# should occur
TOO_LONG_TIME = 30   # minutes

import subprocess
import time
from pathlib import Path

def reboot():
    # save the current time so upon reboot it is sort-of accurate if there is no
    # network connection.
    subprocess.run('sudo fake-hwclock save', shell=True)
    subprocess.run('sudo reboot now', shell=True)

# The number of seconds since rebooting
uptime = float( open('/proc/uptime').read().split()[0] )

# only check if the system has been running long enough
if uptime > TOO_LONG_TIME * 60.0 + 120:

    # filename of the file that gets updated when a meter read has occurred
    plast = Path(__file__).resolve().parent / 'last-post'

    if not plast.exists():
        # no file present, reboot
        reboot()
    elif time.time() - plast.stat().st_mtime > TOO_LONG_TIME * 60.0:
        # the file is too old, reboot
        reboot()
