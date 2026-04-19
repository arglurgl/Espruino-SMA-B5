/*
 * ----------------------------------------------------------------------------------------
 * ITE IT7259 Touchscreen Driver Implementation
 * Hardware driver for IT7259 touch controller with I2C interface
 * Based on https://android.googlesource.com/kernel/msm/+/android-msm-mullet-3.18-nougat-dr1-wear/drivers/input/touchscreen/it7259_ts_i2c.c
 * ----------------------------------------------------------------------------------------
 */

#include <stdbool.h>
#include "jshardware.h"
#include "jspin.h"
#include "jsi2c.h"
#include "jsvar.h"
#include "jsinteractive.h"
#include "it7259.h"

// Command Status Bits (from BUF_QUERY)
#define IT7259_CMD_STATUS_BITS       0x07
#define IT7259_CMD_STATUS_DONE       0x00
#define IT7259_CMD_STATUS_BUSY       0x01
#define IT7259_CMD_STATUS_ERROR      0x02

// Query Buffer Status Bits
#define IT7259_QUERY_NEW_PACKET      0x80  // Bit 7: New packet available
#define IT7259_QUERY_CURRENTLY_TOUCHED 0x40  // Bit 6: Currently touched

// Commands
#define IT7259_CMD_IDENT_CHIP        0x00

// Local I2C interface for touchscreen
static JshI2CInfo i2cIT7259;
static bool i2cIT7259_initialized = false;

// Forward declaration for static helper function
static unsigned char it7259_read_query_buffer(void);

void it7259_power_down(void) {
  // IT7259 can simply be powered down by setting the reset pin low
  jshPinOutput(TOUCH_PIN_RST, 0);
}

void it7259_power_up(void) {
  // Initialize I2C interface on first power up
  if (!i2cIT7259_initialized) {
    jshI2CInitInfo(&i2cIT7259);
    i2cIT7259.bitrate = 0x7FFFFFFF; // make it as fast as we can go
    i2cIT7259.pinSDA = TOUCH_PIN_SDA;
    i2cIT7259.pinSCL = TOUCH_PIN_SCL;
    jsi2cSetup(&i2cIT7259);
    i2cIT7259_initialized = true;
  }
  
  // IT7259: wake from reset power-down
  jshPinOutput(TOUCH_PIN_RST, 1);  
  // Wait for device to be ready (status in BUF_QUERY = 0x00)
  unsigned char status;
  int ready_count = 0;
  do {
    status = it7259_read_query_buffer() & IT7259_CMD_STATUS_BITS;
    if (status != IT7259_CMD_STATUS_DONE) {
      jshDelayMicroseconds(5000);
      ready_count++;
    }
  } while (status != IT7259_CMD_STATUS_DONE && ready_count < 100); // max ~500ms wait
  
  if (ready_count > 0)
    jsiConsolePrintf("IT7259: Waited %dms for device ready\n", ready_count * 5);
  
  // Set up for normal operation
  // Debug: read device name (CMD_IDENT_CHIP = 0x00)
  unsigned char dev_name_buf[10];
  unsigned char cmd_buf[2];
  cmd_buf[0] = IT7259_BUFFER_TYPE_COMMAND;
  cmd_buf[1] = IT7259_CMD_IDENT_CHIP;
  jsi2cWrite(&i2cIT7259, TOUCH_ADDR, 2, cmd_buf, true);
  jshDelayMicroseconds(1000);
  
  // Check command status in BUF_QUERY
  status = it7259_read_query_buffer() & IT7259_CMD_STATUS_BITS;
  if (status == IT7259_CMD_STATUS_BUSY) {
    jsiConsolePrintf("IT7259: Device busy, retrying...\n");
    jshDelayMicroseconds(10000);
    status = it7259_read_query_buffer() & IT7259_CMD_STATUS_BITS;
  }
  if (status != IT7259_CMD_STATUS_DONE) {
    jsiConsolePrintf("IT7259: Command failed with status 0x%02x\n", status);
  }
  
  // Read response from BUF_RESPONSE
  jsi2cReadReg(&i2cIT7259, TOUCH_ADDR, IT7259_BUFFER_TYPE_RESPONSE, 10, dev_name_buf);
  // Response format: byte[0]=length, bytes[1-8]="ITE7259", bytes[8-9]=revision
  jsiConsolePrintf("IT7259 Device ID: %c%c%c%c%c%c%c (Rev: %02x %02x)\n",
    dev_name_buf[1], dev_name_buf[2], dev_name_buf[3], dev_name_buf[4],
    dev_name_buf[5], dev_name_buf[6], dev_name_buf[7],
    dev_name_buf[8], dev_name_buf[9]);
}

