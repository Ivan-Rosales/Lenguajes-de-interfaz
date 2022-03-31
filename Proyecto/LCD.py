from time import time
from machine import Pin
import utime


class LCD:
    num_lines = 2
    num_columns = 16
    cursor_x = 0
    cursor_y = 0

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

        self.write_4bits(0x03 >> 4)
        utime.sleep_ms(5)
        self.write_4bits(0x03 >> 4)
        utime.sleep_ms(1)
        self.write_4bits(0x03 >> 4)
        utime.sleep_ms(1)
        
        self.write_4bits(0x02 >> 4)
        utime.sleep_ms(1)
        
        self.write_command(0b1000, 37) # Display apagado
        self.clear()
        self.write_command(0b110, 37) 
        self.write_command(0b1111, 37) # Display encendido
        self.write_command(0b101000, 37) # Establece que seran dos lineas
        
        utime.sleep_ms(20)
        self.clear()

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
        #utime.sleep_us(100)

    def write_command(self, value, delay):
        self.RS.value(0) # intruccion
        self.RW.value(0) # escribir
        self.write_4bits(value >> 4)
        utime.sleep_us(37)
        self.write_4bits(value)
        utime.sleep_us(delay)
        
    def clear(self):
        self.write_command(0x01, 1520) # limpia la pantalla
        self.write_command(0x02, 1520) # posiciona el cursor en (0, 0)
        self.write_command(0b1100, 37) # Display encendido
        self.cursor_x = 0
        self.cursor_y = 0
        
    def write_data(self, value):
        self.RS.value(1) # informacion
        self.RW.value(0) # escribir
        self.write_4bits(value >> 4)
        utime.sleep_us(37)
        self.write_4bits(value)
        
    def set_char(self, char):
        self.write_data(ord(char)) # carga el caracter en la RAM

        self.cursor_x += 1      
        if self.num_columns == self.cursor_x:
            self.cursor_x = 0
            self.cursor_y = int(not self.cursor_y)
        
        cmd = 0x80 | self.cursor_x # 0x80 set RAM | Define la columna en la cual se escribe
        if self.cursor_y == 1:
            cmd |= 0x40 # Define la fila en la cual se escribe
        self.write_command(cmd, 37)
        
        
    def set_string(self, string, ow=False):
        string = string if ow else string[0:32] # Recorta el tamaño de la string si se requiere
        for char in string:
            self.set_char(char)
            
            

