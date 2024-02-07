#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

#include defined functions
from DirectionFcn import GetDirectionByAngel, GetDirectionByRate
from FillMap import FillMap

from sys import version
import csv

# Define the Constants
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4
GREEN = 12
WHITE = 55
THRESHOLD = (GREEN + WHITE) / 2
DRIVE_SPEED = 30 
PROPORTIONAL_GAIN = 3.8  
MAP_ITEM_SIZE=10
ROWS = 200
COLS = 200


LandMap = [ [ 0 for i in range(ROWS) ] for j in range(COLS) ]
data = DataLog('time', 'Angle', 'Delta', 'Distance', name='TrackLog', timestamp=False, extension='csv')
mapMyfile = DataLog('','', name='LandMap', timestamp=False, extension='csv')


# Initialize the EV3 Brick.
ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
line_sensor = ColorSensor(Port.S4)
obstacle_sensor = InfraredSensor(Port.S1)
robot = DriveBase(left_motor, right_motor, wheel_diameter=33, axle_track=174)


CurrentDirection = 1    #starting direction has to be up
PreviousDirection=1     #starting direction
EdgeCompleted = True
map_row = 0
map_col = 0
PreviousDistance = 0
PrevAngel = 0
watch = StopWatch()


robot.reset()




# Start following the line endlessly.
while EdgeCompleted:

    if obstacle_sensor.distance() < 15:
        robot.stop()
        continue

    deviation = line_sensor.reflection() - THRESHOLD
    turn_rate = PROPORTIONAL_GAIN * deviation

    robot.drive(DRIVE_SPEED, turn_rate)
    
    CurrentAngel = robot.angle()
    CurrentDirection = GetDirectionByAngel(PreviousDirection, CurrentAngel,PrevAngel)
    CurrentDistance = robot.distance()

    data.log(watch.time()/1000, CurrentAngel, CurrentAngel-PrevAngel, CurrentDistance)
    
    
    if CurrentDirection == UP:
        if (CurrentDistance - PreviousDistance) >= MAP_ITEM_SIZE and CurrentDistance != 0:   
            LandMap[map_row][map_col] = 1
            map_row += 1
            PreviousDistance = CurrentDistance
        if (CurrentDistance - PreviousDistance) >= MAP_ITEM_SIZE:
            LandMap[map_row][map_col] = 1
            map_row -= 1    
            PreviousDistance = CurrentDistance             
    elif CurrentDirection == RIGHT:
        if (CurrentDistance - PreviousDistance) >= MAP_ITEM_SIZE:
            LandMap[map_row][map_col] = 1
            map_col += 1
            PreviousDistance = CurrentDistance
    elif CurrentDirection == LEFT: 
        if (CurrentDistance - PreviousDistance) >= MAP_ITEM_SIZE:
            LandMap[map_row][map_col] = 1
            map_col -= 1
            PreviousDistance = CurrentDistance
        if map_col -1 == -1:
            robot.stop()
            EdgeCompleted = False
            robot.turn(98)
  

    PrevAngel = CurrentAngel
    PreviousDirection = CurrentDirection

    wait(25)



FillMap(LandMap)

def turnRight():
    robot.turn(98)
    robot.straight(70)
    robot.turn(98)
def turnLeft():
    robot.turn(-98)
    robot.straight(70)
    robot.turn(-98)


turned = False
size = 0
othersize = 0

#Code for cutting grass  
for col in range(0,COLS,7):
    size = 0
    for row in range(ROWS):
        if LandMap[row][col] == 1:
            size+=1
    if size == othersize and size != 0 and othersize != 0:
        robot.straight(size*MAP_ITEM_SIZE)
        if turned == False:   
            turnRight()
            turned = True
        else:
            turnLeft()
            turned = False
    elif size != othersize and othersize != 0 and size != 0:
        if turned == False:
            robot.straight(size*MAP_ITEM_SIZE)
            turnRight()
            turned = True
        else:
            robot.straight(othersize*MAP_ITEM_SIZE)
            robot.turn(201)
            robot.straight(size*MAP_ITEM_SIZE)
            turnRight()
            turned = True
    othersize = size    