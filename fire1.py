import random
import copy  
from grid import generate_valid_start_goal

from constants import *
# Places a fire in a random open cell.
def place_fire_randomly(grid):
    open_cells = [(i, j) for i in range(DIMENSION) for j in range(DIMENSION) if grid[i][j] == CELL_OPEN]
    if open_cells:
        i, j = random.choice(open_cells)
        grid[i][j] = CELL_FIRE # Fire is represented by 2
    return grid

# Simulates the fire spreading over time
def fire_spread(grid,q,goal):
    new_grid = copy.deepcopy(grid) 
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if grid[i][j] == CELL_OPEN and (i,j)!=goal :  # Fire spreads only to open spaces
                fire_neighbors = sum(grid[i + dx][j + dy] == 2 for dx, dy in DIRECTIONS if 0 <= i + dx < DIMENSION and 0 <= j + dy < DIMENSION)
                if fire_neighbors > 0:  # The more fire nearby, the higher the chance of spread
                    fire_probability = 1 - (1 - q) ** fire_neighbors
                    if random.random() < fire_probability:
                        new_grid[i][j] = CELL_FIRE   # Fire spreads here
    return new_grid


#Checks if a given cell is on fire or is adjacent to a fire.If 'neighbour_flag' is True, it considers fire-adjacent cells as unsafe, This helps the bot decide whether to avoid such areas.
def is_fire_affected(grid, cell, neighbour_flag=True):
    x, y = cell
    if grid[x][y] == CELL_FIRE:  # The cell itself is on fire
        return True
    if not neighbour_flag:
        return False
    for dx, dy in DIRECTIONS:  # Check its 4 neighbors
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == CELL_FIRE:
            return True  # If any neighbor has fire, consider it fire-affected
    return False  # Safe cell