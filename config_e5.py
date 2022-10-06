#!/usr/bin/env python3
"""Configures a LoRa-E5 device to work on the US915 Things Network.
"""

from secrets import token_hex
from pathlib import Path
import time
from serial import Serial

SER_PORT = '/dev/ttyUSB0'
APP_EUI = '0000000000000001'      # will be programmed into E5 device

# A CSV file is used to track Device IDs and Keys
FN_KEYS = 'keys.csv'
if not Path(FN_KEYS).exists():
    # start the file with a header row
    with open(FN_KEYS, 'w') as fkeys:
        fkeys.write('dev_eui,app_eui,app_key\n')

# Generate a random App Key
app_key = token_hex(16).upper()

# Commands that need to be executed to configure the device; will be later
# prefaced with an AT+.
cmds = (
    'FDEFAULT',
    'UART=TIMEOUT, 2000',
    f'ID=APPEUI, "{APP_EUI}"',
    f'KEY=APPKEY,"{app_key}"',
    'MODE=LWOTAA',
    'DR=US915HYBRID',
    'CH=NUM,8-15',
    'CLASS=A',
    'ADR=OFF',
    'DR=1',
    'DELAY=RX1,5000',
    'DELAY=RX2,6000',
    'JOIN=AUTO,10,1200,0',
)
try:
    p = Serial(SER_PORT, timeout=1.0)

    # determine the Dev EUI of the device
    p.write(b'AT+ID=DEVEUI\n')
    resp = p.readline()
    dev_eui = resp.decode('utf-8').strip().split(' ')[-1].replace(':','')

    for cmd in cmds:
        print('\n' + cmd)
        cmd_full = f'AT+{cmd}\n'.encode('utf-8')
        p.write(cmd_full)
        resp = p.readlines()
        for lin in resp:
            print(lin.decode('utf-8').strip())

except Exception as e:
    raise e

finally:
    p.close()
    # Save the IDs and App Key for this device.
    with open(FN_KEYS, 'a') as fkeys:
        fkeys.write(f'{dev_eui}, {APP_EUI}, {app_key}\n')
