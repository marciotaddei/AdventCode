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

fig, ax = plt.subplots(figsize=(8,8))
map_numer = np.zeros_like(themap, dtype=int)
for pos in np.argwhere(themap=="@"):    map_numer[tuple(pos)] = -1
for pos in np.argwhere(themap=="O"):    map_numer[tuple(pos)] = 1
for pos in np.argwhere(themap=="#"):    map_numer[tuple(pos)] = 2

display = ax.matshow(map_numer)
ax.set_yticks([x-.5 for x in range(1,themap.shape[0])], ['']*(themap.shape[0]-1))
ax.set_xticks([x-.51 for x in range(1,themap.shape[1])], ['']*(themap.shape[1]-1))
ax.set_title("t=0")
ax.grid(axis="both", which="major")

def initialize():
    display.set_data(map_numer)
    return display

def step(t):
    ri, rj = np.argwhere(themap=="@")[0]
    ax.set_title(f"t={t}")
    char = commands[t]

    if char == ">":
        ahead = themap[ri,rj:]
        if "." not in ahead: return display
        dotloc = np.argwhere(ahead==".")[0][0]
        if dotloc > np.argwhere(ahead=="#")[0]: return display
        themap[ri,rj+1:rj+1+dotloc] = themap[ri,rj:rj+dotloc]

    elif char =="v":
        ahead = themap[ri:,rj]
        if "." not in ahead: return display
        dotloc = np.argwhere(ahead==".")[0][0]
        if dotloc > np.argwhere(ahead=="#")[0]: return display
        themap[ri+1:ri+1+dotloc,rj] = themap[ri:ri+dotloc,rj]

    elif char =="<":
        ri, rj = np.argwhere(themap=="@")[0]
        ahead = themap[ri,:rj+1]
        if "." not in ahead: return display
        dotloc = np.argwhere(ahead==".")[-1][0]
        if dotloc < np.argwhere(ahead=="#")[-1]: return display
        themap[ri, dotloc:rj] = themap[ri, dotloc+1:rj+1]

    elif char == "^":
        ri, rj = np.argwhere(themap=="@")[0]
        ahead = themap[:ri+1,rj]
        if "." not in ahead: return display
        dotloc = np.argwhere(ahead==".")[-1][0]
        if dotloc < np.argwhere(ahead=="#")[-1]: return display
        themap[dotloc:ri, rj] = themap[dotloc+1:ri+1, rj]

    themap[ri,rj] = "."

    map_numer = np.zeros_like(themap, dtype=int)
    for pos in np.argwhere(themap=="@"):    map_numer[tuple(pos)] = -1
    for pos in np.argwhere(themap=="O"):    map_numer[tuple(pos)] = 1
    for pos in np.argwhere(themap=="#"):    map_numer[tuple(pos)] = 2
    display.set_data(map_numer)
    return display


ani = animation.FuncAnimation(fig=fig, func=step, init_func=initialize,
                               frames=len(commands), interval=5 if len(commands)<1000 else 1, repeat=False)
plt.show()