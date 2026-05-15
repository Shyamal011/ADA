import heapq
import grid

DIRECTIONS=[(0, 1),(1, 0),(-1, 0),(0, -1)]

def dijkstra(grid, start, end, terrain_cost):
    rows=len(grid)
    cols=len(grid[0])
    distances={}
    for r in range(rows):
        for c in range(cols):
            distances[(r,c)]=float("inf")

    distances[start]=0
    pq=[]
    heapq.heappush(pq,(0,start))
    previous={}

    while pq:
        current_cost,current=heapq.heappop(pq)
        if current==end:
            break
        r, c = current
        for dr,dc in DIRECTIONS:
            nr=r+dr
            nc=c+dc
            if 0<=nr<rows and 0<=nc<cols:
                terrain=grid[nr][nc]
                if terrain=="water":
                    continue
                new_cost=current_cost+terrain_cost[terrain]
                if new_cost<distances[(nr,nc)]:

                    distances[(nr,nc)]=new_cost

                    previous[(nr,nc)]=current

                    heapq.heappush(pq,(new_cost,(nr, nc)))
    path=[]
    current=end

    while current!=start:
        path.append(current)
        current=previous[current]

    path.append(start)
    path.reverse()

    return path,distances[end]