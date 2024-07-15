from smbus2 import SMBus
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

TEENSY_ADDR = 0x3c
DEVICE_BUS = 1

def send_static_emotion(id):
    with SMBus(DEVICE_BUS) as bus:
        bus.write_block_data(TEENSY_ADDR, 0x00, [0b00,id])

def send_dynamic_emotion(eye,id):
    with SMBus(DEVICE_BUS) as bus:
        bus.write_block_data(TEENSY_ADDR, 0x01, [0b01,eye,id])

def send_secondary_feature(state,feature):
    with SMBus(DEVICE_BUS) as bus:
        bus.write_block_data(TEENSY_ADDR, 0x02, [0b10,state,feature])

def send_primary_feature(state,feature):
    with SMBus(DEVICE_BUS) as bus:
        bus.write_block_data(TEENSY_ADDR, 0x03, [0b11,state,feature])


