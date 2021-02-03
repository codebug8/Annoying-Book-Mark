from machine import Pin, Timer, PWM

buzzer = PWM(Pin(3))
timer = Timer()
buzz_on = False
buzzer.freq(800)
hour = 60*60

# The duty cycle is defined to be how
# long the pin is high compared with the length of a single period 
def buzz(timer):
    global buzz_on
    if  buzz_on:
        buzzer.duty_u16(0)
    else:
        buzzer.duty_u16(32512)
        
    buzz_on = not buzz_on
    
# timer freq is x over y seconds so 10 is 10/1 so 10 times per second
# a timer of 1/60 is once every minute
timer.init(freq=1, mode=Timer.PERIODIC, callback=buzz)