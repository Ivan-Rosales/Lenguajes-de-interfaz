from machine import Pin, SPI
import utime, select, sys

from LCD import LCD
from mfrc522 import MFRC522

state = Pin(25, Pin.OUT)

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

# usb serial port
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

# leds
true = Pin(26, Pin.OUT)
false = Pin(27, Pin.OUT)
state = Pin(25, Pin.OUT)


while True:
    try:
        rdr = MFRC522(spi, sda, rst)
        
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                state.value(1)
                print(rdr.read_data())
                state.value(0)

                wait = poll.poll()
                res = wait[0][0].read(32)
                state.value(0)
    
                if res.strip() == "False":
                    false.value(1)
                    pantalla.set_string("Acceso Denegado")
                else:
                    true.value(1)
                    pantalla.set_string(res)
                
                utime.sleep(1)
                true.value(0)
                false.value(0)
                pantalla.clear()
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)
        true.value(1)
        false.value(1)
        utime.sleep(3)
