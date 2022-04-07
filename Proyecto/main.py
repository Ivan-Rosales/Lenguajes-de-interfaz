from LCD import LCD
from machine import Pin, SPI
import time

RS = Pin(9, Pin.OUT)
RW = Pin(10, Pin.OUT)
EN = Pin(11, Pin.OUT)
D4 = Pin(12, Pin.OUT)
D5 = Pin(13, Pin.OUT)
D6 = Pin(14, Pin.OUT)
D7 = Pin(15, Pin.OUT)

SCK = Pin(17, Pin.OUT)
MOSI = Pin(18, Pin.OUT)
MISO = Pin(19, Pin.OUT)
SDA = Pin(16, Pin.OUT)
RST = Pin(20, Pin.OUT)
    
for i in range(100000000):
    pantalla = LCD(RS=RS, RW=RW, EN=EN, D4=D4, D5=D5, D6=D6, D7=D7)
    pantalla.set_string(str(i))
    print({
        "data": i
        })
    time.sleep(2)