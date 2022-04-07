from ast import arg
import json
import serial
import threading

from database.database import DB


class Serial:

    def __init__(self, port, baud, function):
        self.port = port
        self.baud = baud
        self.con = serial.Serial(port, baud, timeout=0)
        self.function = function

    def activate(self):
        watchdog = threading.Thread(target=self.watchdog)
        watchdog.setDaemon(True)
        watchdog.start()

    def watchdog(self):
        while True:
            try:
                if self.con.in_waiting:
                    data = json.loads(self.con.readline().decode('ascii'))
                    self.function(data)
            except json.decoder.JSONDecodeError:
                pass
