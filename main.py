#!/usr/bin/env python3
'''Script to read utility meter transmissions and transmit the reading to a 
LoRaWAN network through a SEEED E5 module.

This script assumes the RTL-SDR Software Defined Radio is based on R820T2 tuner and 
RTL2832U chips.

This script assumes that the program rtl_tcp is already running. (I tried starting
it within this script, but it then captured keystrokes such as Ctrl-C.).

'''
import subprocess
import signal
import time
import logging

logging.warning('meter_reader has restarted')

import settings

def shutdown(signum, frame):
    '''Kills the external processes that were started by this script
    '''
    # Hard kill these processes and I have found them difficult to kill with SIGTERM
    subprocess.call('/usr/bin/pkill -f "/bin/bash /home/pi/amr-to-lora/run_rtl_tcp"', shell=True)
    subprocess.call('/usr/bin/pkill -f "/bin/bash /home/pi/amr-to-lora/run_meter_reader"', shell=True)
    subprocess.call('/usr/bin/pkill --signal 9 rtlamr', shell=True)
    subprocess.call('/usr/bin/pkill --signal 9 rtl_tcp', shell=True)
    # Also found that I need to hard kill this process as well (suicide)
    subprocess.call('/usr/bin/pkill --signal 9 -f "python3 /home/pi/amr-to-lora/main.py"', shell=True)

# If process is being killed, go through shutdown process
signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

# Dictionary keyed on Meter ID that holds the timestamp of the last reading.
# Initialize to timestamp of 0 for every requested meter ID.
last_reads = {}
for meter_id in settings.METER_IDS:
    last_reads[meter_id] = 0

def get_last(meter_id):
    """Returns the last reading timestamp for Meter ID 'meter_id'.
    """
    return last_reads[meter_id]

def set_last(meter_id, ts):
    """Sets the last meter reading for Meter ID 'meter_id'.
    The attributes stored are the timestamp 'ts' and the
    value 'val'.
    """
    last_reads[meter_id] = ts

# start the rtlamr program.
rtlamr = subprocess.Popen(['/home/pi/go/bin/rtlamr', 
    '-gainbyindex=24',   # index 24 was found to be the most sensitive
    '-format=csv'], stdout=subprocess.PIPE, text=True)

while True:

    try:
        line = rtlamr.stdout.readline().strip()
        flds = line.split(',')

        if len(flds) != 9:
            # valid readings have nine fields
            continue

        # make sure this ID is in the list of IDs to record.
        meter_id = int(flds[3])
        if meter_id not in last_reads:
            continue

        ts_cur = time.time()
        read_cur = float(flds[7])

        logging.debug('%s %s %s %s' % (ts_cur, meter_id, read_cur))

        ts_last = get_last(meter_id)

        if ts_cur > ts_last + settings.METER_POST_INTERVAL * 60.0:
            # enough time has elapsed to make a post.
            ts_post = int((ts_cur + ts_last) / 2.0)
            post_str = f'{ts_post}\t{settings.LOGGER_ID}_{commod_type:02d}_{meter_id}\t{rate}'
            logging.debug(f'meter_reader MQTT post: {post_str}')

            set_last(meter_id, ts_cur)

    except:
        logging.exception('Error processing reading %s' % line)
        time.sleep(2)