import smbus2

DEVICE_BUS = 1
DEVICE_ADDR = 0x15

bus = smbus2.SMBus(DEVICE_BUS)

def send_emotion(id):
    hex_values = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09]
    bus.write_byte_data(DEVICE_ADDR, 0x00, hex_values[id])


