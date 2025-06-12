import RPi.GPIO as GPIO
from config import BTN1_PIN, BTN2_PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup(BTN1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_pressed(pin):
    return GPIO.input(pin) == GPIO.LOW