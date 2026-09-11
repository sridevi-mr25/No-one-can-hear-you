import random
import time

from fire1 import place_fire_randomly, fire_spread
from plot import plot_grid
from grid import create_maze, generate_valid_start_goal
from algorithm import astar
from constants import *

def simulate_bot_spread(start,goal, grid, q):
    traversed_path = [start] 
    bot_position = start
    
    while bot_position != goal:
        # Find the path using A* algorithm on the updated grid
        bot_position = astar(grid, bot_position, goal)
        # print(bot_position)
        if not bot_position:
            print("No path found. The bot is trapped.")
            break
        
        traversed_path.append(bot_position)
        print(f"Bot moved to {bot_position}")
        if grid[bot_position[0]][bot_position[1]] == CELL_FIRE:
            print("Bot burned by fire! Failed.")
            break
        
        # Simulate fire spread using the original probability logic
        grid = fire_spread(grid,q,goal)  # Update grid with new fire spread

        # Plot each step
        plot_grid(grid, start, goal, bot_position,traversed_path[:])
        time.sleep(0.5)  # Pause for better visualization

if __name__ == "__main__":
    # Initialize the grid and fire placement
    grid = create_maze()
    count_freq = {}
    
    grid = place_fire_randomly(grid)
    q = random.random() # Flammability of the ship

    # Generate valid start and goal positions
    start, goal = generate_valid_start_goal(grid)
    print(f"Start: {start}, Goal: {goal}")
    
    simulate_bot_spread(start,goal, grid, q)
    
    