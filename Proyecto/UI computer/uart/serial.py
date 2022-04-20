import json
import serial
import threading


class Serial:
    active = True

    def __init__(self, port, baud, function):
        self.port = port
        self.baud = baud
        self.con = serial.Serial(port, baud, timeout=0)
        self.function = function
        watchdog = threading.Thread(target=self.watchdog)
        watchdog.setDaemon(True)
        watchdog.start()

    def watchdog(self):
        while self.active:
            try:
                if self.con.in_waiting:
                    data_1 = self.con.readline().decode('ascii')
                    data = json.loads(data_1)
                    response = self.function(data)
                    self.con.write(str(response)[0].encode())
            except json.decoder.JSONDecodeError as e:
                self.function({'num_control': '', 'password': ''})
