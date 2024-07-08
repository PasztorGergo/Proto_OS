import serial
from i2c_comm import send_dynamic_emotion
# Initialize serial connection
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

while True:
    data = ser.read(1)  # Read one byte
    with open("db.txt") as fs:
        splitted = fs.readline().replace("\n", "").split()
        if data and splitted[3]:
            eye_state = int(data)
            send_dynamic_emotion(eye_state, splitted[0])