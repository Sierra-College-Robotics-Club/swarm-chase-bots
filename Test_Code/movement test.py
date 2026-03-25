from machine import Pin,PWM,ADC
from time import sleep
from math import ceil

frequency = 1000

led = Pin(25,  Pin.OUT)
led.on()

h1 = PWM((2),freq = frequency)
h2 = PWM((3),freq = frequency)
h3 = PWM((4),freq = frequency)
h4 = PWM((5),freq = frequency)

'''
testadc = ADC(28)

while True:
    print(testadc.read_u16())
    sleep(1)
'''

def movement(direction, speed):
    
    h1.duty_u16(0)
    h2.duty_u16(0)
    h3.duty_u16(0)
    h4.duty_u16(0) 
    duty = ceil(speed * 65535)
    
    if direction == "up":
        h1.duty_u16(duty)
        h4.duty_u16(duty)
    elif direction == "down":
        h2.duty_u16(duty)
        h3.duty_u16(duty)
    elif direction == "right":
        h1.duty_u16(duty)
        h3.duty_u16(duty)
    elif direction == "left":
        h2.duty_u16(duty)
        h4.duty_u16(duty)
    else:
        return False
    print(direction, speed ,duty, frequency)
    return True

movement("up", 0.5)