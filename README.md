
# Duck Off
<img src="https://github.com/MarkMakies/Duck-Off/blob/main/Version%202%20PIR%20and%20uWave%20in%20neck"  width=50% height=50%>

**Electronic Duck Repeller**

## What's it do?
Scares ducks off my jetty when they get too close so I don't have to cleanup endless amounts of duck poo!

## How does it work?  
It detects presence using PIR and microwave sensors which triggers a two stage sound and light show.
It uses a 12V 5W horn speaker and 8x8 matrix of LEDs to strobe

## Parts
- RP2040 Pico board (or anything that runs Micropyhton
- GlowBit 8x8 Matrix of LEDs
- RCWL-0516 Microwave sensor
- HC-SR501 PIR Motion Sensor
- 2x 10k resistors
- BC547 Bipolar (or whatever is lying around)
- IRF610 FET (or whatever is lying around)
- 12V 5W Horn Speaker
- 12V -> 3.3V 2A stepdown 
- Power source (On standby expect 35mA, but pushing 2A when triggered) 

## 3D Printing
- Design files in FreeCAD format
- Models in step format
- Traslucent PETG used for front- pay particular attention to first layer.  It must only be one layer thick, but also use 150% flow, otherwise not as watertight

## Usage
- After powering on move away and avoid changes for 60 seconds whilst sensors initialise.
- A funky count down will signal that it is armed (single green LED).
- Upon trigger, for either 10 seconds, or 20 if creature has not moved on, an increasingly louder noise and brighter strobes.  
- Then a 60 second lockout (single red LED).
- When it rearms, as well as the green single LED, another will indicate how many time it has been triggered since last power cycle (up to 63)

## Videos
- On the jetty:  https://youtube.com/shorts/f2WUhRsC7lQ?feature=share
- On the desk:   https://youtube.com/shorts/twOLctHPTis?feature=share
