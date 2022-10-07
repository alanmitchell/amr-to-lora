# amr-to-lora
Application that relays AMR meter readings collected with an RTL-SDR dongle to a LoRaWAN network
through use of a [SEEED Studio LoRa E5 Mini module.](https://www.seeedstudio.com/LoRa-E5-mini-STM32WLE5JC-p-4869.html).

A ready-to-go [Raspberry Pi SD Image](https://analysisnorth.com/mini-monitor/amr-to-lora-2022-10-07.zip) is
available for download.  This can be used to create a Raspberry Pi SD card that will automatically
run the amr-to-lora program, after appropriate editing of the `settings.py` file in the /boot/amr
directory on the card.  Select the "Use Custom" option in the "Operating System" drop-down of the
Raspberry Pi Imager program to make the card. There is no need to unzip the image file, as the 
Imager program can read a zip file.

The application can be installed on most systems running Linux.
To perform the bulk of the installation, run the install.sh script, which will install
necessary Linux packages and clone this repository to the host machine.  Running the install.sh
script can be accomplished by running the follwing at a Linux shell prompt from your $HOME 
directory:

    curl https://raw.githubusercontent.com/alanmitchell/amr-to-lora/main/install.sh | bash

Further configuration is then needed.  If you are installing on a Raspberry Pi:

* Change into the `$HOME/amr-to-lora` directory.
* Examine the pi_prep.sh script, and if no conflicts are noted, run it: `./pi_prep.sh`
    * This script makes the `settings.py` file easily editable with a PC by placing it
      on the /boot partition in the `amr` subdirectory.
    * The script adds a command to the pi crontab to reboot the system nightly.
    * The script adds a systemd service to autostart the amr-to-lora program at system startup.
* Edit the `settings.py` file in \boot\amr to make appropriate settings. If you are running on 
  a Pi Zero, make sure SLOW_CPU is set to True.  For any CPU faster, use False and meter
  readings reception will be improved.
* Reboot the Pi to have the changes take effect and the program should start collecting data.
* Note that the above-mentioned Pi SD Card image has already completed these configuration steps;
  the only necessary step is editing the settings.py file.

If you are not installing on a Raspberry Pi, examine `pi_prep.sh` to determine the general
nature of needed one-time configuration tasks and modify your system accordingly.  To simply start the meter
reading program after having created a suitable `settings.py` file, change into the
`$HOME/amr-to-lora` directory, make sure the RTL-SDR and SEEED E5 dongles are connected to USB
ports and execute: `env/bin/python main.py`  

It is possible to change the LoRa datarate of the E5 board through a Downlink command.  Use Port 1 for
the downlink and send a two-byte downlink:  the first byte is 0x01 and the second byte is the desired
datarate.  For example, to change to Datarate 0, send 0x0100.  Valid datarates are 0, 1, 2, or 3.

The software would not be possible without the much more detailed work that went into the
[rtl_tcp](https://www.rtl-sdr.com/) and [rtlamr](https://github.com/bemasher/rtlamr) packages.
Many thanks to the creators of those packages.
