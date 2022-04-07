"""import serial, sqlite3, json, time
from tkinter import Tk

port = "COM7"
baud = 112500

con_micro = serial.Serial(port, baud, timeout=0)
con_datab = sqlite3.connect("app.db")
cur = con_datab.cursor()

while True:
    try:
        if3 con_micro.in_waiting:
            user = json.loads(con_micro.readline().decode('ascii'))
            data = cur.execute(f"SELECT * FROM user WHERE num_control='{user['num_control']}' and password='{user['password']}'")
            
            result = data.fetchall()

            if len(result) == 1:
                c
            else:
                print(f"Acceso denegado")
    except json.decoder.JSONDecodeError:
        pass
"""
from pip import main
from ui.UI import init
from uart.serial import Serial
from database.database import DB


if __name__ == '__main__':
    db = DB()
    main = init(db)
    serial = Serial("COM7", 112500, main.set_string)

    serial.activate()
    main.start()
