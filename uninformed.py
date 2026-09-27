# uninformed.py
# BFS, DFS, UCS, and IDS
# I used a parent dictionary to rebuild the path at the end

import heapq


def path_cost(graph, path):
    # add up the road distances along the path
    if path is None or len(path) < 2:
        return 0
    total = 0
    i = 0
    while i < len(path) - 1:
        a = path[i]
        b = path[i + 1]
        total = total + graph[a][b]
        i = i + 1
    return round(total, 2)


def make_path(parent, start, goal):
    # walk backwards from goal using parent pointers
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = parent.get(cur)
        if cur is None and path[-1] != start:
            return None
    path.reverse()
    if path[0] != start:
        return None
    return path


def bfs(graph, start, goal):
    # BFS uses a queue (FIFO) so it expands the closest cities first (by hops)
    if start not in graph or goal not in graph:
        return None, 0, 0

    if start == goal:
        return [start], 0, 1

    queue = []
    queue.append(start)
    visited = []
    visited.append(start)
    parent = {}
    parent[start] = None
    expanded = 0

    while len(queue) > 0:
        current = queue.pop(0)  # take from front of list
        expanded = expanded + 1

        if current == goal:
            p = make_path(parent, start, goal)
            return p, path_cost(graph, p), expanded

        # graph[current] is a dict of neighbor -> distance
        neighbors = list(graph[current].keys())
        for n in neighbors:
            if n not in visited:
                visited.append(n)
                parent[n] = current
                queue.append(n)

    return None, 0, expanded


def dfs(graph, start, goal):
    # DFS uses a stack (LIFO), goes deep first then backtracks
    if start not in graph or goal not in graph:
        return None, 0, 0

    if start == goal:
        return [start], 0, 1

    stack = []
    stack.append(start)
    visited = []
    visited.append(start)
    parent = {}
    parent[start] = None
    expanded = 0

    while len(stack) > 0:
        current = stack.pop()  # take from the end
        expanded = expanded + 1

        if current == goal:
            p = make_path(parent, start, goal)
            return p, path_cost(graph, p), expanded

        neighbors = list(graph[current].keys())
        # I reverse so the first neighbor gets popped first (more like class notes)
        neighbors.reverse()
        for n in neighbors:
            if n not in visited:
                visited.append(n)
                parent[n] = current
                stack.append(n)

    return None, 0, expanded


def ucs(graph, start, goal):
    # UCS always expands the cheapest path so far (g(n))
    if start not in graph or goal not in graph:
        return None, 0, 0

    if start == goal:
        return [start], 0, 1

    # heap items: (cost so far, city)
    frontier = []
    heapq.heappush(frontier, (0, start))
    parent = {}
    parent[start] = None
    best_cost = {}
    best_cost[start] = 0
    expanded = 0
    done = []

    while len(frontier) > 0:
        cost, current = heapq.heappop(frontier)

        if current in done:
            continue

        expanded = expanded + 1
        done.append(current)

        if current == goal:
            p = make_path(parent, start, goal)
            return p, path_cost(graph, p), expanded

        neighbors = graph[current]
        for n in neighbors:
            new_cost = cost + neighbors[n]
            # only keep this path if its cheaper
            if n not in best_cost or new_cost < best_cost[n]:
                best_cost[n] = new_cost
                parent[n] = current
                heapq.heappush(frontier, (new_cost, n))

    return None, 0, expanded


def dls(graph, start, goal, limit):
    # depth limited search used by IDS
    # I keep the path list so I dont go in circles
    expanded = [0]  # list so the recursive function can update it

    def rec(current, remaining, path):
        expanded[0] = expanded[0] + 1
        if current == goal:
            return path
        if remaining == 0:
            return None
        for n in graph[current]:
            if n not in path:
                ans = rec(n, remaining - 1, path + [n])
                if ans is not None:
                    return ans
        return None

    result = rec(start, limit, [start])
    return result, expanded[0]


def ids(graph, start, goal):
    # IDS keeps increasing the depth limit until it finds the goal
    # this way it has BFS like shortest hop path but uses less memory
    if start not in graph or goal not in graph:
        return None, 0, 0

    if start == goal:
        return [start], 0, 1

    total_expanded = 0
    # max depth is number of cities, should be enough if the graph is connected
    max_d = len(graph) + 1
    d = 0
    while d <= max_d:
        p, exp = dls(graph, start, goal, d)
        total_expanded = total_expanded + exp
        if p is not None:
            return p, path_cost(graph, p), total_expanded
        d = d + 1

    return None, 0, total_expanded


# extra names just in case something calls them differently
breadth_first_search = bfs
depth_first_search = dfs
uniform_cost_search = ucs
iterative_deepening_search = ids
iddfs = ids
