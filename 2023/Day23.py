#making it a .py doesn't really speed it up

from collections import deque

def graph_maker(grid, start, end): #assumes final point only one in its row
    #from start to 1st bifurcation
    neighbors = {tuple(map(sum,zip(start,(1,0))))} #at start, single neighbor always down
    current = start
    edge_weight = 0
    while len(neighbors)==1:
        edge_weight +=1
        previous = current
        current = neighbors.pop() #single neighbor
        neighbors = {tuple(map(sum,zip(current,delta))) for delta in {(0,1), (1,0), (0,-1), (-1,0)}}
        neighbors.remove(previous)
        neighbors = {n for n in neighbors if grid[n[0]][n[1]]!="#"}
    root = current
    queue = deque({root})  #begin queue with first bifurcation
    visited = {previous} #set of visited points neighbors to bifurcations
    pre_root_dist = edge_weight #start point not in graph, distance added to every path anyway

    #from end to finish point, find fin_leaf
    neighbors = {tuple(map(sum,zip(end,(-1,0))))} #at the end, single neighbor always up
    current = end
    edge_weight = 0
    while len(neighbors)==1:
        edge_weight +=1
        previous = current
        current = neighbors.pop() #single neighbor
        neighbors = {tuple(map(sum,zip(current,delta))) for delta in {(0,1), (1,0), (0,-1), (-1,0)}}
        neighbors.remove(previous)
        neighbors = {n for n in neighbors if grid[n[0]][n[1]]!="#"}
    fin_leaf = current
    visited.add(previous) #set of visited points neighbors to bifurcations
    post_gr_fin_dist = edge_weight

    #main cycle
    graph = {root: {}}
    while queue!=deque([]):
        node = queue.pop()

        edge_weight = 0
        current = node
        
        followings = {tuple(map(sum,zip(current,delta))) for delta in {(0,1), (1,0), (0,-1), (-1,0)}}
        followings = followings - visited
        followings = {f for f in followings if grid[f[0]][f[1]]!="#"}

        for current in followings: #1, 2, or 3 paths to go, depending on junction kind
            neighbors = {tuple(map(sum,zip(current,delta))) for delta in {(0,1), (1,0), (0,-1), (-1,0)}}
            neighbors.remove(node)
            neighbors = {n for n in neighbors if grid[n[0]][n[1]]!="#"}

            edge_weight = 1
            while len(neighbors)==1:
                edge_weight +=1
                previous = current
                current = neighbors.pop() #single neighbor
                neighbors = {tuple(map(sum,zip(current,delta))) for delta in {(0,1), (1,0), (0,-1), (-1,0)}}
                neighbors.remove(previous)
                neighbors = {n for n in neighbors if grid[n[0]][n[1]]!="#"}
            graph[node].update({current: edge_weight})
            if current not in graph:
                graph.update({current: {node: edge_weight}})
            else:
                graph[current].update({node: edge_weight})
            visited.add(previous)
            if current != fin_leaf:
                queue.appendleft(current) #add point to queue, except final one

    return graph, root, pre_root_dist, fin_leaf, post_gr_fin_dist

best = 0
def traversal(node, pathset, dist):#, graph, fin_leaf):
    global best
    if node == fin_leaf:
        best = max(best, dist)
    for nb in set(graph[node].keys()):
        if nb not in pathset:
            pathset.add(nb)
            traversal(nb, pathset, dist+graph[node][nb])#, graph, fin_leaf)
            pathset.remove(nb)

with open("input23.txt", "r") as f:
    grid = f.read().split("\n")

start, end = (0,1), (len(grid)-1,len(grid[0])-2) #valid for example and actual input
graph, root, pre_root_dist, fin_leaf, post_gr_fin_dist = graph_maker(grid, start, end)
traversal(root, {root}, pre_root_dist + post_gr_fin_dist)#, 0)#, graph, fin_leaf)
print(best)