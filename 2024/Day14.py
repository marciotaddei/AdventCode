import math
#for plotting
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

with open("input14.txt") as f:
    data = f.read().splitlines()
config = []
for line in data:
    p, v = line.split()
    p, v = p.strip("p=").split(","), v.strip("v=").split(",")
    config.append((int(p[0]), int(p[1]), int(v[0]), int(v[1])))

init_place = []
width, height = ((101, 103) if len(config) > 50 else (11,7))
grid = np.zeros((width, height), dtype=int)

t=0
for robot in config:
    init_place.append((robot[0], robot[1]))
placemt = init_place.copy()

width, height, cycle_length = 101, 103, 10403
init_place = [(robot[0], robot[1]) for robot in config]

fig, ax = plt.subplots()
grid = np.zeros((width, height), dtype=int)
for i in range(len(init_place)):
    placemt[i] = ( (init_place[i][0] + t*config[i][2])%width, (init_place[i][1] + t*config[i][3])%height)
    grid[placemt[i]] += 1
# ax.legend("t=0")
theshow = ax.matshow(grid.T, vmax=1)

def update_robots(t):
    placemt = init_place.copy()
    grid = np.zeros((width, height), dtype=int)
    for i in range(len(init_place)):
        placemt[i] = ( (init_place[i][0] + t*config[i][2])%width, (init_place[i][1] + t*config[i][3])%height)
        grid[placemt[i]] += 1
    theshow.set_data(grid.T)
    theshow.set_label(str(t))
    return theshow

ani = animation.FuncAnimation(fig=fig, func=update_robots, frames=10403, interval=5)
plt.show()