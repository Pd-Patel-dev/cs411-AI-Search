# informed.py
# Greedy Best First, A*, and SMA* (memory bounded A*)
# heuristic is straight line distance between two cities

import math
import heapq


def haversine(lat1, lon1, lat2, lon2):
    # distance in miles between 2 lat/lon points
    R = 3958.8
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def heuristic(city, goal, locations):
    # h(n) = straight line miles to the goal
    if locations is None:
        return 0
    if city not in locations or goal not in locations:
        return 0
    c1 = locations[city]
    c2 = locations[goal]
    d = haversine(c1["lat"], c1["lon"], c2["lat"], c2["lon"])
    return d


def path_cost(graph, path):
    if path is None or len(path) < 2:
        return 0
    total = 0
    for i in range(len(path) - 1):
        total = total + graph[path[i]][path[i + 1]]
    return round(total, 2)


def make_path(parent, start, goal):
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = parent.get(cur)
    path.reverse()
    if len(path) == 0 or path[0] != start:
        return None
    return path


class Node:
    # simple node object, I used this for A* and SMA*
    def __init__(self, name, parent, g, h):
        self.name = name
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def get_path(self):
        p = []
        n = self
        while n is not None:
            p.append(n.name)
            n = n.parent
        p.reverse()
        return p


def greedy(graph, start, goal, locations=None):
    # greedy only looks at h(n), it ignores how far we already traveled
    if start not in graph or goal not in graph:
        return None, 0, 0

    if start == goal:
        return [start], 0, 1

    # I just keep a list and sort it by heuristic each time
    # not the fastest but easier to understand
    frontier = [start]
    parent = {}
    parent[start] = None
    visited = []
    visited.append(start)
    expanded = 0

    while len(frontier) > 0:
        # pick the city that looks closest to the goal
        best_i = 0
        best_h = heuristic(frontier[0], goal, locations)
        i = 1
        while i < len(frontier):
            hval = heuristic(frontier[i], goal, locations)
            if hval < best_h:
                best_h = hval
                best_i = i
            i = i + 1

        current = frontier.pop(best_i)
        expanded = expanded + 1

        if current == goal:
            p = make_path(parent, start, goal)
            return p, path_cost(graph, p), expanded

        for n in graph[current]:
            if n not in visited:
                visited.append(n)
                parent[n] = current
                frontier.append(n)

    return None, 0, expanded


def astar(graph, start, goal, locations=None):
    # A* uses f(n) = g(n) + h(n)
    if start not in graph or goal not in graph:
        return None, 0, 0

    if start == goal:
        return [start], 0, 1

    start_h = heuristic(start, goal, locations)
    start_node = Node(start, None, 0, start_h)

    # heap of (f, counter, node) because if f is same heapq needs a tie breaker
    counter = 0
    frontier = []
    heapq.heappush(frontier, (start_node.f, counter, start_node))
    best_g = {}
    best_g[start] = 0
    expanded = 0
    done = []

    while len(frontier) > 0:
        fval, c, current = heapq.heappop(frontier)

        if current.name in done:
            continue

        expanded = expanded + 1
        done.append(current.name)

        if current.name == goal:
            p = current.get_path()
            return p, path_cost(graph, p), expanded

        for n in graph[current.name]:
            new_g = current.g + graph[current.name][n]
            if n not in best_g or new_g < best_g[n]:
                best_g[n] = new_g
                h = heuristic(n, goal, locations)
                child = Node(n, current, new_g, h)
                counter = counter + 1
                heapq.heappush(frontier, (child.f, counter, child))

    return None, 0, expanded


def sma_star(graph, start, goal, locations=None, memory_limit=15):
    # SMA* is A* but we only keep a limited number of nodes in memory
    # if we run out of space we drop the worst leaf (highest f)
    # I followed the idea from the lecture, not sure if every backup is perfect
    if start not in graph or goal not in graph:
        return None, 0, 0

    if start == goal:
        return [start], 0, 1

    if memory_limit is None or memory_limit < 2:
        memory_limit = 15

    start_h = heuristic(start, goal, locations)
    start_node = Node(start, None, 0, start_h)
    start_node.forgotten = []  # kids we had to drop

    frontier = [start_node]
    expanded = 0

    # stop if it runs too long
    steps = 0
    max_steps = 5000

    while len(frontier) > 0 and steps < max_steps:
        steps = steps + 1

        # pick the best f value
        best = frontier[0]
        bi = 0
        i = 1
        while i < len(frontier):
            if frontier[i].f < best.f:
                best = frontier[i]
                bi = i
            i = i + 1

        current = frontier.pop(bi)
        expanded = expanded + 1

        if current.name == goal:
            p = current.get_path()
            return p, path_cost(graph, p), expanded

        # expand neighbors
        kids = []
        for n in graph[current.name]:
            # dont go back to parent right away
            if current.parent is not None and n == current.parent.name:
                continue
            new_g = current.g + graph[current.name][n]
            h = heuristic(n, goal, locations)
            child = Node(n, current, new_g, h)
            child.forgotten = []
            # f should not be better than parent (pathmax)
            if child.f < current.f:
                child.f = current.f
            kids.append(child)

        if len(kids) == 0:
            # dead end, backup a big f so we dont pick this again
            current.f = 999999
            frontier.append(current)
            continue

        for child in kids:
            frontier.append(child)

        # if too many nodes, drop the worst one
        while len(frontier) > memory_limit:
            worst = frontier[0]
            wi = 0
            j = 0
            while j < len(frontier):
                # worst is highest f, if tie drop the deeper one
                deeper = 0
                t = frontier[j]
                depth_j = 0
                temp = t
                while temp is not None:
                    depth_j = depth_j + 1
                    temp = temp.parent
                depth_w = 0
                temp = worst
                while temp is not None:
                    depth_w = depth_w + 1
                    temp = temp.parent
                if t.f > worst.f or (t.f == worst.f and depth_j > depth_w):
                    worst = t
                    wi = j
                j = j + 1

            dropped = frontier.pop(wi)
            if dropped.parent is not None:
                # remember the f of the forgotten child
                if not hasattr(dropped.parent, "forgotten"):
                    dropped.parent.forgotten = []
                dropped.parent.forgotten.append(dropped.f)
                # parent f becomes the min of leftover kids / forgotten
                leftover = []
                for n2 in frontier:
                    if n2.parent is dropped.parent:
                        leftover.append(n2.f)
                leftover = leftover + dropped.parent.forgotten
                if len(leftover) > 0:
                    dropped.parent.f = min(leftover)

    # if we couldnt finish with the memory limit just fall back to A*
    return astar(graph, start, goal, locations)


# other names the website / tests might use
greedy_best_first = greedy
greedy_best_first_search = greedy
a_star = astar
astar_search = astar
sma = sma_star
memory_bounded = sma_star
memory_bounded_astar = sma_star
