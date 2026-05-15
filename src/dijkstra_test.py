from dijkstra import dijkstra
from scoring import *

grid = [
    ["grass", "grass", "forest"],
    ["water", "mountain", "grass"],
    ["grass", "grass", "grass"]
]

terrain_cost = {
    "grass": 1,
    "forest": 3,
    "mountain": 7,
    "water": float("inf")
}

start = (0, 0)
end = (2, 2)

path, cost = dijkstra(
    grid,
    start,
    end,
    terrain_cost
)

print("Best Path:", path)
print("Optimal Cost:", cost)