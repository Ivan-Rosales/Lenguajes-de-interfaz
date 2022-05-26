import serial


class Serial(serial.Serial):

    def write(self, data):
        message = str(data)[0:32].ljust(32)
        return super().write(message.encode())
