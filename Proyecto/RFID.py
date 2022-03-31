class SPI:
    def __init__(self, SCLK, MOSI, MISO):
        self.SCLK = SCLK
        self.MOSI = MOSI
        self.MISO = MISO

        self.init()

    def init(self):
        pass


class RFID:

    def __init__(self, SCK, MOSI, MISO, SDA, RST):
        self.SDA = SDA
        self.RST = RST
        self.SPI = SPI(SCK, MOSI, MISO) 