void it7259_write_reg(unsigned char reg, unsigned char data) {
  // Ensure I2C is initialized
  if (!i2cIT7259_initialized) {
    it7259_power_up();
  }
  jsi2cWriteReg(&i2cIT7259, TOUCH_ADDR, reg, data);
}

unsigned char it7259_read_reg(unsigned char reg) {
  // Ensure I2C is initialized
  if (!i2cIT7259_initialized) {
    it7259_power_up();
  }
  unsigned char val;
  jsi2cReadReg(&i2cIT7259, TOUCH_ADDR, reg, 1, &val);
  return val;
}

JsVar *it7259_read_regs(unsigned char reg, unsigned int count) {
  // Ensure I2C is initialized
  if (!i2cIT7259_initialized) {
    it7259_power_up();
  }
  unsigned char buf[count];
  jsi2cReadReg(&i2cIT7259, TOUCH_ADDR, reg, count, buf);
  JsVar *arr = jsvNewTypedArray(ARRAYBUFFERVIEW_UINT8, count);
  for (unsigned int i=0; i<count; i++) {
    jsvSetArrayItem(arr, i, jsvNewFromInteger(buf[i]));
  }
  return arr;
}

// Helper function: Read query buffer and return its status byte
// Bits: 7=new_packet (IT7259_QUERY_NEW_PACKET), 6=currently_touched (IT7259_QUERY_CURRENTLY_TOUCHED), 1-0=command_status
static unsigned char it7259_read_query_buffer(void) {
  unsigned char status;
  jsi2cReadReg(&i2cIT7259, TOUCH_ADDR, IT7259_BUFFER_TYPE_QUERY, 1, &status);
  return status;
}

bool it7259_get_event(unsigned char *out_gesture, unsigned char *out_points, uint16_t *out_x, uint16_t *out_y) {
  // Ensure I2C is initialized
  if (!i2cIT7259_initialized) {
    return false;
  }

  unsigned char buf[14];
  unsigned char gesture = 0;
  unsigned char points = 0;
  uint16_t x = 0, y = 0;

  // First check query buffer to see if there's new data
  unsigned char query_status = it7259_read_query_buffer();
  bool new_packet = (query_status & IT7259_QUERY_NEW_PACKET) != 0;
  
  if (!new_packet) {
    return false;  // No new data available
  }

  // Read point information buffer
  jsi2cReadReg(&i2cIT7259, TOUCH_ADDR, IT7259_BUFFER_TYPE_POINT_INFO, 14, buf);
  uint8_t format_tag = (buf[0] & 0xF0) >> 4;

  switch (format_tag) {
    case IT7259_FORMAT_TAG_POINT_DATA:
      // Check for point 0
      if ((buf[0] & 0x01) != 0) {
        x = buf[2] | ((buf[3] & 0x0F) << 8);
        y = buf[4] | ((buf[3] & 0xF0) << 4);
        points = 1;
      } else {
        points = 0;
      }
      *out_gesture = 0;
      break;

    case IT7259_FORMAT_TAG_GESTURE: {
      uint8_t gesture_id = buf[1];
      switch (gesture_id) {
        case 0x20: // tap
          gesture = 5; // single click
          x = buf[3] << 8 | buf[2];
          y = buf[5] << 8 | buf[4];
          points = 1;
          break;
        case 0x21: // press
          gesture = 0x0C; // long touch
          x = buf[3] << 8 | buf[2];
          y = buf[5] << 8 | buf[4];
          points = 1;
          break;
        case 0x22: // flick
          switch (buf[10] & 0x0F) {
            case 0x08: gesture = 2; break; // slide up
            case 0x0C: gesture = 1; break; // slide down
            case 0x0E: gesture = 3; break; // slide left
            case 0x0A: gesture = 4; break; // slide right
            default: return false;
          }
          points = 0;
          break;
        case 0x23: // double tap
          gesture = 0x0B; // double touch
          x = buf[3] << 8 | buf[2];
          y = buf[5] << 8 | buf[4];
          points = 1;
          break;
        default:
          return false;
      }
      *out_gesture = gesture;
      break;
    }

    case IT7259_FORMAT_TAG_TOUCH_EVENT:
    case IT7259_FORMAT_TAG_WAKEUP:
      return false; // ignore these

    default:
      return false;
  }

  *out_points = points;
  *out_x = x;
  *out_y = y;
  return true;
}
