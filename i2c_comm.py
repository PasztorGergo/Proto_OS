import smbus2

DEVICE_BUS = 1
DEVICE_ADDR = 0x15

bus = smbus2.SMBus(DEVICE_BUS)

def send_emotion(id):
    bus.write_byte_data(DEVICE_ADDR, 0x00, id)


