/*
 * ----------------------------------------------------------------------------------------
 * ITE IT7259 Touchscreen Driver
 * Hardware driver for IT7259 touch controller with I2C interface
 * ----------------------------------------------------------------------------------------
 */

#ifndef IT7259_H
#define IT7259_H

#include "jsvar.h"

// IT7259 Buffer Types
#define IT7259_BUFFER_TYPE_COMMAND   0x20
#define IT7259_BUFFER_TYPE_QUERY     0x80
#define IT7259_BUFFER_TYPE_RESPONSE  0xA0
#define IT7259_BUFFER_TYPE_POINT_INFO 0xE0

// Data Format Tags
#define IT7259_FORMAT_TAG_POINT_DATA    0x0
#define IT7259_FORMAT_TAG_GESTURE       0x8
#define IT7259_FORMAT_TAG_TOUCH_EVENT   0x4
#define IT7259_FORMAT_TAG_WAKEUP        0x1

/**
 * Power up the IT7259 touchscreen and initialize it
 * Waits for device ready and reads/displays device identification
 */
void it7259_power_up(void);

/**
 * Power down the IT7259 touchscreen
 * Sets reset pin low to put device into low power state
 */
void it7259_power_down(void);

/**
 * Write a register on the IT7259 touchscreen
 */
void it7259_write_reg(unsigned char reg, unsigned char data);

/**
 * Read a single byte from the IT7259 touchscreen
 */
unsigned char it7259_read_reg(unsigned char reg);

/**
 * Read multiple bytes from the IT7259 touchscreen
 */
JsVar *it7259_read_regs(unsigned char reg, unsigned int count);

/**
 * Process touch interrupt and write results to output parameters
 * Returns: true if valid touch/gesture event, false otherwise
 * Output: gesture code, touch point count, x, y coordinates
 */
bool it7259_get_event(unsigned char *out_gesture, unsigned char *out_points, uint16_t *out_x, uint16_t *out_y);

#endif // IT7259_H
