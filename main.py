from machine import Pin,PWM,ADC
from time import sleep
from math import ceil

frequency = 1000

led = Pin(25,  Pin.OUT)
led.on()

lastDirection = 'stop'

#TODO: switch pwm drive to enable pin not the h bridge pins

BOT_NUM = 4

if BOT_NUM == 1:
    midresv = ADC(28)
    leftresv = ADC(27)
    rightresv = ADC(26)
    
    h1 = PWM((2),freq = frequency)
    h2 = PWM((3),freq = frequency)
    h3 = PWM((4),freq = frequency)
    h4 = PWM((5),freq = frequency)

elif BOT_NUM == 2:
    midresv = ADC(27)
    leftresv = ADC(28)
    rightresv = ADC(26)
    
    h1 = PWM((2),freq = frequency)
    h2 = PWM((3),freq = frequency)
    h3 = PWM((4),freq = frequency)
    h4 = PWM((5),freq = frequency)

elif BOT_NUM == 3:
    rightresv = ADC(26)
    midresv = ADC(27)
    leftresv = ADC(28)
    
    led_r = Pin(15,  Pin.OUT)
    led_m = Pin(14,  Pin.OUT)
    led_l = Pin(13,  Pin.OUT)
    
    #h is the motor driver pins (h for H-bridge)
    enable_a = Pin(2,  Pin.OUT)
    enable_a.on()
    h1 = PWM((3),freq = frequency)
    h2 = PWM((4),freq = frequency)
    h3 = PWM((5),freq = frequency)
    h4 = PWM((6),freq = frequency)
    enable_b = Pin(7,  Pin.OUT)
    enable_b.on()
    
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
    
elif BOT_NUM == 4:
    rightresv = ADC(26)
    midresv = ADC(27)
    leftresv = ADC(28)
    
    led_r = Pin(15,  Pin.OUT)
    led_m = Pin(14,  Pin.OUT)
    led_l = Pin(13,  Pin.OUT)
    
    #h is the motor driver pins (h for H-bridge)
    enable_a = PWM((2),freq = frequency)
    h1 = Pin(3, Pin.OUT)
    h2 = Pin(4, Pin.OUT)
    h3 = Pin(5, Pin.OUT)
    h4 = Pin(6, Pin.OUT)
    enable_b = PWM((7),freq = frequency)
    
    def movement(direction, speed):
        enable_a.duty_u16(0)
        enable_b.duty_u16(0)
        h1.off()
        h2.off()
        h3.off()
        h4.off()
    
        if speed > 1:
            speed = 1
        
        duty = ceil(speed * 65535)
        
        enable_a.duty_u16(duty)
        enable_b.duty_u16(duty)
    
        if direction == 'up':
            h1.on()
            h4.on()
        elif direction == 'down':
            h2.on()
            h3.on()
        elif direction == 'right':
            h1.on()
            h3.on()
        elif direction == 'left':
            h2.on()
            h4.on()
        else:
            return False
        print(direction, speed ,duty, frequency)
        return True
        
'''
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
'''
'''
def movement2(direction, speed):
    enable_a.duty_u16(0)
    enable_b.duty_u16(0)
    
    if speed > 1:
        speed = 1
        
    duty = ceil(speed * 65535)
    
    enable_a.duty_u16(duty)
    enable_b.duty_u16(duty)
    
    if direction == 'up':
        h1.on()
        h4.on()
    elif direction == 'down':
        h2.on()
        h3.on()
    elif direction == 'right':
        h1.on()
        h3.on()
    elif direction == 'left':
        h2.on()
        h4.on()
    else: 
        return False
    print(direction, speed ,duty, frequency)
    return True   
'''

def irreader(irreceiver):
    minval = 66000
    maxval = 0
    for i in range (0, 400):
        reading = irreceiver.read_u16()
        if reading > maxval:
            maxval = reading
        if reading < minval:
            minval = reading
    #print("Max value mid: ", maxval, "Min value mid: ", minval)
    irstrength = maxval-minval
    #print(irstrength)
    return (irstrength)

def smoothMove(direction, speed):
    global lastDirection
    
    if direction == lastDirection:
        movement(direction, speed)
        
    lastDirection = direction

while True:
    irstrength = irreader(midresv)
    irstrength2 = irreader(leftresv)
    irstrength3 = irreader(rightresv)
    
    print(irstrength, irstrength2, irstrength3)
    
    led_r.off();
    led_m.off();
    led_l.off();
    
    if irstrength2 >= irstrength and irstrength2 >= 2000: #Left
        smoothMove('left', 0.5)
        led_l.on()
    elif irstrength3 >= irstrength and irstrength3 >= 2000: #Right
        smoothMove('right', 0.5)
        led_r.on()
    elif irstrength > 22000 and not irstrength3 >= irstrength and not irstrength2 >= irstrength:
        smoothMove("down", 0.75)
        led_r.on()
        led_l.on()
    elif irstrength > 1000 and irstrength < 5000: 
        smoothMove("up", 1)
        led_m.on()
    else:
        smoothMove("stop", 0)
        led_r.on();
        led_m.on();
        led_l.on();
    sleep(0.1)
    
    #movement("up", 0.5*(65535-irstrength)/65535)