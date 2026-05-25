# Terrain Path Optimization Game

A single-player Python + Pygame grid game where the player manually builds a path across random terrain and compares the result with Dijkstra's optimal path.

## Folder Structure

```text
terrain-path-optimization-game/
|--src
|   |-- main.py
|   |-- ui.py
|   |-- player.py
|   |-- terrain.py
|   |-- dijkstra.py
|   |-- scoring.py
|   `-- settings.py
|-- requirements.txt
`-- README.md
```

## How To Run

Use Python 3.10, 3.11, or 3.12 for easiest Pygame installation.

```bash
pip install -r requirements.txt
python main.py
```

On the current testing machine, Python 3.12 is available, so this command works:

```bash
py -3.12 main.py
```

## Gameplay

1. Choose a habitat: Forest, Desert, or Snow.
2. Choose a grid size: 5x5, 10x10, or 15x15.
3. Click adjacent non-water tiles to build a route from the green start tile to the red end tile.
4. Click Submit Path after reaching the end.
5. The result screen keeps your yellow path visible and reveals Dijkstra's purple/cyan optimal path.
6. You win only when your cost exactly matches the optimal cost.

## Terrain Costs

```text
grass    = 1
forest   = 3
sand     = 4
snow     = 5
mountain = 7
water    = blocked
```

## Verification

The project was checked with:

```bash
python -m py_compile main.py ui.py player.py terrain.py dijkstra.py scoring.py settings.py
```
