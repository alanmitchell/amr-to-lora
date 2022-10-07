#! /bin/bash
# Additional steps useful for preparing amr-to-lora on a Raspberry Pi.
# Change into the amr-to-lora directory before running this script.
# Run install.sh first.
sudo mkdir /boot/amr
sudo cp settings_example.py /boot/amr/settings.py
ln -s /boot/amr/settings.py settings.py
crontab -l > cron_bak
printf "\n@reboot sleep 15 && /home/pi/amr-to-lora/env/bin/python /home/pi/amr-to-lora/main.py \n0 4 * * * sudo /sbin/shutdown -r +1\n" >> cron_bak
crontab cron_bak
rm cron_bak
