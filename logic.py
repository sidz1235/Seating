import pandas as pds

branch_codes = {"733":"CSE", "737":"IT", "735":"ECE", "734":"EEE", "748":"AIML", "732":"CIVIL", "736":"MECH"}
room_capacity = {"normal":30 , "hall": 66} #5x6, 11x6

def ranges(i):
    i = sorted(set(i))
    for key, group in itertools.groupby(enumerate(i), lambda t: t[1]-t[0]):
        group = list(group)
        yield group[0][1], group[-1][1]

def transpose(l1, l2):
 
    for i in range(len(l1[0])):
        row =[]
        for item in l1:
            row.append(item[i])
        l2.append(row)
    return l2




def generate(file, selected_blocks, selected_halls, selected_rooms, branch, exam_type, capacities):
    xl = pds.ExcelFile(file)
    res = len(xl.sheet_names)
    sheets = []
    counters = []
    for i in range(res):
        sheet = pds.read_excel(file, sheet_name = i)
        rolls = [sheet._get_value(i, "Roll") for i in range(len(sheet.index))]
        sheets.append(rolls)
        counters.append([0, len(rolls)])
    

    rooms = []

    cur_left  = -1
    cur_right = -1

    sheets = []
    counters = []
    
    for i in branch:
        sheet = pds.read_excel(file, sheet_name = i)
        rolls = [sheet._get_value(i, "Roll") for i in range(len(sheet.index))]
        sheets.append(rolls)
        counters.append([0, len(rolls)])

    if(len(sheets) == 1):
        cur_left = 0
    else:
        cur_left = 0
        cur_right = 1

    for i in range(len(selected_rooms)):
        m = 5
        n = 6
        benches = [[["-1", "-1"] for x in range(n)] for y in range(m)]
        if(len(sheets) == 1):
            for x in range(m):
                for y in range(n):
                    if(counters[cur_left][0] >= counters[cur_left][1]):
                        break
                    benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                    counters[cur_left][0] += 1
        else:
            for x in range(m):
                for y in range(n):
                    if(cur_left<len(counters)):
                        if(counters[cur_left][0] >= counters[cur_left][1]):
                            if(cur_left>cur_right):
                                cur_left += 1
                            else:
                                cur_left += 1
                                if(cur_left == cur_right):
                                    cur_left += 1
                                
                    if(cur_right<len(counters)):
                        if(counters[cur_right][0] >= counters[cur_right][1]):
                            if(cur_right>cur_left):
                                cur_right += 1
                            else:
                                cur_right += 1
                                if(cur_right == cur_left):
                                    cur_right += 1
                        
                                
                    if(cur_left<len(counters)):
                        if(counters[cur_left][0] < counters[cur_left][1]):
                            benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                            counters[cur_left][0] += 1
                    if(y%2 == 0):
                        if(cur_right<len(counters)):
                            if(counters[cur_right][0] < counters[cur_right][1]):
                                benches[x][y][1] = sheets[cur_right][counters[cur_right][0]]
                                counters[cur_right][0] += 1
                        
        rooms.append(benches)

    for i in range(len(selected_halls)):
        m = 6
        n = 11
        benches = [[["-1"] for x in range(n)] for y in range(m)]
        if(len(sheets) == 1):
            for x in range(m):
                for y in range(n):
                    if(counters[cur_left][0] >= counters[cur_left][1]):
                        break
                    benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                    counters[cur_left][0] += 1
        else:
            for x in range(m):
                for y in range(n):
                    if(cur_left<len(counters)):
                        if(counters[cur_left][0] >= counters[cur_left][1]):
                            if(cur_left>cur_right):
                                cur_left += 1
                            else:
                                cur_left += 1
                                if(cur_left == cur_right):
                                    cur_left += 1
                                
                    if(cur_right<len(counters)):
                        if(counters[cur_right][0] >= counters[cur_right][1]):
                            if(cur_right>cur_left):
                                cur_right += 1
                            else:
                                cur_right += 1
                                if(cur_right == cur_left):
                                    cur_right += 1
                                
                    if(cur_left<len(counters)):
                        if(counters[cur_left][0] < counters[cur_left][1]):
                            benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                            counters[cur_left][0] += 1
                    if(cur_right<len(counters)):
                        if(counters[cur_right][0] < counters[cur_right][1]):
                            benches[x][y][0] = sheets[cur_right][counters[cur_right][0]]
                            counters[cur_right][0] += 1
        rooms.append(benches)
    

    for i in range(len(rooms)):
        for j in range(len(rooms[i])):
            if(j%2==1): 
                rooms[i][j].reverse() 
    for i in range(len(rooms)):
        room = transpose(rooms[i], [])
        rooms[i] = room
    
    result = {}
    i = 0
    while(i < len(selected_rooms)):
        result[selected_rooms[i]] = rooms[i]
        i += 1
    i = 0
    while(i < len(selected_halls)):
        result[selected_halls[i]] = rooms[i+len(selected_rooms)]
        i += 1


    
    return result


