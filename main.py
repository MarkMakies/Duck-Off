###############################################################################
#
# Duck Off Thing
#   using RP2040 Pico, 8x8 LED matrix, PIR movement sensor, microwave presence 
#   sensor, DC to DC step down, simple 2 transistor speaker driver
# v1.01 8/5/23 first try using ultrasonic range finder and H-bridge to drive 
# v2.01 1/6/23 new enclosure, + PIR sensor, + mWave sensor.  ditched ultrasonic
# v2.02 15/6/23 using PlayLists for light and sound, added visual trigger count
#
###############################################################################

StartDelay = 60

# Output to drive transistor pair for 12V 5W horn speaker (NOTE PWM inverted)
from machine import Pin, PWM
Phorn = PWM(Pin(8, Pin.OUT))
Phorn.freq(1000)
Phorn.duty_u16(2**16 - 1)       # this NEEDS to be done ASAP

# HC-SR501 PIR Motion Sensor, after (re)trig -> 2s high then 2s lockout
Ppir = Pin(10, Pin.IN)

# RCWL-0516 Microwave sensor, 1s high then appears to have a 5 sec lockout
Pmwave = Pin(11, Pin.IN)

# GlowBit 8x8 Matrix of LEDs
Pleds = Pin(13,Pin.OUT)

from time import sleep_ms, ticks_ms
from neopixel import NeoPixel as NP
from math import log10

###############################################################################
# LIGHTS

numPixels = 64
LEDs = NP(Pleds, numPixels)
'''
00 01 02 03 04 05 06 07
08 09 10 11 12 13 14 15
16 17 18 19 20 21 22 23
24 25 26 27 28 29 30 31
32 33 34 35 36 37 38 39 
40 41 42 43 44 45 46 47
48 49 50 51 52 53 54 55
56 57 58 59 60 61 62 63
'''
BorderPix = [0,1,2,3,4,5,6,7,15,23,31,39,47,55,63,62,61,60,59,58,57,56,48,40,
            32,24,16,8]
SnakePix =  [9,10,11,12,13,14,22,21,20,19,18,17,25,26,27,28,29,30,38,37,36,35,
            34,33,41,42,43,44,45,46,54,53,52,51,50,49] 

def Fill(R, G, B):
    for i in range(numPixels):
        LEDs[i] = ((R,G,B))
    NP.write(LEDs)

def Border(R, G, B, Dur):  
    if Dur == 0:
        for i in BorderPix:
            LEDs[i] = ((R,G,B))
        NP.write(LEDs)
    else:
        for i in BorderPix:
            LEDs[i] = ((R,G,B))
            NP.write(LEDs)
            sleep_ms(Dur)

def Strobe(R, G, B, Freq, Dur_ms):
    start = ticks_ms()
    delay = int(1 / Freq / 1000 / 2)  # 2 cycles, in ms
    while ticks_ms() < start + Dur_ms:
            Fill(0,0,0)
            sleep_ms(delay)
            Fill(R,G,B)
            sleep_ms(delay)

###############################################################################
# SOUND

def Tone(Freq, Vol):
    # vol expected to be between 0 and 10
    # freq between 30 and 3000
    # higher freq, greater power required, hence AdjVol formula
    if Vol == 0:
        Phorn.duty_u16(2**16 - 1)
    else:
        AdjFreq = int(min(max(Freq, 30), 3000))
        AdjVol = int( 10 ** (log10(AdjFreq) + log10(Vol)))
        Phorn.freq(AdjFreq)
        Phorn.duty_u16(2**16 - AdjVol)

def Beep(Freq, Vol, Dur):
    Tone(Freq, Vol)
    sleep_ms(Dur)
    Tone(Freq, 0)

def Play(I):
    Fstart, Fend, Vstart, Vend, R, G, B, StrobeFreq, Duration = I
    loopDelay = 10
    StrobeFlipCount = max(1, int(1000 / StrobeFreq / 2 / loopDelay))

    numCycles = Duration / loopDelay
    freqStep = (Fend - Fstart) / numCycles
    volStep = (Vend - Vstart) / numCycles

    #print(numCycles, freqStep, volStep, StrobeFlipCount)
    F, V = Fstart, Vstart 
    count = 1
    ff = True

    while count <= numCycles:
        Tone(F, V)
        if ff:
            Fill(R, G, B)
        else:
            Fill(0,0,0)
        F += freqStep
        V += volStep
        count += 1
        if count % StrobeFlipCount == 0:
            ff = not ff

        sleep_ms(loopDelay)

    Tone(0,0)
    Fill(0,0,0)

