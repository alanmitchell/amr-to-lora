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

# Dictionary keyed on Meter ID that holds the last 
# reading that caused a post to the MQTT broker.
last_reads = {}

def get_last(meter_id):
    """Returns a (ts, val) tuple for Meter ID 'meter_id'.  If that 
    Meter ID is not present (None, None) is returned.
    """
    return last_reads.get(meter_id, (None, None))

def set_last(meter_id, ts, val):
    """Sets the last meter reading for Meter ID 'meter_id'.
    The attributes stored are the timestamp 'ts' and the
    value 'val'.
    """
    last_reads[meter_id] = (ts, val)

# start the rtlamr program.
rtlamr = subprocess.Popen(['/home/pi/gocode/bin/rtlamr', 
    '-gainbyindex=24',   # index 24 was found to be the most sensitive
    '-format=csv'], stdout=subprocess.PIPE, text=True)


# Map of Commodity IDs to Meter Type
commod_map = {
    2: 'Gas',
    4: 'Elec',
    5: 'Elec',
    7: 'Elec',
    8: 'Elec',
    9: 'Gas',
    11: 'Water',
    12: 'Gas',
    13: 'Water',
}

while True:

    try:
        line = rtlamr.stdout.readline().strip()
        flds = line.split(',')

        if len(flds) != 9:
            # valid readings have nine fields
            continue

        # Make a reading received file. This is used to determine whether the gas
        # reader is working or not.
        with open('/var/run/last_gas', 'w') as read_file:
            read_file.write('reading received')

        # If the list of Meter IDs to record is not empty, make sure this ID
        # is in the list of IDs to record.
        meter_id = int(flds[3])
        if len(settings.METER_IDS) and meter_id not in settings.METER_IDS:
            continue

        ts_cur = time.time()
        read_cur = float(flds[7])

        # Determine the type of meter and the multiplier from the Commodity
        # Type in the message.
        commod_type = int(flds[4])    # Commodity type number
        commod = commod_map.get(commod_type, 'Elec')

        logging.debug('%s %s %s %s' % (ts_cur, meter_id, read_cur, commod_type))


        ts_last, read_last = get_last(meter_id)
        if ts_last is None:
            set_last(meter_id, ts_cur, read_cur)
            logging.info('First read for Meter # %s: %s' % (meter_id, read_cur))

        if ts_cur > ts_last + settings.METER_POST_INTERVAL * 60.0:
            # enough time has elapsed to make a post.  calculate the
            # rate of meter reading change per hour.
            rate = (read_cur - read_last) * 3600.0 * multiplier / (ts_cur - ts_last)
            
            # time stamp in the middle of the reading period
            ts_post = int((ts_cur + ts_last) / 2.0)
            post_str = f'{ts_post}\t{settings.LOGGER_ID}_{commod_type:02d}_{meter_id}\t{rate}'
            logging.debug(f'meter_reader MQTT post: {post_str}')

            set_last(meter_id, ts_cur, read_cur)

    except:
        logging.exception('Error processing reading %s' % line)
        time.sleep(2)