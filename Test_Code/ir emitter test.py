from machine import Pin,PWM,ADC
from time import sleep
from math import ceil

whatcode = "new"

if whatcode == "old":
    #OG code
    led = Pin(25,  Pin.OUT)
    led.on()
    p16 = Pin(20,  Pin.OUT)

    duty = ceil(0.5 * 65535)

    pwm16 = PWM(p16)

    pwm16.freq(1000)
    pwm16.duty_u16(duty)

if whatcode == "new":
    led = Pin(25,  Pin.OUT)
    led.on()

    pin12 = Pin(12, Pin.IN)
    pin16 = Pin(20,  Pin.OUT)

    pwm16 = PWM(pin16)
    duty = ceil(0.5 * 65535)
    value = 0

    def pulse_on(pin):
        global value
        if pin.value() == 1:
            print('On')
            value = 1
        else:
            print('Off')
            value = 0
    
    pin12.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=pulse_on)

    while True:
        if value == 1:
            pwm16 = PWM(pin16)
            pwm16.freq(1000)
            pwm16.duty_u16(duty)
            #print('1')
            sleep(0.1)
        elif value == 0:
            pwm16.deinit()
            #print('0')
            sleep(0.1)