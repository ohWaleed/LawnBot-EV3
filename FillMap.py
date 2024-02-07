def FillMap (map):
    map_row = len(map)
    map_col = len(map[0])
    StartIndex = 0
    
    #check and fill the first row if not completed correctly while edge detection
    if map[1][1] != 1:
        map[1] = map[2]
        StartIndex = 2
    if map[0][1] != 1:
        map[0] = map[1]
        if StartIndex != 2:
            StartIndex = 1
    
    for col in range(map_col):
        for row in range(StartIndex,map_row):
            if map[row][col] == 1:
                if map[row+1][col] == 0:
                    map[row+1][col] = 1
                else:
                    break