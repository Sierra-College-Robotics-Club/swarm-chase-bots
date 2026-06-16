from machine import Pin,PWM,ADC
from time import sleep,ticks_diff,ticks_add,ticks_ms
from math import ceil

frequency = 1000

led = Pin(25,  Pin.OUT)
led.on()

lastDirection = 'stop'

BOT_NUM = 3

global searchProtocol
searchProtocol = False
global timeLastMoved
timeLastMoved = ticks_ms()
global couer
couer = True

if BOT_NUM == 1:
    midresv = ADC(27)
    leftresv = ADC(28)
    rightresv = ADC(26)
    
    h1 = PWM((2),freq = frequency)
    h2 = PWM((3),freq = frequency)
    h3 = PWM((4),freq = frequency)
    h4 = PWM((5),freq = frequency)

elif BOT_NUM == 2:
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
    
elif BOT_NUM == 3:
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

def irreader(irreceiver):
    minval = 66000
    maxval = 0
    for i in range (0, 100):
        reading = irreceiver.read_u16()
        if reading > maxval:
            maxval = reading
        if reading < minval:
            minval = reading
    irstrength = maxval-minval
    return (irstrength)

def smoothMove(direction, speed):
    global lastDirection
    global timeLastMoved
    global couer
    
    if direction == lastDirection:
        movement(direction, speed)
    elif lastDirection == 'left' and direction == "up" or direction == "down" or direction == "stop":
        movement('stop', speed)
    elif lastDirection == 'right' and direction == "up" or direction == "down" or direction == "stop":
        movement('stop', speed)
    
    couer = False
    timeLastMoved = ticks_ms()
    lastDirection = direction

while True:
    global timeLastMoved
    global searchProtocol
    global couer
    
    irstrengthMid = irreader(midresv)
    irstrengthLeft = irreader(leftresv)
    irstrengthRight = irreader(rightresv)
    
    #print(irstrengthLeft, irstrengthMid, irstrengthRight)
    
    led_r.off()
    led_m.off()
    led_l.off()
    
    currentTime = ticks_ms()
    
    print("currentTime: ", currentTime)
    print("timeLastMoved: ", timeLastMoved)
    if couer == False:
        if ticks_diff(currentTime, timeLastMoved) >= 3000:
            searchProtocol = True
            print("Ahhhhhhhhhh")
    
    if irstrengthLeft >= irstrengthMid and irstrengthLeft >= 2000: #Left
        searchProtocol = False
        smoothMove('left', 0.5)
        led_l.on()
    elif irstrengthRight >= irstrengthMid and irstrengthRight >= 2000: #Right
        searchProtocol = False
        smoothMove('right', 0.5)
        led_r.on()
    elif irstrengthMid > 22000 and not irstrengthRight >= irstrengthMid and not irstrengthLeft >= irstrengthMid: #Backup
        searchProtocol = False
        smoothMove("down", 0.75)
        led_r.on()
        led_l.on()
    elif irstrengthMid > 1000 and irstrengthMid < 5000: #Forward
        searchProtocol = False
        smoothMove("up", 0.9)
        led_m.on()
    else:
        if searchProtocol == True:
            movement('left', 0.5)
        else:
            movement("stop", 0)
            led_r.on()
            led_m.on()
            led_l.on()
            
    sleep(0.025)