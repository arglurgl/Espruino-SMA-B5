#!/bin/false
# This file is part of Espruino, a JavaScript interpreter for Microcontrollers
#
# Copyright (C) 2013 Gordon Williams <gw@pur3.co.uk>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# ----------------------------------------------------------------------------------------
# This file contains information for a specific board - the available pins, and where LEDs,
# Buttons, and other in-built peripherals are. It is used to build documentation as well
# as various source and header files for Espruino.
# ----------------------------------------------------------------------------------------
# this file was originally created from https://github.com/fanoush/ds-d6/blob/master/espruino/DFU/B5/

import pinutils;

info = {
 'name' : "SMA B5 GPS smartwatch",
 'boardname' : 'SMAB5', # visible in process.env.BOARD
 'default_console' : "EV_BLUETOOTH",
 'variables' : 2000, # *16//13 2565 SD5.0 0x200014B8 SD 3.0 0x200019C0  How many variables are allocated for Espruino to use. RAM will be overflowed if this number is too high and code won't compile.
 'bootloader' : 1,
 'binary_name' : 'espruino_%v_SMAB5.hex',
 'build' : {
   'optimizeflags' : '-Os',
   'libraries' : [
     'BLUETOOTH',
     'GRAPHICS', 
     'LCD_SPI'
   ],
   'makefile' : [
      'DEFINES += -DBOARD_SMAB5', # not sure how board defines usually work so adding this manually here

      #hardware specific defines:
      'DEFINES += -DCONFIG_NFCT_PINS_AS_GPIOS', # Allow using NFC pins for gpio
      'DEFINES+=-DBTN1_IS_TOUCH=1', # BTN1 is a touch button
      'DEFINES+=-DSPIFLASH_SLEEP_CMD', # SPI flash needs to be explicitly slept and woken up

      # generic defines:
      'DEFINES+=-DNO_DUMP_HARDWARE_INITIALISATION', # don't dump hardware init - not used and saves 1k of flash
      #'DEFINES+=-DJSVAR_FORCE_16_BYTE=1', # 16 byte variables, without this 13 bytes seem to be used

      # Bluetooth settings:
      'DEFINES+=-DBLUETOOTH_NAME_PREFIX=\'"B5"\'', # Bluetooth device name prefix
      'DEFINES+=-DNRF_BLE_GATT_MAX_MTU_SIZE=53 -DNRF_BLE_MAX_MTU_SIZE=53', # increase MTU from default of 23
      'LDFLAGS += -Xlinker --defsym=LD_APP_RAM_BASE=0x2c40', # set RAM base to match MTU
      #'DEFINES+=-DBLE_HIDS_ENABLED=1', # for emulating keyboard/mouse etc over BLE

      # DFU settings:
      'DEFINES += -DBUTTONPRESS_TO_REBOOT_BOOTLOADER', # to have some way to get out of DFU mode, since we have no reset/power cycle
      'NRF_BL_DFU_INSECURE=1', # allow insecure DFU (no signature checking)
      'DFU_PRIVATE_KEY=targets/nrf5x_dfu/dfu_private_key.pem',
      'DFU_SETTINGS=--application-version 0xff --hw-version 52 --sd-req 0x8C,0x91',     

      # graphics/LCD settings:
      'DEFINES+=-DUSE_FONT_6X8 -DGRAPHICS_PALETTED_IMAGES=1 -DGRAPHICS_FAST_PATHS=1',
      'DEFINES+=-DESPR_GRAPHICS_INTERNAL=1', # Creates an internal Graphics object (graphicsInternal struct in C) that persists across execution
      'DEFINES+=-DDUMP_IGNORE_VARIABLES=\'"g\\0"\'', # Prevents the variable g from being saved to flash storage (saving flash space)
      # includes and sources for B5SDK12:
      'INCLUDE += -I$(ROOT)/libs/B5SDK12 -I$(ROOT)/libs/misc',
      'WRAPPERSOURCES += libs/B5SDK12/jswrap_B5SDK12.c',
      'JSMODULESOURCES += libs/js/banglejs/locale.min.js', # we might want to use our own locale later, for now just include the original Bangle.js one
      # might use these via code from bangle.js left in jswrap_B5SDK12.c/h later:
      #'SOURCES += libs/misc/nmea.c',
      'SOURCES += libs/misc/stepcount.c', # needed for the current non-weeded-out bangle.js code in jswrap_B5SDK12.c
      'DEFINES+=-DHOME_BTN=1', # fixup for the current non-weeded-out bangle.js code in jswrap_B5SDK12.c      
   ]
 }
};


