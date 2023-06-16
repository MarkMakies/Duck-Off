# Duck-Off
Electronic Duck Repeller
Made by Mark Makies, June 2023
   using RP2040 Pico, 8x8 LED matrix, PIR movement sensor, microwave presence 
   sensor, DC to DC step down, simple 2 transistor speaker driver
v1.01 8/5/23 first try using ultrasonic range finder and H-bridge to drive 
v2.01 1/6/23 new enclosure, + PIR sensor, + mWave sensor.  ditched ultrasonic
v2.02 15/6/23 using PlayLists for light and sound, added visual trigger count

detects presence using PIR and Microwave sensors
triggers a two stage sound and light show to scare off ducks
uses 12V 5W horn speaker and 8x8 matrix of LEDs to strobe

# Parts
RP2040 Pico board (or anything that runs Micropyhton
GlowBit 8x8 Matrix of LEDs
RCWL-0516 Microwave sensor
HC-SR501 PIR Motion Sensor
2x 10k resistors
BC547 Bipolar (or whatever is lying around)
IRF610 FET (or whatever is lying around)
12V 5W Horn Speaker
12V -> 3.3V 2A stepdown 
Power source (On standby expect 35mA, but pushing 2A when triggered) 

# 3D Printing
Design files in FreeCAD format
Models in step format
Traslucent PETG used for front- pay particular attention to first layer.
   It must only be one layer thick, but also use 150% flow, otherwise not as watertight
I used the horn bracket to mount as it already allows for angle adjustments

# Usage
After powering on move away and avoid changes for 60 seconds whilst sensors initialise.
A funky count down will signal that it is armed (single green LED)
Upon trigger for either 10 seconds, or 20 if creature has not moved on, an increasingly
louder noise and brighter strobes.  Then a 60 second lockout (single red LED).
When it rearms, as well as the green single LED, another will indicate how many times
it has been triggered since last power cycle (up to 63)

# In Action
https://youtube.com/shorts/f2WUhRsC7lQ?feature=share
