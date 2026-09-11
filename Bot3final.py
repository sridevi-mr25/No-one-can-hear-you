import random
import time

from fire1 import place_fire_randomly, fire_spread
from plot import plot_grid
from grid import create_maze, generate_valid_start_goal
from algorithm import astar
from constants import *

def simulate_bot_spread(start,goal, grid, q):
    bot_position = start  # Set the bot's initial position
    traversed_path = [start]  # Keep track of the path the bot has taken
    path_not_found_flag = False  # Flag to check if a valid path exists
    
    while bot_position != goal: # Keep moving until the bot reaches the goal
        bot_position = astar(grid, bot_position, goal) # Try finding the safest path using A* 
        # Stop if fire spreads onto bot's position
        
        # If no path is found, allow the bot to move next to fire (relaxing constraints)
        if not bot_position:
            path = astar(grid, bot_position, goal, "v3", neighbor_flag=False) # Try allowing fire-adjacent cells
            if not path:
                path_not_found_flag = True # If still no path, set the trapped flag
            else:
                path_not_found_flag = False # Path found, reset flag
        
        if path_not_found_flag:  
            print("No path found. The bot is trapped.") # The bot is stuck
            break
        if grid[bot_position[0]][bot_position[1]] == CELL_FIRE:
            print("Bot burned by fire! Failed.")
            break
        traversed_path.append(bot_position) # Save the new position to the traversed path
        print(f"Bot moved to {bot_position}")
        grid = fire_spread(grid,q,goal) # Simulate fire spreading in the environment

        plot_grid(grid, start, goal, bot_position,traversed_path) # Visualize the grid with updated positions
        time.sleep(0.5)


if __name__ == "__main__":
    # Initialize the grid and fire placement
    grid = create_maze()
    grid = place_fire_randomly(grid)
    q = random.random() #Flammability of the ship

    # Generate valid start and goal positions
    start, goal = generate_valid_start_goal(grid)
    print(f"Start: {start}, Goal: {goal}")
    simulate_bot_spread(start,goal, grid, q)
    
    
    