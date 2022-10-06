#!/usr/bin/env python3
'''Script to read utility meter transmissions and transmit the reading to a 
LoRaWAN network through a SEEED E5 module.

This script assumes the RTL-SDR Software Defined Radio is based on R820T2 tuner and 
RTL2832U chips.
'''
import subprocess
import signal
import time
import logging
import os

from e5lora import Board

logging.warning('meter_reader has restarted')

import settings


def process_downlink(down_data: bytes):
    """Processes a downlink command sent to the LoRa E5 board.  'down_data' is a bytes
    object containing the data sent in the downlink.
    """
    if down_data[0] == 1:         # request to change data rate
        new_data_rate = down_data[1]
        if new_data_rate in (0, 1, 2, 3):
            lora_board.set_data_rate(new_data_rate) 

def shutdown(signum, frame):
    '''Kills the external processes that were started by this script
    '''
    # Hard kill these processes and I have found them difficult to kill with SIGTERM
    try:
        rtlamr.kill()
    except:
        pass
    try:
        rtl_tcp.kill()
    except:
        pass

    # Also found that I need to hard kill this process as well (suicide)
    this_pid = os.getpid()
    os.kill(this_pid, signal.SIGKILL)

# If process is being killed, go through shutdown process
signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

# make object to use the E5 LoRaWAN board
lora_board = Board(port=settings.E5_PORT, downlink_callback=process_downlink)

# Dictionary keyed on Meter ID that holds the timestamp of the last reading.
# Initialize to timestamp of 0 for every requested meter ID.
last_reads = {}
for meter_id in settings.METER_IDS:
    last_reads[meter_id] = 0

# start the rtl_tcp and rtlamr program.
rtl_tcp = subprocess.Popen(settings.RTL_TCP_PATH)
# discovered that a delay of at least 30 seconds is required or rtl_tcp will disconnect rtlamr.
time.sleep(47)     
rtlamr = subprocess.Popen(
    [settings.RTLAMR_PATH, 
    '-gainbyindex=24',   # index 24 was found to be the most sensitive
    '-format=csv',
    '-symbollength=48' if settings.SLOW_CPU else '-symbollength=72'], 
    stdout=subprocess.PIPE, 
    text=True,
    )

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
        read_cur = int(flds[7])

        logging.debug('%s %s %s' % (ts_cur, meter_id, read_cur))

        ts_last = last_reads[meter_id]

        if ts_cur > ts_last + settings.METER_POST_INTERVAL * 60.0:
            # enough time has elapsed to make a post.
            print('transmitting:', int(ts_cur), meter_id, read_cur)
            lora_board.send_uplink(
                [
                    (4, 1),             # message type: id with value
                    (meter_id, 5),      # id
                    (read_cur, 4)       # value
                ]
            )

            last_reads[meter_id] = ts_cur

    except:
        logging.exception('Error processing reading %s' % line)
        time.sleep(2)