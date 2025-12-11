# %%
from collections import deque
import time

t0 = time.perf_counter_ns()

DIRS = (1,0), (0, 1), (-1,0), (0,-1)

def graph_maker(grid, start, end):
    #from start to 1st bifurcation
    neighbors = {tuple(map(sum, zip(start, (1, 0))))} #at start, single neighbor always down
    current = start
    edge_weight = 0
    while len(neighbors) == 1:
        edge_weight +=1
        previous = current
        current = neighbors.pop() #single neighbor
        neighbors = {tuple(map(sum, zip(current, delta))) for delta in DIRS}
        neighbors.remove(previous)
        neighbors = {(y, x) for (y, x) in neighbors if grid[y][x] != "#"}
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
        neighbors = {tuple(map(sum,zip(current,delta))) for delta in DIRS}
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

def path_to_fin_leaf(node, history):
    nodes_to_check = [set(graph[node].keys()) - history]
    path, nodes_visited = [node], {node}

    while nodes_to_check and (fin_leaf not in path):
        if not nodes_to_check[-1]:
            del nodes_to_check[-1]
            del path[-1]
            continue
        
        curr_node = nodes_to_check[-1].pop()

        if curr_node == fin_leaf:
            path.append(curr_node)
            return set(path)

        nodes_visited.add(curr_node)

        new_nodes = set(graph[curr_node].keys()) - (history | nodes_visited)
        if new_nodes:
            nodes_to_check.append(new_nodes)
            path.append(curr_node)      

    return None

def list_traversal(root,graph, init_dist=0):
    all_paths = [(root, init_dist, set())] #deque actually a bit slower
    best = 0

    while all_paths:    
        node, dist, history = all_paths.pop()
        history = history | {node}

        for adj, delta in graph[node].items():            
            if adj in history:
                continue

            if adj == fin_leaf:
                best = max(dist+delta, best)
                continue
            
            if paths[adj] & history:
                new_path = path_to_fin_leaf(adj, history)
                if new_path is None:
                    continue
                paths[adj] = new_path
            
            all_paths.append((adj, dist+delta, history))
    return best

print(f"Functions loaded: {(time.perf_counter_ns() - t0) / 1_000_000_000:.1f} s")

with open("input23.txt", "r") as f:
    grid = f.read().split("\n")
print(f"Grid read:        {(time.perf_counter_ns() - t0) / 1_000_000_000:.1f} s")

start, end = (0,1), (len(grid)-1,len(grid[0])-2) #valid for example and actual input
graph, root, pre_root_dist, fin_leaf, post_gr_fin_dist = graph_maker(grid, start, end)
print(f"Graph created:    {(time.perf_counter_ns() - t0) / 1_000_000_000:.1f} s")

paths = {node: path_to_fin_leaf(node, set()) for node in graph.keys()}
best = list_traversal(root, graph, init_dist=pre_root_dist+post_gr_fin_dist)
print(f"Find longest:     {(time.perf_counter_ns() - t0) / 1_000_000_000:.1f} s")

print(f"Total runtime:    {(time.perf_counter_ns() - t0) / 1_000_000_000:.1f} s")
print(f"Max length:       {best}")
