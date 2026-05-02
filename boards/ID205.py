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

import pinutils;

info = {
 'name' : "ID205",
 'link' :  [ "" ],
 'espruino_page_link' : '',
# 'default_console' : "EV_SERIAL1",
# 'default_console_tx' : "D6",
# 'default_console_rx' : "D8",
# 'default_console_baudrate' : "9600",
 'variables' : 2500, # How many variables are allocated for Espruino to use. RAM will be overflowed if this number is too high and code won't compile.
 'bootloader' : 1,
 'binary_name' : 'espruino_%v_id205.hex',
 'build' : {
   'optimizeflags' : '-Os',
   'libraries' : [
     'BLUETOOTH',
     'TERMINAL',
     'GRAPHICS',
     'LCD_SPI',
     'JIT',
   ],
   'makefile' : [
     'DEFINES += -DCONFIG_NFCT_PINS_AS_GPIOS', # Allow the reset pin to work
     'DEFINES += -DNRF_BL_DFU_ENTER_METHOD_BUTTON=1 -DNRF_BL_DFU_ENTER_METHOD_BUTTON_PIN=5',
     'DEFINES += -DBUTTONPRESS_TO_REBOOT_BOOTLOADER',
     'DEFINES+=-DBLUETOOTH_NAME_PREFIX=\'"Bangle.js"\'',
     'DEFINES+=-DCUSTOM_GETBATTERY=jswrap_banglejs_getBattery',
     'DEFINES+=-DESPR_BATTERY_FULL_VOLTAGE=0.2144', # TODO: check with full battery
     'DEFINES+=-DDUMP_IGNORE_VARIABLES=\'"g\\0"\'',
     'DEFINES+=-DESPR_GRAPHICS_INTERNAL=1',
     'DEFINES+=-DUSE_FONT_6X8 -DGRAPHICS_PALETTED_IMAGES -DESPR_GRAPHICS_12BIT -DGRAPHICS_ANTIALIAS -DESPR_PBF_FONTS',
     'DEFINES+=-DNO_DUMP_HARDWARE_INITIALISATION', # don't dump hardware init - not used and saves 1k of flash
     'INCLUDE += -I$(ROOT)/libs/banglejs -I$(ROOT)/libs/misc',
     
     # enable bangle storage factory reset and needed fonts
     'SOURCES += libs/banglejs/banglejs2_storage_default.c',
     'DEFINES += -DESPR_STORAGE_INITIAL_CONTENTS=1', # use banglejs2_storage_default
     'WRAPPERSOURCES += libs/graphics/jswrap_font_14.c',
     'WRAPPERSOURCES += libs/graphics/jswrap_font_17.c',
     'WRAPPERSOURCES += libs/graphics/jswrap_font_22.c',
     'WRAPPERSOURCES += libs/graphics/jswrap_font_28.c',
     'WRAPPERSOURCES += libs/graphics/jswrap_font_6x15.c',
     'WRAPPERSOURCES += libs/graphics/jswrap_font_12x20.c',

     'DEFINES += -DESPR_USE_STORAGE_CACHE=32', # Add a 32 entry cache to speed up finding files
          
      # used for accelerometer stepcounter
     'SOURCES += libs/misc/stepcount.c',

     'WRAPPERSOURCES += libs/banglejs/jswrap_bangle.c',
     'JSMODULESOURCES += libs/js/banglejs/locale.min.js',
     'DEFINES += -DBANGLEJS',

     # touchscreen settings
     'DEFINES += -DTOUCH_DEVICE_IT7259=1', # Enable IT7259 touchscreen handler
     # unistroke gesture recognition:
     #'SOURCES += libs/misc/unistroke.c',
     #'WRAPPERSOURCES += libs/misc/jswrap_unistroke.c',
     #'DEFINES += -DESPR_BANGLE_UNISTROKE=1', 

     'DFU_PRIVATE_KEY=targets/nrf5x_dfu/dfu_private_key.pem',
     'DFU_SETTINGS=--application-version 0xff --hw-version 52 --sd-req 0xa9,0xae,0xb6',

     'NRF_SDK15=1', # activate for SDK15, defaults to SDK12
     'BOOTLOADER_SETTINGS_FAMILY=NRF52840',

     # flash settings
     'DEFINES+=-DSPIFLASH_SLEEP_CMD', # SPI flash needs to be explicitly slept and woken up
     'DEFINES += -DSPIFLASH_READ2X', # Read SPI flash at 2x speed using MISO and MOSI for IO
     'DEFINES += -DSPIFLASH_READ2X_DUAL_PORT', # Support mixed P0/P1 pins (ID205 fix)

     'DEFINES += -DESPR_USE_SPI3=1', # Use SPIM3 (even though it has errata 195) as it's much faster, bitrate is set in lcd config below

   ]
 }
};


