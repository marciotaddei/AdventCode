import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
# import keyboard
# import msvcrt

user_in = input("Choose filename (empty for input15example.txt): ")
filename = user_in if user_in != "" else "input15example.txt"
with open(filename, "r") as file:
    maxrows=0
    while file.readline() != "\n":
        maxrows+=1
#     commands = file.readlines()
# commands = "".join(commands).replace("\n", "")

def numerize_map(amap):
    map_numer = np.zeros_like(amap, dtype=int)
    for pos in np.argwhere(amap=="@"):    map_numer[tuple(pos)] = -1
    for pos in np.argwhere(amap == "O"):  map_numer[tuple(pos)] = 2
    for pos in np.argwhere(amap == "["):  map_numer[tuple(pos)] = 2
    for pos in np.argwhere(amap == "]"):  map_numer[tuple(pos)] = 2
    for pos in np.argwhere(amap=="#"):    map_numer[tuple(pos)] = 3
    return map_numer

themap = np.genfromtxt(filename, dtype='str', delimiter=1, comments=None, max_rows=maxrows)
themap = numerize_map(themap)

fig, ax = plt.subplots(figsize=(8,8))
display = ax.matshow(themap)
ax.set_yticks([x-.5 for x in range(1,themap.shape[0])], ['']*(themap.shape[0]-1))
ax.set_xticks([x-.5 for x in range(1,themap.shape[1])], ['']*(themap.shape[1]-1))
ax.set_title("t=0")
ax.grid(axis="both", which="major")

def initialize():
    display.set_data(themap)
    return display

def step(t):
    ri, rj = np.argwhere(themap==-1)[0]
    ax.set_title(f"t={t}")
    # key = msvcrt.getch().decode()
    # key = keyboard.read_event(suppress=True)
    # char = key.name if key.event_type == keyboard.KEY_DOWN else ""
    try:
        char = input()[0]
    except IndexError: return display

    if char in ">d":
        ahead = themap[ri,rj:]
        if 0 not in ahead: return display
        dotloc = np.argwhere(ahead==0)[0][0]
        if dotloc > np.argwhere(ahead==3)[0]: return display
        themap[ri,rj+1:rj+1+dotloc] = themap[ri,rj:rj+dotloc]

    elif char in "vs":
        ahead = themap[ri:,rj]
        if 0 not in ahead: return display
        dotloc = np.argwhere(ahead==0)[0][0]
        if dotloc > np.argwhere(ahead==3)[0]: return display
        themap[ri+1:ri+1+dotloc,rj] = themap[ri:ri+dotloc,rj]

    elif char in "<a":
        ri, rj = np.argwhere(themap==-1)[0]
        ahead = themap[ri,:rj+1]
        if 0 not in ahead: return display
        dotloc = np.argwhere(ahead==0)[-1][0]
        if dotloc < np.argwhere(ahead==3)[-1]: return display
        themap[ri, dotloc:rj] = themap[ri, dotloc+1:rj+1]

    elif char in "^w":
        ri, rj = np.argwhere(themap==-1)[0]
        ahead = themap[:ri+1,rj]
        if 0 not in ahead: return display
        dotloc = np.argwhere(ahead==0)[-1][0]
        if dotloc < np.argwhere(ahead==3)[-1]: return display
        themap[dotloc:ri, rj] = themap[dotloc+1:ri+1, rj]

    else: return display

    themap[ri,rj] = 0

    display.set_data(themap)
    return display


ani = animation.FuncAnimation(fig=fig, func=step, init_func=initialize,
                              frames=1024, interval=1, repeat=True)
plt.show()