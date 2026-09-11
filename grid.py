import random
from constants import *
import numpy as np

def create_maze():
    # Define movement directions: Right, Left, Down, Up
    DIRECTIONS = np.array([(1, 0), (-1, 0), (0, 1), (0, -1)])
     # Create a grid filled with obstacles
    grid = np.full((DIMENSION, DIMENSION), CELL_OBSTACLE, dtype=int)
    # Randomly select a starting point within the maze boundaries
    start_x, start_y = random.randint(1, DIMENSION - 2), random.randint(1, DIMENSION - 2)
    # Mark the starting point as an open cell
    grid[start_x, start_y] = CELL_OPEN

    while True:
        # Find all positions inside the maze that are currently obstacles
        rows, cols = np.where(grid[1:-1, 1:-1] == CELL_OBSTACLE)
        rows += 1
        cols += 1
# If there are no more obstacles to process, stop the loop
        if not rows.size:
            break

        candidates = []
        # Check each obstacle cell to see if it has exactly one open cell as a neighbor
        for i, j in zip(rows, cols):
            neighbors = grid[i + DIRECTIONS[:, 0], j + DIRECTIONS[:, 1]]
            if np.sum(neighbors == CELL_OPEN) == 1:
                candidates.append((i, j))
 # If no valid candidates remain, break the loop
        if not candidates:
            break
 # Randomly select one of the valid obstacle cells and open it up
        x, y = random.choice(candidates)
        grid[x, y] = CELL_OPEN
# Identify all open  cells within the maze
    rows, cols = np.where(grid[1:-1, 1:-1] == CELL_OPEN)
    rows += 1
    cols += 1

    dead_ends = []
# Identify dead-end cells (cells with only one open neighbor)
    for i, j in zip(rows, cols):
        neighbors = grid[i + DIRECTIONS[:, 0], j + DIRECTIONS[:, 1]]
        if np.sum(neighbors == CELL_OPEN) == 1:
            dead_ends.append((i, j))
# Randomly remove some dead ends
    if dead_ends:
        num_dead_ends_to_open = len(dead_ends) // 2  # Open about half of the dead ends
        dead_ends_to_open = random.sample(dead_ends, num_dead_ends_to_open)
        for x, y in dead_ends_to_open:
# Identify adjacent obstacle cells
            neighbors = grid[x + DIRECTIONS[:, 0], y + DIRECTIONS[:, 1]]
            closed_neighbors = np.where(neighbors == CELL_OBSTACLE)[0]
# If there are closed neighbors, open one of them to reduce dead-ends
            if closed_neighbors.size:
                dx, dy = DIRECTIONS[random.choice(closed_neighbors)]
                grid[x + dx, y + dy] = CELL_OPEN

    return grid
def generate_valid_start_goal(grid):
    while True:
        start = (random.randint(0, DIMENSION-1), random.randint(0, DIMENSION-1))
        goal = (random.randint(0, DIMENSION-1), random.randint(0, DIMENSION-1))
        # Making sure start and goal are open cells and not the same location
        if grid[start[0]][start[1]] == CELL_OPEN and grid[goal[0]][goal[1]] == CELL_OPEN and start != goal :
            return start, goal