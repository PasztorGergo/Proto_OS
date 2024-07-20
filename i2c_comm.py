from smbus2 import SMBus, i2c_msg
import RPi.GPIO as GPIO

TEENSY_ADDR = 0x3c
DEVICE_BUS = 1

def send_emotion(id):
    with SMBus(DEVICE_BUS) as bus:
        bus.write_block_data(TEENSY_ADDR, 0x00, [id])

def send_feature(state,feature):
    with SMBus(DEVICE_BUS) as bus:
        bus.write_block_data(TEENSY_ADDR, 0x01, [feature,state])

def send_blink():
    with SMBus(DEVICE_BUS) as bus:
        bus.write_block_data(TEENSY_ADDR, 0x02, [0x01])

