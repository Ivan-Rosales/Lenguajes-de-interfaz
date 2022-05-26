import json
import threading

from serial.serialutil import SerialException
from uart.serial import Serial


class Uart:
    active = True

    def __init__(self, port, baud, function):
        self.port = port
        self.baud = baud
        self.function = function
        self.con = Serial()
        self.con.port = port
        self.con.baudrate = baud
        try:
            self.con.open()
            watchdog = threading.Thread(target=self.watchdog)
            watchdog.setDaemon(True)
            watchdog.start()
        except SerialException:
            raise Exception("No esta conectado el dispositivo")

    def watchdog(self):
        while self.active:
            try:
                if self.con.in_waiting:
                    data_1 = self.con.readline().decode('ascii')
                    data = json.loads(data_1)
                    response = self.function(data)
                    self.con.write(response)
            except json.decoder.JSONDecodeError:
                response = self.function({'num_control': '', 'password': ''})
                self.con.write(response)
