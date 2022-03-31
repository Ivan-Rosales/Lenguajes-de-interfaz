import machine
import utime

a = [
    machine.Pin(5, machine.Pin.OUT),
    machine.Pin(7, machine.Pin.OUT),
    machine.Pin(10, machine.Pin.OUT),
    machine.Pin(12, machine.Pin.OUT),
    machine.Pin(28, machine.Pin.OUT),
    machine.Pin(26, machine.Pin.OUT),
    machine.Pin(22, machine.Pin.OUT),
    machine.Pin(19, machine.Pin.OUT),
]

def number_to_port(temp_n):
    n = int(temp_n, 16)
    if 0<= n <=255:
        for i in a:
            i.value(0)
        binario = bin(n)
        cadena = str(binario)[2:]
        for i in range(len(cadena)):
            a[i].value(int(cadena[len(cadena)-1-i]))

while True:
    try:
        number_to_port((input("numero:")))
    except Exception as e:
        print(e)
