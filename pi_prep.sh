#! /bin/bash
# Additional steps useful for preparing amr-to-lora on a Raspberry Pi.
# Change into the amr-to-lora directory before running this script.
# Run install.sh first.

# Make settings.py accessible on the /boot partition so that it can be easily
# edited by a PC.  Link it back to its necessary location in the amr-to-lora
# directory.
sudo mkdir /boot/meter-reader
sudo cp settings_example.py /boot/meter-reader/settings.py
ln -s /boot/meter-reader/settings.py settings.py

# Add cron command to reboot nightly
crontab -l > cron_bak
printf "\n*/10 * * * * /home/pi/amr-to-lora/env/bin/python /home/pi/amr-to-lora/watchdog.py\n" >> cron_bak
crontab cron_bak
rm cron_bak

# Create and enable a systemd service to start the amr-to-lora program
# at start up.
sudo cp amr-to-lora.service /lib/systemd/system/amr-to-lora.service
sudo chmod 644 /lib/systemd/system/amr-to-lora.service
sudo systemctl daemon-reload
sudo systemctl enable amr-to-lora.service
