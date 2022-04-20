from machine import Pin, SPI
import utime, select, sys

from LCD import LCD
from mfrc522 import MFRC522

# lcd
RS = Pin(9, Pin.OUT)
RW = Pin(10, Pin.OUT)
EN = Pin(11, Pin.OUT)
D4 = Pin(12, Pin.OUT)
D5 = Pin(13, Pin.OUT)
D6 = Pin(14, Pin.OUT)
D7 = Pin(15, Pin.OUT)

pantalla = LCD(RS=RS, RW=RW, EN=EN, D4=D4, D5=D5, D6=D6, D7=D7)

# rfid
sck = Pin(18, Pin.OUT)
mosi = Pin(19, Pin.OUT)
miso = Pin(16, Pin.OUT)
spi = SPI(0, baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

sda = Pin(17, Pin.OUT)
rst = Pin(22, Pin.OUT)
rdr = MFRC522(spi, sda, rst)

# usb serial port
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

# leds
true = Pin(26, Pin.OUT)
false = Pin(27, Pin.OUT)

while True:
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            print(rdr.read_data())
            
            wait = poll.poll()
            res = wait[0][0].read(1)
            pantalla.set_string(res)
            if res == "T":
                true.value(1)
            elif res == "F":
                false.value(1)
            utime.sleep(2)
            true.value(0)
            false.value(0)