"""
Capacity = 60
for i in range(len(selected_rooms)):
        m = 5
        n = 6
        benches = [[["-1", "-1"] for x in range(n)] for y in range(m)]
        if(len(sheets) == 1):
            for x in range(m):
                for y in range(n):
                    if(counters[cur_left][0] >= counters[cur_left][1]):
                        break
                    benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                    counters[cur_left][0] += 1
        else:
            for x in range(m):
                for y in range(n):
                    if(cur_left<len(counters)):
                        if(counters[cur_left][0] >= counters[cur_left][1]):
                            if(cur_left>cur_right):
                                cur_left += 1
                            else:
                                cur_left += 1
                                if(cur_left == cur_right):
                                    cur_left += 1
                                
                    if(cur_right<len(counters)):
                        if(counters[cur_right][0] >= counters[cur_right][1]):
                            if(cur_right>cur_left):
                                cur_right += 1
                            else:
                                cur_right += 1
                                if(cur_right == cur_left):
                                    cur_right += 1
                        
                                
                    if(cur_left<len(counters)):
                        if(counters[cur_left][0] < counters[cur_left][1]):
                            benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                            counters[cur_left][0] += 1
                    if(cur_right<len(counters)):
                        if(counters[cur_right][0] < counters[cur_right][1]):
                            benches[x][y][1] = sheets[cur_right][counters[cur_right][0]]
                            counters[cur_right][0] += 1
        rooms.append(benches)
"""

"""
Capacity = 45
for i in range(len(selected_rooms)):
        m = 5
        n = 6
        benches = [[["-1", "-1"] for x in range(n)] for y in range(m)]
        if(len(sheets) == 1):
            for x in range(m):
                for y in range(n):
                    if(counters[cur_left][0] >= counters[cur_left][1]):
                        break
                    benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                    counters[cur_left][0] += 1
        else:
            for x in range(m):
                for y in range(n):
                    if(cur_left<len(counters)):
                        if(counters[cur_left][0] >= counters[cur_left][1]):
                            if(cur_left>cur_right):
                                cur_left += 1
                            else:
                                cur_left += 1
                                if(cur_left == cur_right):
                                    cur_left += 1
                                
                    if(cur_right<len(counters)):
                        if(counters[cur_right][0] >= counters[cur_right][1]):
                            if(cur_right>cur_left):
                                cur_right += 1
                            else:
                                cur_right += 1
                                if(cur_right == cur_left):
                                    cur_right += 1
                        
                                
                    if(cur_left<len(counters)):
                        if(counters[cur_left][0] < counters[cur_left][1]):
                            benches[x][y][0] = sheets[cur_left][counters[cur_left][0]]
                            counters[cur_left][0] += 1
                    if(y%2 == 0):
                        if(cur_right<len(counters)):
                            if(counters[cur_right][0] < counters[cur_right][1]):
                                benches[x][y][1] = sheets[cur_right][counters[cur_right][0]]
                                counters[cur_right][0] += 1
                        
        rooms.append(benches)
"""
