import heapq

from settings import TERRAIN_COSTS

DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


def compute_dijkstra(grid, start, end, terrain_costs=TERRAIN_COSTS):
    rows = len(grid)
    cols = len(grid[0])
    distances = {}
    for r in range(rows):
        for c in range(cols):
            distances[(r, c)] = float("inf")

    distances[start] = 0
    pq = []
    heapq.heappush(pq, (0, start))
    previous = {}

    while pq:
        current_cost, current = heapq.heappop(pq)
        if current_cost > distances[current]:
            continue
        if current == end:
            break
        r, c = current
        for dr, dc in DIRECTIONS:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                terrain = grid[nr][nc]
                terrain_cost = terrain_costs[terrain]
                if terrain_cost is None:
                    continue
                new_cost = current_cost + terrain_cost
                if new_cost < distances[(nr, nc)]:
                    distances[(nr, nc)] = new_cost
                    previous[(nr, nc)] = current
                    heapq.heappush(pq, (new_cost, (nr, nc)))

    if distances[end] == float("inf"):
        return [], float("inf")

    path = []
    current = end

    while current != start:
        path.append(current)
        current = previous[current]

    path.append(start)
    path.reverse()

    return path, distances[end]


def dijkstra(grid, start, end, terrain_cost):
    return compute_dijkstra(grid, start, end, terrain_cost)
