from machine import Pin,PWM,ADC
from time import sleep
from math import ceil

led = Pin(25,  Pin.OUT)
led.on()
p16 = Pin(16,  Pin.OUT)

duty = ceil(0.5 * 65535)

pwm16 = PWM(p16)

pwm16.freq(1000)
pwm16.duty_u16(duty)