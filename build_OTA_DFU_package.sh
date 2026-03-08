#!/usr/bin/env bash

set -o errexit

# remove old files from bin if they exist
# remove old files from bin if they exist
rm -f bin/espruino_*
rm -f bin/bootloader_espruino_*

# build espruino (full build)
source scripts/provision.sh ID205
make clean 
DFU_UPDATE_BUILD=1 BOARD=ID205 RELEASE=1 make