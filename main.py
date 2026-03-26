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

midresv = ADC(28)
leftresv = ADC(27)
rightresv = ADC(26)

def movement(direction, speed):
    
    h1.duty_u16(0)
    h2.duty_u16(0)
    h3.duty_u16(0)
    h4.duty_u16(0)
    
    if speed > 1:
        speed = 1
        
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

while True:
    minval = 66000
    maxval = 0
    for i in range (0, 500):
        reading = midresv.read_u16()
        if reading > maxval:
            maxval = reading
        if reading < minval:
            minval = reading
    print("Max value: ", maxval, "Min value: ", minval)
    irstrength = maxval-minval
    print(irstrength)
    if irstrength > 22000:
        movement("down", 0.75)
    elif irstrength > 1000 and irstrength < 5000:
        movement("up", 1)
    else:
        movement("stop", 0)
    
    #movement("up", 0.5*(65535-irstrength)/65535)