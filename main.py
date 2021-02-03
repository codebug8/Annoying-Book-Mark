from machine import Pin, Timer, PWM, ADC

countTimer = Timer()
buzzTimer = Timer()
count_time = 3

segment_one = [
    Pin(9, Pin.OUT),
    Pin(10, Pin.OUT),
    Pin(11, Pin.OUT),
    Pin(18, Pin.OUT),
    Pin(17, Pin.OUT),
    Pin(16, Pin.OUT),
    Pin(8, Pin.OUT)]

segment_two = [
    Pin(13, Pin.OUT),
    Pin(14, Pin.OUT),
    Pin(15, Pin.OUT),
    Pin(22, Pin.OUT),
    Pin(26, Pin.OUT),
    Pin(20, Pin.OUT),
    Pin(12, Pin.OUT)]

max_time = 24
current_time = 0

buzzer = PWM(Pin(2))
buzz_on = False
buzzer.freq(800)
buzzer.duty_u16(0)

book_mark_sensor = ADC(Pin(28))
book_mark_threshold = 1000

def shut_off(segments):
    for segment in segments:
        segment.value(1)
        
def turn_on(segments):
    for segment in segments:
        segment.value(0)
        
def display_num(number, segments):
    numbers = {
        0: lambda segments : turn_on(segments[:6]),
        1: lambda segments : turn_on(segments[2:4]),
        2: lambda segments : turn_on(segments[1:3] + segments[4:]), 
        3: lambda segments : turn_on(segments[1:5] + [segments[6]] ),
        4: lambda segments : turn_on([segments[0]] + segments[2:4] + [segments[6]]),
        5: lambda segments : turn_on(segments[:2] + segments[3:5] + [segments[6]]),
        6: lambda segments : turn_on(segments[:2] + segments[3:7]),
        7: lambda segments : turn_on(segments[1:4]),
        8: lambda segments : turn_on(segments),
        9: lambda segments : turn_on((segments[:5] + [segments[6]]))
    }
    numbers[number](segments)
    
def book_mark_in_use():
    return book_mark_sensor.read_u16() <= book_mark_threshold

def time_is_up():
    global max_time
    global current_time
    return current_time > max_time

def buzz(timer):
    global buzz_on
    if time_is_up() and book_mark_in_use():
        if  buzz_on:
            buzzer.duty_u16(0)
        else:
            buzzer.duty_u16(32512)
            
        buzz_on = not buzz_on
    elif buzz_on and not time_is_up or not book_mark_in_use():
        buzz_on = False
        buzzer.duty_u16(0)
    
def timer_counter(timer):
    global current_time
    if not time_is_up() and book_mark_in_use():
        shut_off(segment_one)
        shut_off(segment_two)
        display_num(current_time//10, segment_one)
        display_num(current_time%10, segment_two)
        current_time += 1
    elif not book_mark_in_use():
        shut_off(segment_one)
        shut_off(segment_two)
        current_time = 0
        
#Init
shut_off(segment_one)
shut_off(segment_two)
countTimer.init(freq=count_time, mode=Timer.PERIODIC, callback=timer_counter)
buzzTimer.init(freq=1, mode=Timer.PERIODIC, callback=buzz)