#!/usr/bin/env bash

set -o errexit

# remove old files from bin if they exist
# remove old files from bin if they exist
rm -f bin/espruino_*
rm -f bin/bootloader_espruino_*

# build espruino (full build)
source scripts/provision.sh B5SDK12 
make clean 
DFU_UPDATE_BUILD=1 BOARD=B5SDK12 RELEASE=1 make