import json
import time
import serial
import threading


port = "COM7"
baud = 9600
con = serial.Serial(port, baud, timeout=0)

while True:
    mensaje = "Hola Mundo xd"
    print(mensaje)
    con.write(mensaje.encode("UTF8"))
    time.sleep(1)
