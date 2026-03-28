# Hardware Notes for ID205

## Specs
Chipset:  Nordic nRF52840
Accelerometer sensor:  KIONIX KX022-1022
Heart rate sensor:  Silicon labs Si1142
Flash:  64Mb = 8 MB
Battery:  210mAh
Display: 240x240 st7789v controller
Touch: IT7259

## Screen Connector (Touch/Display)
| Pin | Display Side      | Main PCB Side         | NRF52   |
| --- | ----------------- | --------------------- | -------- |
| 1   | Display XY        | TP1                   | D30      |
| 2   | Display XY        | TP2                   | D28      |
| 3   | Display XY        | TP3                   | D18      |
| 4   | Display XY        | TP4                   | D19      |
| 5   | GND               | GND                   |          |
| 6   | Touch SDA         | TP6                   | D21      |
| 7   | Touch SCL         | TP7                   | D23      |
| 8   | Touch RDY (Int?)  | TP8                   | D32      |
| 9   | Touch Reset       | TP9                   | D33      |
| 10  | 3.3V Touch, Disp. | TP10, Transistor VDD  | D46      |
| 11  | GND               | GND                   |          |
| 12  | Display XY?       | TP12                  | D2       |
| 13  | Backlight K       | TP13, Transitor GND   | D35 = on |
| 14  | Backlight K       | TP13, Transitor GND   | D35 = on |
| 15  | Backlight A       | TP15, LED Driver?     | D3  = on |
| 16  | Backlight A       | NC? (Empty Footprint) |          |

## Heartrate / Buttons Connector

| Pin | NRF52 / Function         |
| --- | ------------------------ |
| 1   | D41                      |
| 2   | VDD                      |
| 3   | GND                      |
| 4   | GND                      |
| 5   | BAT+                     |
| 6   | BAT+                     |
| 7   | D7 / Button              |
| 8   | ? 0V                     |
| 9   | D5 / Button              |
| 10  | D16, Series R after Flex |
| 11  | D27                      |
| 12  | D24, Series R after Flex |
| 13  | D22                      |
| 14  | D20, Series R after Flex |
| 15  | GND                      |

## Flash 
(XT25F64B, full part name: XT25F64BW016)

| Pin        | NRF52    |
| ---------- | -------- |
| CS#        | D15      |
| SO(IO1)    | D17      |
| WP#(IO2)   | ? 3.3V   |
| HOLD#(IO3) | NC, 3.3V |
| SCLK       | D36      |
| SI(IO0)    | D38      |

## Accelerometer
| Name     | NRF52 |
| -------- | ----- |
| SCL      | D14   |
| SDO/ADDR | D40   |
| SDI/SDA  | D11   |
| INT1     | D12?  |
| nCS      | D13   |

## Labeled Testpoints
| Name | NRF52   |
| ---- | ------- |
| TX   | D31     |
| RX   | D34     |
| DCK  | no GPIO |
| DIO  | no GPIO |

