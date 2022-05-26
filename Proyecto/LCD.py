from time import time
from machine import Pin
import utime


class LCD:
    num_lines = 2
    num_columns = 16
    cursor_x = 0
    cursor_y = 0
    newline = False

    def __init__(self, RS, RW, EN, D4, D5, D6, D7):
        self.RS: Pin = RS
        self.RW: Pin = RW
        self.EN: Pin = EN
        self.D4: Pin = D4
        self.D5: Pin = D5
        self.D6: Pin = D6
        self.D7: Pin = D7

        self.init()

    def init(self):
        self.RS.value(0)
        self.RW.value(0)
        self.EN.value(0)
        self.D4.value(0)
        self.D5.value(0)
        self.D6.value(0)
        self.D7.value(0)

        utime.sleep_ms(20)

        self.write_4bits(0x30 >> 4)
        utime.sleep_ms(5)
        self.write_4bits(0x30 >> 4)
        utime.sleep_ms(1)
        self.write_4bits(0x30 >> 4)
        utime.sleep_ms(1)
        
        self.write_4bits(0x02 >> 4)
        utime.sleep_ms(1)
        
        self.write_command(0x08)
        self.clear()
        self.write_command(0x06)
        self.write_command(0x0C)
        self.write_command(0x0C)

    def write_4bits(self, data):
        self.D7.value(data & 0x08)
        self.D6.value(data & 0x04)
        self.D5.value(data & 0x02)
        self.D4.value(data & 0x01)
        self.enable()

    def enable(self):
        self.EN.value(0)
        utime.sleep_us(1)
        self.EN.value(1)
        utime.sleep_us(1)
        self.EN.value(0)
        utime.sleep_us(100)

    def write_command(self, value):
        self.RS.value(0)
        self.RW.value(0)
        self.write_4bits(value >> 4)
        self.write_4bits(value)
        if value <= 3:
            utime.sleep_ms(5)
        
    def clear(self):
        self.write_command(0x01)
        self.write_command(0x02)
        self.cursor_x = 0
        self.cursor_y = 0
        
    def write_data(self, value):
        self.RS.value(1)
        self.RW.value(0)
        self.write_4bits(value >> 4)
        self.write_4bits(value)
        
    def set_char(self, char):
        if char == '\n':
            if self.implied_newline:
                pass
            else:
                self.cursor_x = self.num_columns
        else:
            self.write_data(ord(char))
            self.cursor_x += 1
        if self.cursor_x >= self.num_columns:
            self.cursor_x = 0
            self.cursor_y += 1
            self.implied_newline = (char != '\n')
        if self.cursor_y >= self.num_lines:
            self.cursor_y = 0
        self.move_to(self.cursor_x, self.cursor_y)
        
    def move_to(self, cursor_x, cursor_y):
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        addr = cursor_x & 0x3f
        if cursor_y & 1:
            addr += 0x40
        if cursor_y & 2:
            addr += self.num_columns
        self.write_command(0x80 | addr)
        
    def set_string(self, string):
        self.clear()
        string = string[0:32]
        for char in string:
            self.set_char(char)
            
            
