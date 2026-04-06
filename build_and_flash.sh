#!/usr/bin/env bash

set -o errexit

# remove old files from bin if they exist
rm -f bin/espruino_*
rm -f bin/bootloader_espruino_*

# build espruino (full build)
source scripts/provision.sh ID205 
make clean 
BOARD=ID205 RELEASE=1 make

# flash espruino to the device
#nrfutil device program --options reset=RESET_DEFAULT,chip_erase_mode=ERASE_ALL --firmware bin/espruino_*_id205.hex
nrfutil device program --options reset=RESET_DEFAULT,chip_erase_mode=ERASE_RANGES_TOUCHED_BY_FIRMWARE --firmware bin/espruino_*_id205.hex