chip = {
  'part' : "NRF52840",
  'family' : "NRF52",
  'package' : "QFN48",
  'ram' : 256,
  'flash' : 1024,
  'speed' : 64,
  'usart' : 2,
  'spi' : 1,
  'i2c' : 1,
  'adc' : 1,
  'dac' : 0,
  'saved_code' : {
    'address' : 0x60000000, # put this in external spiflash (see SPIFLASH below)
    'page_size' : 256,
    'pages' : 32*1024, # Entire 8MB of external flash
    'flash_available' : 1024 - ((31 + 8 + 2 + 10)*4) # Softdevice uses 31 pages of flash, bootloader 8, FS 2, code 10. Each page is 4 kb.
  },
};

devices = {
  'BTN1' : { 'pin' : 'D5', 'pinstate' : 'IN_PULLDOWN' }, # Pin negated in software
  'BTN2' : { 'pin' : 'D7', 'pinstate' : 'IN_PULLDOWN' }, # Pin negated in software
  'VIBRATE' : { 'pin' : 'D8' }, # Pin negated in software
  'LCD' : {
            'width' : 240, 'height' : 240, 'bpp' : 12, # 16 normal, 12 bit is possible
            'controller' : 'st7789v',
            'pin_dc' : 'D28',
            'pin_cs' : 'D19',
            'pin_rst' : 'D2',
            'pin_sck' : 'D30',
            'pin_mosi' : 'D18',
            'pin_bl' : 'D35', # backlight pwm, active high
            'bitrate' : 32000000 , # this bitrate only works on SPIM3, see makefile flag above
          },
  'BAT' : {
            'pin_charging' : 'D45', # active low
            'pin_voltage' : 'D4'
          },
  'SPIFLASH' : {
            'pin_cs' : 'D15',
            'pin_sck' : 'D36',
            'pin_mosi' : 'D38',
            'pin_miso' : 'D17',
            'size' : 8*1024*1024, # 8MB
            'memmap_base' : 0x60000000 # map into the address space (in software)
          },
  'TOUCH' : {
            'device' : 'IT7259', 'addr' : 0x46,
            'pin_sda' : 'D21',
            'pin_scl' : 'D23',
            'pin_rst' : 'D33',
            'pin_irq' : 'D32'
          },
  'MISC' : {
             'pin_lcd_bl_driver' : 'D3', # power for backlight, controlled by a driver IC, active high
             'pin_lcd_touch_vdd' : 'D46' # power for LCD and touchscreen, controlled by a FET, active low
          },
  'ACCEL' : {
          'device' : 'KX023', 'addr' : 0x1f, # this actually is a KX022 but it is close enough to work
          'pin_sda' : 'D11',
          'pin_scl' : 'D14'
          },
};

# left-right, or top-bottom order
board = {
};
board["_css"] = """
#board {
  width: 528px;
  height: 800px;
  top: 0px;
  left : 200px;
  background-image: url(img/ID205.jpg);
}
#boardcontainer {
  height: 900px;
}

#left {
    top: 219px;
    right: 466px;
}
#right {
    top: 150px;
    left: 466px;
}

.leftpin { height: 17px; }
.rightpin { height: 17px; }
""";

def get_pins():
  pins = pinutils.generate_pins(0,47) # 48 General Purpose I/O Pins.
  pinutils.findpin(pins, "PD0", True)["functions"]["XL1"]=0;
  pinutils.findpin(pins, "PD1", True)["functions"]["XL2"]=0;
  pinutils.findpin(pins, "PD9", True)["functions"]["NFC1"]=0;
  pinutils.findpin(pins, "PD10", True)["functions"]["NFC2"]=0;
  pinutils.findpin(pins, "PD2", True)["functions"]["ADC1_IN0"]=0;
  pinutils.findpin(pins, "PD3", True)["functions"]["ADC1_IN1"]=0;
  pinutils.findpin(pins, "PD4", True)["functions"]["ADC1_IN2"]=0;
  pinutils.findpin(pins, "PD5", True)["functions"]["ADC1_IN3"]=0;
  pinutils.findpin(pins, "PD28", True)["functions"]["ADC1_IN4"]=0;
  pinutils.findpin(pins, "PD29", True)["functions"]["ADC1_IN5"]=0;
  pinutils.findpin(pins, "PD30", True)["functions"]["ADC1_IN6"]=0;
  pinutils.findpin(pins, "PD31", True)["functions"]["ADC1_IN7"]=0;
  # Make buttons and LEDs negated
  pinutils.findpin(pins, "PD5", True)["functions"]["NEGATED"]=0;
  pinutils.findpin(pins, "PD7", True)["functions"]["NEGATED"]=0;

  # everything is non-5v tolerant
  for pin in pins:
    pin["functions"]["3.3"]=0;
  #The boot/reset button will function as a reset button in normal operation. Pin reset on PD21 needs to be enabled on the nRF52832 device for this to work.
  return pins
