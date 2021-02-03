from machine import Pin, Timer, ADC
from time import sleep

photo = ADC(Pin(28))

while True:
    print(photo.read_u16())
    sleep(1)