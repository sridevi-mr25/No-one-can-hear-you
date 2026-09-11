import random
import time

from fire1 import place_fire_randomly, fire_spread
from plot import plot_grid
from grid import create_maze, generate_valid_start_goal
from algorithm import astar
from constants import *

def simulate_bot_spread(start,goal, grid, q):
    # Try to find a path for the bot
    path = astar(grid, start, goal, bot_algo="v1")
    if not path:
        print("No path found. The bot is trapped.")
    
    for i in range(1, len(path)):  # Skip the first position since it's the start
        bot_position = path[i]  # Move bot to next step
        grid = fire_spread(grid,q,goal)  # Simulate fire spread

        # Stop if fire spreads onto bot's position
        if grid[bot_position[0]][bot_position[1]] == CELL_FIRE:
            print("Bot burned by fire! Failed.")
            break

        # Plot each timestep
        plot_grid(grid, start, goal, bot_position, path[:i+1])
        time.sleep(0.5)  # Pause to simulate time steps


        
if __name__ == "__main__":
    
    # Initialize grid and place fire
     grid = create_maze()

     grid = place_fire_randomly(grid)
     q = random.random() # Flammability of the ship

    # # Get valid start and goal position
     start, goal = generate_valid_start_goal(grid)

     print(f"Start: {start}, Goal: {goal}")

     simulate_bot_spread(start, goal, grid, q)