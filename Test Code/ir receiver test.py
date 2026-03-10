from machine import Pin,ADC
from time import sleep
from math import ceil

led = Pin(25,  Pin.OUT)
led.on()

testadc = ADC(28)

while True:
    minval = 66000
    maxval = 0
    for i in range (0, 500):
        reading = testadc.read_u16()
        if reading > maxval:
            maxval = reading
        if reading < minval:
            minval = reading
    print("Max value: ", maxval, "Min value: ", minval)
    print(maxval-minval)
    #print(testadc.read_u16())
    #sleep(0.2)