RampList = [(30, 30, 0, 5,       100, 100, 100,   20,      2000),
            (100, 500, 2, 4,     100, 0, 0,       30,      1000),
            (800, 300, 6, 2,     0, 100, 0,       10,       200),
            (100, 300, 2, 7,     0, 0, 100,       10,       200),
            (100, 300, 6, 2,     155, 155, 155,   50,       200),
            (1060, 60, 5, 7,     100,100,100,     5,        100)]

BlastList = [(3000, 2000, 10, 5,   255,255,255,    50,      400),  
            (1000, 3000, 10, 5,    255,255,255,   100,      600), 
            (30, 50, 10, 8,        255, 0, 0,      40,     1000),
            (1000, 1500, 10, 10,   0, 255, 0,      10,      600),
            (3000, 30, 10, 8,      0, 0, 255,       5,     1000),
            (100, 50, 1, 10,       255, 255, 255,  25,      500),
            (100, 50, 1, 10,       255, 255, 255,  15,      500),
            (100, 50, 1, 10,       255, 255, 255,  10,      500),
            (60, 3000, 5, 10,      255,0,0,        10,      100),
            (30, 3000, 10, 10,     255,255,255,    40,      200)]

#for i in RampList: Play(i)  
#for i in BlastList:  Play(i)  

###############################################################################
# INITIALISE
# We need to wait for the sensors (30-60s) so lets do a fancy count down

Fill(0,0,0)
Border(0,10,0,0)

for i in SnakePix:
    LEDs[i] = ((10,10,10))
NP.write(LEDs)

CountDelay = int(StartDelay * 1000 / len(SnakePix))
for i in SnakePix:
    LEDs[i] = ((0,0,0))
    if not 50 <= i <= 54:
        sleep_ms(CountDelay)
    else:
        sleep_ms(int(CountDelay-(28*20))) # adj for 28 pixels @ 20ms each 
    NP.write(LEDs)
    if i == 54:   
        Beep(200, 1, 100)
        Border(20,0,0,20)        
    if i == 53:
        Border(0,0,0,0)
        Beep(400, 2, 100)
        Border(30,0,0,20)
    if i == 52:
        Border(0,0,0,0)
        Beep(800, 3, 100)
        Border(50,0,0,20)
    if i == 51:
        Border(0,0,0,0)
        Beep(1200, 4, 100)
        Border(100,0,0,20)
    if i == 50:
        Border(0,0,0,0)
        Beep(1500, 5, 100)
        Border(200,0,0,20)     
    if i == 49:
        Tone(0,0)
        Strobe(255,255,255,6,500)

Fill(0,0,0)
Tone(0,0)

###############################################################################
# START main loop

tRamp = 10
tBlast = 10
tWait = 60
tRetrig = 9    

def Pir():
    return Ppir.value() == 1

def Mwave():
    return Pmwave.value() == 1

State = 'Init'
lState = 'blaa'
TrigTime = 0
trig = False
TrigCount = 1

while True:   

    if State != lState:
        lState = State
        print(State)

    if Pir() or Mwave():
        trig = True
        TrigTime = ticks_ms()

    if State == 'Init':
        LEDs[0] = ((10,10,10))
        NP.write(LEDs)
        
        if not (Pir() or Mwave()):
            trig = False
            State = 'Armed'

    elif State == 'Armed':
        LEDs[0] = ((0,10,0))
        LEDs[TrigCount] = ((10,10,0))
        NP.write(LEDs)

        if trig:
            State = 'Ramp'
            TrigCount = min(63, TrigCount + 1)
            RampCount = 0
            StateTime = ticks_ms()

    elif State == 'Ramp':
        Play(RampList[RampCount])
        RampCount = min(len(RampList) - 1, RampCount + 1)

        if TrigTime + (1000 * tRetrig) < ticks_ms():
            Tone(0,0)
            State = 'Recover'
        if StateTime + (1000 * tRamp) < ticks_ms():
            State = 'Blast'
            BlastCount = 0
            StateTime = ticks_ms()

    elif State == 'Blast':
        Play(BlastList[BlastCount])
        BlastCount = min(len(BlastList) - 1, BlastCount + 1)

        if TrigTime + (1000 * tRetrig) < ticks_ms():
            Tone(0,0)
            State = 'Recover'
        if StateTime + (1000 * tBlast) < ticks_ms():
            Tone(0,0)
            StateTime = ticks_ms()
            State = 'Recover'

    elif State == 'Recover':
        Fill(0,0,0)
        LEDs[0] = ((0,0,20))
        NP.write(LEDs)

        if not(Pir() or Mwave()):
            StateTime = ticks_ms()
            State = 'Wait'

    elif State == 'Wait':
        LEDs[0] = ((20,0,0))
        NP.write(LEDs)
        if StateTime + (1000 * tWait) < ticks_ms():
            trig = False
            State = 'Armed'

    #if State != 'Ramp' and State != 'Blast': sleep_ms(100)
    sleep_ms(10)
