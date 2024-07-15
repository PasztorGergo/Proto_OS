import serial
import time
from i2c_comm import send_blink
# Initialize serial connection
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

while True:
    data = ser.read(1)  # Read one byte
    with open("db.txt") as fs:
        splitted = fs.readline().replace("\n", "").split()
        if data and eval(splitted[3]):
            eye_state = int(data)
            try:
                send_blink()
            except:
                time.sleep(2.5)