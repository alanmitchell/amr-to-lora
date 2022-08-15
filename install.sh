#! /bin/bash

# Run this script from your Home directory.  Do not plug in the RTL-SDR dongle
# until the script is complete.

# Most of this script is copied from 
# https://gist.github.com/n8acl/dab196ce30e1e2139727cb7f76d300d6#file-rtlsdr-install-sh

echo "-------------------------------------------"
echo "-- Installing needed packages from repos --"
echo "-------------------------------------------"
sudo apt-get install -y git cmake libffi-dev libssl-dev build-essential libusb-1.0-0-dev pkg-config golang

echo "------------------------------------------------"
echo "-- Cloning rtl-sdr driver files from osmocom  --"
echo "------------------------------------------------"

sudo git clone git://git.osmocom.org/rtl-sdr.git

echo "------------------------------------------------"
echo "-- Building and Installing drivers            --"
echo "------------------------------------------------"

cd rtl-sdr
sudo mkdir build
cd build
sudo cmake ../ -DINSTALL_UDEV_RULES=ON
sudo make
sudo make install
sudo cp ../rtl-sdr.rules /etc/udev/rules.d/
sudo ldconfig

echo "------------------------------------------------"
echo "-- Blacklisting Certain RTL-SDR drivers       --"
echo "------------------------------------------------"

echo "blacklist dvb_usb_rtl28xxu" | sudo tee /etc/modprobe.d/blacklist-rtl.conf
echo "blacklist rtl2832" | sudo tee -a /etc/modprobe.d/blacklist-rtl.conf
echo "blacklist rtl2830" | sudo tee -a /etc/modprobe.d/blacklist-rtl.conf

echo "------------------------------------------------"
echo "-- Installing RTLAMR Meter Reading script     --"
echo "------------------------------------------------"
go get github.com/bemasher/rtlamr

echo "------------------------------------------------"
echo "-- Install the AMR to LoRa script          --"
echo "------------------------------------------------"
cd ../../
git clone https://github.com/alanmitchell/amr-to-lora.git
cd amr-to-lora
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
deactivate
cd ..

echo "------------------------------------------------"
echo "-- Now Reboot System and plug in RTL-SDR.     --"
echo "-- See the amr-to-lora/README.md file for     --"
echo "-- further configuration instructions.        --"
echo "------------------------------------------------"