chip = {
  'part' : "NRF52832",
  'family' : "NRF52",
  'package' : "QFN48",
  'ram' : 64,
  'flash' : 512,
  'speed' : 64,
  'usart' : 1,
  'spi' : 1,
  'i2c' : 1,
  'adc' : 1,
  'dac' : 0,
  'saved_code' : {
    #single-bank external version
    'page_size' : 4096,
    #'address' : ((118 - 10) * 4096), # Bootloader takes pages 120-127, FS takes 118-119
    #'pages' : 10,
    #'flash_available' : 512 - ((28 + 8 + 2 + 10)*4) # Softdevice 2.0 uses 28 pages of flash, bootloader 8, FS 2, code 10. Each page is 4 kb.
    'flash_available' : 512 - ((31 + 8 + 2 + 10)*4), # Softdevice 3.0 uses 31 pages of flash, bootloader 8, FS 2, code 10. Each page is 4 kb.
    #'flash_available' : 512 - ((35 + 8 + 10 + 10)*4) # Softdevice 5.0  uses 35 pages of flash, bootloader 8, FS 2, code 10. Each page is 4 kb.
    #'flash_available' : 512 - ((38 + 8 + 2 +16)*4) # Softdevice 6.x  uses 38 pages of flash, bootloader 8, FS 2, no code. Each page is 4 kb.
    'address' : 0x60000000, # second bank (for second 'drive' of storage module, see jsflash.c) in external spiflash (see below)
    'pages' : 512, # Entire 2MB of external flash
  },
};

devices = {
    'BTN1' : { 'pin' : 'D9', 'pinstate' : 'IN_PULLDOWN' },
    'VIBRATE' : { 'pin' : 'D30' },
    'SPIFLASH' : {
              'pin_sck' : 'D14',
              'pin_mosi' : 'D13',
              'pin_miso' : 'D11',
              'pin_cs' : 'D12',
              'size' : 2048*1024, # 2MB
              'memmap_base' : 0x60000000 # map into the address space (in software)
    },
    'LCD' : {
            'width' : 80, 'height' : 160, 'bpp' : 12,
            'controller' : 'st7735',
            'pin_dc' : 'D6',
            'pin_cs' : 'D5',
            'pin_rst' : 'D8',
            'pin_sck' : 'D2',
            'pin_mosi' : 'D3',
            'pin_bl' : 'D29',
    },
};


def get_pins():
  pins = pinutils.generate_pins(0,31) # 32 General Purpose I/O Pins.
  pinutils.findpin(pins, "PD2", True)["functions"]["ADC1_IN0"]=0;
  pinutils.findpin(pins, "PD3", True)["functions"]["ADC1_IN1"]=0;
  pinutils.findpin(pins, "PD4", True)["functions"]["ADC1_IN2"]=0;
  pinutils.findpin(pins, "PD5", True)["functions"]["ADC1_IN3"]=0;
  pinutils.findpin(pins, "PD28", True)["functions"]["ADC1_IN4"]=0;
  pinutils.findpin(pins, "PD29", True)["functions"]["ADC1_IN5"]=0;
  pinutils.findpin(pins, "PD30", True)["functions"]["ADC1_IN6"]=0;
  pinutils.findpin(pins, "PD31", True)["functions"]["ADC1_IN7"]=0;
  # Make buttons and LEDs negated
  pinutils.findpin(pins, "PD9", True)["functions"]["NEGATED"]=0;

  # everything is non-5v tolerant
  for pin in pins:
    pin["functions"]["3.3"]=0;
  return pins
