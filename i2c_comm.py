from smbus2 import SMBus

TEENSY_ADDR = 0x3c
DEVICE_BUS = 1

def send_emotion(id):
    with SMBus(DEVICE_BUS) as bus:
        bus.write_byte_data(TEENSY_ADDR, 0x00, id)
