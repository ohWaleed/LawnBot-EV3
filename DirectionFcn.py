AngleCheck=True


def GetDirectionByAngel (PreviousDirection, RotationAngle, PrevAngel):
    
    #define Global Angel check enabler 
    global AngleCheck

    # threshhold value 
    TURNCHANGE = 4

    # directions
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

    if AngleCheck:
        if PreviousDirection == UP:
            if RotationAngle - PrevAngel >= TURNCHANGE:
                AngleCheck = False
                return RIGHT
        elif PreviousDirection == DOWN:
            if RotationAngle - PrevAngel >= TURNCHANGE:
                AngleCheck = False
                return LEFT
            elif RotationAngle - PrevAngel <= TURNCHANGE * -1:
                AngleCheck = False
                return RIGHT    
        elif PreviousDirection == RIGHT:
            if RotationAngle - PrevAngel >= TURNCHANGE:
                AngleCheck = False
                return DOWN
            elif RotationAngle - PrevAngel <= TURNCHANGE * -1:
                AngleCheck = False
                return UP    
        elif PreviousDirection == LEFT:
            if RotationAngle - PrevAngel >= TURNCHANGE:
                AngleCheck = False
                return UP
            elif RotationAngle - PrevAngel <= TURNCHANGE * -1:
                AngleCheck = False
                return DOWN    
    else:
        if abs(RotationAngle-PrevAngel) <= 0:
            AngleCheck = True
        
    return PreviousDirection