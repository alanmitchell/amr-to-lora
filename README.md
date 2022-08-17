# amr-to-lora
Application that relays AMR meter readings collected with an RTL-SDR dongle to a LoRaWAN network
through use of a [SEEED Studio LoRa E5 Mini module.](https://www.seeedstudio.com/LoRa-E5-mini-STM32WLE5JC-p-4869.html)

The application can be installed on most systems running Linux, such as the Raspberry Pi.
To perform the bulk of the installation, run the install.sh script, which will install
necessary Linux packages and clone this repository to the host machine.  Running the install.sh
script can be accomplished by running the follwing at a Linux shell prompt from your $HOME 
directory:

    curl https://raw.githubusercontent.com/alanmitchell/amr-to-lora/main/install.sh | bash

Further configuration is then needed.  

* Change into the $HOME/amr-to-lora directory.
* Copy the `settings_example.py` file to `settings.py` and then edit the values in that file.
    * Note that you can place the `settings.py` file in a more accessible location, such as in
      in the `/boot` directory of the Raspberry Pi, but then you will need to symlink the file
      back to the $HOME/amr-to-lora directory.
* To run the meter collection script, change into the $HOME/amr-to-lora directory, make sure the
  RTL-SDR dongle and the E5 LoRa Mini are plugged into USB ports, and run the following command:
    * `env/bin/python main.py`
* If you want the script to automatically start when your system is booted, add the following
  command to a startup script file such as `/etc/rc.local` on the Raspberry Pi.  Or, you can add
  the command to the crontab file with the @reboot directive:
    * `$HOME/amr-to-lora/env/bin/python $HOME/amr-to-lora/main.py &`
* It is a good idea to automatically reboot your system to recover from unexpected software problems
  by adding a command to the crontab file similar to:
    * `0 4   *   *   *    sudo /sbin/shutdown -r +1`

It is possible to change the LoRa datarate of the E5 board through a Downlink command.  Use Port 1 for
the downlink and send a two-byte downlink:  the first byte is 0x01 and the second byte is the desired
datarate.  For example, to change to Datarate 0, send 0x0100.  Valid datarates are 0, 1, 2, or 3.

The software would not be possible without the much more detailed work that went into the
[rtl_tcp](https://www.rtl-sdr.com/) and [rtlamr](https://github.com/bemasher/rtlamr) packages.
Many thanks to the creators of those packages.
