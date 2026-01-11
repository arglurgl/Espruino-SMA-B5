#!/usr/bin/env bash

set -o errexit

# remove old files from bin if they exist
rm -f bin/espruino_*
rm -f bin/bootloader_espruino_*

# build espruino (full build)
source scripts/provision.sh B5SDK12 
make clean 
BOARD=B5SDK12 RELEASE=1 make

# flash espruino to the device
nrfutil device program --options reset=RESET_DEFAULT,chip_erase_mode=ERASE_ALL --firmware bin/espruino_*_SMAB5.hex