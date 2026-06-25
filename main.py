from machine import Pin,PWM,ADC
from time import sleep,ticks_diff,ticks_add,ticks_ms
from math import ceil

frequency = 1000

led = Pin(25,  Pin.OUT)
led.on()

lastDirection = 'stop'
lastTurnDirection = 'left'

thresholdLow = 1400
thresholdMid = 5000
thresholdLeft = 2150
thresholdRight = 2150
thresholdBackup = 22000

global Spinny_is_on
Spinny_is_on = True
BOT_NUM = 3

global searchProtocol
searchProtocol = False
global timeLastMoved
timeLastMoved = ticks_ms()
global cower
cower = True

switch1 = Pin(10, Pin.IN, Pin.PULL_UP)

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
    global cower
    
    if direction == lastDirection:
        movement(direction, speed)
    elif lastDirection == 'left' and direction == "up" or direction == "down" or direction == "stop":
        movement('stop', speed)
    elif lastDirection == 'right' and direction == "up" or direction == "down" or direction == "stop":
        movement('stop', speed)
    
    cower = False
    timeLastMoved = ticks_ms()
    lastDirection = direction

while True:
    global timeLastMoved
    global searchProtocol
    global cower
    global Spinny_is_on
    
    irstrengthMid = irreader(midresv)
    irstrengthLeft = irreader(leftresv)
    irstrengthRight = irreader(rightresv)
    
    print(irstrengthLeft, irstrengthMid, irstrengthRight)
    
    led_r.off()
    led_m.off()
    led_l.off()
    
    currentTime = ticks_ms()
    
    #print("currentTime: ", currentTime)
    #print("timeLastMoved: ", timeLastMoved)
    if cower == False:
        if Spinny_is_on == True:
            if ticks_diff(currentTime, timeLastMoved) >= 3000:
                searchProtocol = True
                print("Ahhhhhhhhhh")
    
    if irstrengthLeft >= irstrengthMid and irstrengthLeft >= thresholdLeft: #Left
        searchProtocol = False
        lastTurnDirection = 'left'
        smoothMove('left', 0.5)
        led_l.on()
    elif irstrengthRight >= irstrengthMid and irstrengthRight >= thresholdRight: #Right
        searchProtocol = False
        lastTurnDirection = 'right'
        smoothMove('right', 0.5)
        led_r.on()
    elif irstrengthMid > thresholdBackup: #Backup
        searchProtocol = False
        smoothMove("down", 0.75)
        led_r.on()
        led_l.on()
    elif irstrengthMid > thresholdLow and irstrengthMid < thresholdMid: #Forward
        searchProtocol = False
        smoothMove("up", 0.9)
        led_m.on()
    elif irstrengthMid >= thresholdMid: #and < thresholdBackup #Powered stop/TOO CLOSE (stop)
        searchProtocol = False
        movement("stop", 0)
        led_r.on()
        led_m.on()
        led_l.on()

    else: # NO LIGHT DETECTED (light < thresholdLow)
        if searchProtocol == True:
            if lastTurnDirection == 'left':
                movement('left', 0.5)
                print('spinny left')
            if lastTurnDirection == 'right':
                movement('right', 0.5)
                print('spinny right')
        else:
            movement("blindStop", 0)
            led_r.on()
            led_m.on()
            led_l.on()
            
    if switch1.value() == 0:
        print("yelling")
        while switch1.value() == 0:
            pass
        Spinny_is_on = not Spinny_is_on
        
    #print(Spinny_is_on)
    sleep(0.025)
