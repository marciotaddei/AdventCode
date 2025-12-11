import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

user_in = input("Choose filename (empty for input15example.txt): ")
filename = user_in if user_in != "" else "input15example.txt"
with open(filename, "r") as file:
    maxrows=0
    while file.readline() != "\n":
        maxrows+=1
    commands = file.readlines()
commands = "".join(commands).replace("\n", "")

themap = np.genfromtxt(filename, dtype='str', delimiter=1, comments=None, max_rows=maxrows)
bigmap = np.zeros((themap.shape[0], themap.shape[1]*2), dtype=str)
for i in range(themap.shape[1]):
    bigmap[:, 2*i] = themap[:, i]
    bigmap[:, 2*i+1] = themap[:, i]
bigmap[tuple(np.argwhere(bigmap=="@")[1])] = "."
for pos in np.argwhere(bigmap=="O")[::2]:
    bigmap[tuple(pos)]="["
    bigmap[tuple(pos+[0,1])]="]"

def numerize_map(amap):
    map_numer = np.zeros_like(amap, dtype=int)
    for pos in np.argwhere(amap=="@"):    map_numer[tuple(pos)] = -1
    for pos in np.argwhere(amap == "O"):  map_numer[tuple(pos)] = 1
    for pos in np.argwhere(amap == "["):  map_numer[tuple(pos)] = 2
    for pos in np.argwhere(amap == "]"):  map_numer[tuple(pos)] = 2
    for pos in np.argwhere(amap=="#"):    map_numer[tuple(pos)] = 3
    return map_numer


fig, ax = plt.subplots(figsize=(10,5))    
map_numer = numerize_map(bigmap)
display = ax.matshow(map_numer)
ax.set_yticks([x-.5 for x in range(1,map_numer.shape[0])], '')
ax.set_xticks([x-.51 for x in range(1,map_numer.shape[1])], '')
ax.set_title("t=0")
ax.grid(axis="both", which="major")

def initialize():
    display.set_data(map_numer)
    return display

def step(t):
    ri, rj = np.argwhere(bigmap=="@")[0]
    ax.set_title(f"t={t}")
    char = commands[t]

    #horizontal: no change
    if   char == ">":
        ahead = bigmap[ri,rj:]
        if "." not in ahead: return display
        dotloc = np.argwhere(ahead==".")[0][0]
        if dotloc > np.argwhere(ahead=="#")[0]: return display
        bigmap[ri,rj+1:rj+1+dotloc] = bigmap[ri,rj:rj+dotloc]
        bigmap[ri,rj] = "."
        
    elif char == "<":
        ri, rj = np.argwhere(bigmap=="@")[0]
        ahead = bigmap[ri,:rj+1]
        if "." not in ahead: return display
        dotloc = np.argwhere(ahead==".")[-1][0]
        if dotloc < np.argwhere(ahead=="#")[-1]: return display
        bigmap[ri, dotloc:rj] = bigmap[ri, dotloc+1:rj+1]
        bigmap[ri,rj] = "."
         
    #vertical: many changes needed
    elif char == "v":
        if bigmap[ri+1,rj]=="#": return display
        if bigmap[ri+1,rj]==".":
            bigmap[ri+1,rj]="@"
            bigmap[ri,rj] = "."
            return display
        
        if   bigmap[ri+1,rj] == "[":    moved_boxes_l = {(ri+1,rj  )};  to_check = {(ri+1,rj), (ri+1,rj+1)}
        elif bigmap[ri+1,rj] == "]":    moved_boxes_l = {(ri+1,rj-1)};  to_check = {(ri+1,rj-1), (ri+1,rj)}
        #moved_boxes_l: left half of boxes to move
        #to_check:      boxes below those to move, to check for collisions
        while to_check:
            box_0, box_1 = to_check.pop()
            if bigmap[box_0, box_1] == "#": break
            if bigmap[box_0, box_1] == "[":
                moved_boxes_l.update({(box_0,  box_1)}) 
                to_check.     update({(box_0+1,box_1), (box_0+1,box_1+1)})
            elif bigmap[box_0, box_1] == "]":
                moved_boxes_l.update({(box_0,  box_1-1)})
                to_check.     update({(box_0+1,box_1-1), (box_0+1,box_1)})
        else: #make the move
            for (pos0, pos1) in moved_boxes_l: bigmap[pos0,  pos1] = "."; bigmap[pos0  ,pos1+1] = "." 
            for (pos0, pos1) in moved_boxes_l: bigmap[pos0+1,pos1] = "["; bigmap[pos0+1,pos1+1] = "]"
            bigmap[ri+1,rj]="@"
            bigmap[ri,rj] = "."

    elif char == "^":
        if bigmap[ri-1,rj]=="#": return display
        if bigmap[ri-1,rj]==".":
            bigmap[ri-1,rj]="@"
            bigmap[ri,rj] = "."
            return display
        
        if   bigmap[ri-1,rj] == "[":    moved_boxes_l = {(ri-1,rj  )};  to_check = {(ri-1,rj), (ri-1,rj+1)}
        elif bigmap[ri-1,rj] == "]":    moved_boxes_l = {(ri-1,rj-1)};  to_check = {(ri-1,rj-1), (ri-1,rj)}
        
        while to_check:
            box_0, box_1 = to_check.pop()
            if bigmap[box_0, box_1] == "#": break
            if bigmap[box_0, box_1] == "[":
                moved_boxes_l.update({(box_0,  box_1)})
                to_check.     update({(box_0-1,box_1)  ,(box_0-1,box_1+1)})
            elif bigmap[box_0, box_1] == "]":
                moved_boxes_l.update({(box_0,  box_1-1)})
                to_check.     update({(box_0-1,box_1-1) ,(box_0-1,box_1  )})
        else: #make the move
            for (pos0, pos1) in moved_boxes_l: bigmap[pos0  ,pos1] = "."; bigmap[pos0  ,pos1+1] = "."
            for (pos0, pos1) in moved_boxes_l: bigmap[pos0-1,pos1] = "["; bigmap[pos0-1,pos1+1] = "]"
            bigmap[ri-1,rj]="@"
            bigmap[ri,rj] = "."

    display.set_data(numerize_map(bigmap))
    return display


ani = animation.FuncAnimation(fig=fig, func=step, init_func=initialize, 
                              frames=len(commands), interval=5, repeat=False) 
plt.show()