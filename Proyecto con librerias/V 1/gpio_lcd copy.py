from lcd_api import LcdApi
from machine import Pin
from utime import sleep_ms, sleep_us


class GpioLcd(LcdApi):
    """Implements a HD44780 character LCD connected via ESP32 GPIO pins."""

    def __init__(self, rs_pin, enable_pin, d0_pin=None, d1_pin=None,
                 d2_pin=None, d3_pin=None, d4_pin=None, d5_pin=None,
                 d6_pin=None, d7_pin=None, rw_pin=None, backlight_pin=None,
                 num_lines=2, num_columns=16):
        """Constructs the GpioLcd object. All of the arguments must be machine.Pin
        objects which describe which pin the given line from the LCD is
        connected to.
        When used in 4-bit mode, only D4, D5, D6, and D7 are physically
        connected to the LCD panel. This function allows you call it like
        GpioLcd(rs, enable, D4, D5, D6, D7) and it will interpret that as
        if you had actually called:
        GpioLcd(rs, enable, d4=D4, d5=D5, d6=D6, d7=D7)
        The enable 8-bit mode, you need pass d0 through d7.
        The rw pin isn't used by this library, but if you specify it, then
        it will be set low.
        """
        
        

        LcdApi.__init__(self, num_lines, num_columns)
        
        if num_lines > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)

    def hal_pulse_enable(self):
        """Pulse the enable line high, and then low again."""
        self.enable_pin.value(0)
        sleep_us(1)
        self.enable_pin.value(1)
        sleep_us(1)       # Enable pulse needs to be > 450 nsec
        self.enable_pin.value(0)
        sleep_us(100)     # Commands need > 37us to settle

    def hal_write_init_nibble(self, nibble):
        """Writes an initialization nibble to the LCD.
        This particular function is only used during initialization.
        """
        self.hal_write_4bits(nibble >> 4)

    def hal_backlight_on(self):
        """Allows the hal layer to turn the backlight on."""
        if self.backlight_pin:
            self.backlight_pin.value(1)

    def hal_backlight_off(self):
        """Allows the hal layer to turn the backlight off."""
        if self.backlight_pin:
            self.backlight_pin.value(0)

    def hal_write_command(self, cmd):
        """Writes a command to the LCD.
        Data is latched on the falling edge of E.
        """
        self.rs_pin.value(0)
        self.hal_write_8bits(cmd)
        if cmd <= 3:
            # The home and clear commands require a worst
            # case delay of 4.1 msec
            sleep_ms(5)

    def hal_write_data(self, data):
        """Write data to the LCD."""
        self.rs_pin.value(1)
        self.hal_write_8bits(data)

    def hal_write_8bits(self, value):
        """Writes 8 bits of data to the LCD."""
        if self.rw_pin:
            self.rw_pin.value(0)
        if self._4bit:
            self.hal_write_4bits(value >> 4)
            self.hal_write_4bits(value)
        else:
            self.d3_pin.value(value & 0x08)
            self.d2_pin.value(value & 0x04)
            self.d1_pin.value(value & 0x02)
            self.d0_pin.value(value & 0x01)
            self.hal_write_4bits(value >> 4)

    def hal_write_4bits(self, nibble):
        """Writes 4 bits of data to the LCD."""
        self.d7_pin.value(nibble & 0x08)
        self.d6_pin.value(nibble & 0x04)
        self.d5_pin.value(nibble & 0x02)
        self.d4_pin.value(nibble & 0x01)
        self.hal_pulse_enable()