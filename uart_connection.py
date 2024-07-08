import serial
from i2c_comm import send_dynamic_emotion
# Initialize serial connection
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

while True:
    data = ser.read(1)  # Read one byte
    if data:
        with open("db.txt") as fs:
            splitted = fs.readline().split()
            eye_state = int(data)
            send_dynamic_emotion(eye_state, splitted[0])