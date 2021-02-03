from machine import Pin, Timer
from time import sleep

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

timer = Timer()
seg1_count = 0;
seg2_count = 0;
cycle_test = False
num_test = True

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
    
def segment_on(timer):
    global seg1_count
    global seg2_count
    if seg1_count < 7:
        segment_one[seg1_count].value(0)
        seg1_count += 1
    elif seg2_count < 7:
        segment_two[seg2_count].value(0)
        seg2_count += 1
    else:
        seg1_count = 0
        seg2_count = 0
        shut_off(segment_one)
        shut_off(segment_two)
        
if cycle_test:
    timer.init(freq=1, mode=Timer.PERIODIC, callback=segment_on)
elif num_test:
    display_test = 0
    while num_test:
        display_num(display_test, segment_one)
        display_num(display_test, segment_two)
        sleep(1)
        shut_off(segment_two)
        shut_off(segment_one)
        sleep(1)
        display_test += 1
        if display_test > 9:
            display_test = 0
