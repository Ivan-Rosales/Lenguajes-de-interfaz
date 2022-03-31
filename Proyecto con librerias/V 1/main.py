import time
from machine import Pin, SPI
from mfrc522 import MFRC522
from gpio_lcd import GpioLcd
import json

led = Pin(25, Pin.OUT)
true = Pin(15, Pin.OUT)
false = Pin(14, Pin.OUT)

#sck = Pin(6, Pin.OUT)
#mosi = Pin(7, Pin.OUT)
#miso = Pin(4, Pin.OUT)
#sda = Pin(5, Pin.OUT)
rst = Pin(22, Pin.OUT)
spi = SPI(0, baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

false = Pin(16, Pin.OUT)
true = Pin(17, Pin.OUT)

lcd = GpioLcd(rs_pin=Pin(8),
              enable_pin=Pin(9),
              d4_pin=Pin(10),
              d5_pin=Pin(11),
              d6_pin=Pin(12),
              d7_pin=Pin(13),
              num_lines=2, num_columns=16)

while True:
    rdr = MFRC522(spi, sda, rst)
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        led.value(1)
        lcd.clear()
        (stat, raw_uid) = rdr.anticoll()
        
        try:
            uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
            
            with open("users.json", 'r') as file:
                users = json.load(file)
            
            if uid in users:
                lcd.putstr(f"Welcome         {users[uid]}")
                print(f"tarjeta leida, user:{users[uid]}, id:{uid}")
                true.value(1)
            else:
                lcd.putstr(f"Usuario denegado{uid}")
                print(f"tarjeta leida, id:{uid}")
                false.value(1)
        except Exception as e:
            print(e)
        
        time.sleep(1.2)
        true.value(0)
        false.value(0)
        led.value(0)
        lcd.clear()
e
