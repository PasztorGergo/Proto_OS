import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

fan = GPIO.PWM(12, 100)
fan.start(0)

def set_fan_speed(percent):
    if percent >= 0 or percent <= 100:
        fan.ChangeDutyCycle(percent)
