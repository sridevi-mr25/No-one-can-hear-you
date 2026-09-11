import heapq
import random
import numpy as np
import time

from fire1 import place_fire_randomly, fire_spread
from plot import plot_grid
from grid import create_maze, generate_valid_start_goal
from constants import *

# A heuristic function to estimate how far a point is from the goal.It uses the "Manhattan Distance" (sum of row and column differences).
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


#Assigns a risk factor (lamda) based on the probability of fire spread (q). Higher 'q' means higher fire risk, so 'lamda' increases.
def calculate_lamda(q):     
    if q < 0.3:
        lamda = 1  # Low risk
    elif q < 0.6 :
        lamda = 5  # Medium risk
    else :
        lamda = 10 # High risk
    
    return lamda

#Computes the fire risk for each open cell based on the probability 'q'. More fire in the neighborhood means a higher risk value.
def compute_fire_risk(grid, q):
    risk_map = np.zeros((DIMENSION, DIMENSION))  # Initialize a risk map with zero values
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if grid[i][j] == CELL_OPEN:  # Only open cells
                k = sum(grid[i + dx][j + dy] == CELL_FIRE for dx, dy in DIRECTIONS if 0 <= i + dx < DIMENSION and 0 <= j + dy < DIMENSION) # Count fire neighbors
                if k > 0:
                    risk_map[i][j] = 1 - (1 - q) ** k  # Fire spread probability formula
    return risk_map

#Adaptive A* Search Algorithm, updates heuristics dynamically to improve future searches.
def adaptive_astar(grid, start, goal, risk_cell, h_score, lamda):
    open_list = [] # Priority queue to store the next cells to explore
    if not isinstance(start, tuple):
        import pdb;pdb.set_trace()
    came_from = {} # Keeps track of the path that we came from
    g_score = {start: 0} # Cost from start to each cell
    h_score = {start: heuristic(start, goal)} # Estimated total cos
    heapq.heappush(open_list, (g_score[start] + h_score[start], g_score[start], start))

    closed_set = set() # Stores cells that have already been evaluated
    while open_list:
        _, g, current = heapq.heappop(open_list) # Get the cell with the lowest cost
        # If we reached the goal, reconstruct the path
        if current == goal:
            last_node = None
            while current in came_from:
                last_node = current
                current = came_from[current]
            
              # Update heuristics based on the actual cost from start to goal
            goal_g = g_score[goal]  # Get actual cost from start to goa
            for node in closed_set:
                h_score[node] = goal_g - g_score[node] # New heuristic: h(node) = goal_g - g(node)
            
            return last_node, h_score # Return the computed path and updated heuristics
        
        closed_set.add(current) # Mark the current node as explored

        # Explore neighboring cells
        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
             # Ensure neighbor is within grid bounds and not an obstacle
            if not (0 <= neighbor[0] < DIMENSION and 0 <= neighbor[1] < DIMENSION):  
                continue   # Ignore cells outside the grid

            # Avoid obstacles and fire-affected cells
            if grid[neighbor[0]][neighbor[1]] in [CELL_OBSTACLE, CELL_FIRE]:
                continue  # Skip this neighbor    
            tentative_g_score = g + 1 + lamda * risk_cell[neighbor] # Risk-adaptive cost( Higher risk nodes are avoided by increasing cost)
                # If this path to the neighbor is better than any previous one, update it
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                
                if not isinstance(neighbor, tuple):
                    import pdb;pdb.set_trace()
                h_score[neighbor] = h_score.get(neighbor,heuristic(neighbor, goal))
                heapq.heappush(open_list, (g_score[neighbor] + h_score[neighbor], g_score[neighbor], neighbor))

    return None, None # Return None if no path to the goal is found

def simulate_bot_spread(start,goal, grid, q):
    lamda = calculate_lamda(q) # Get fire risk level
    bot_position = start # Set the bot's initial position
    traversed_path = [start] # Keep track of the path the bot has taken
    h_score = {}
    while bot_position != goal:  # Keep moving until the bot reaches the goal
        risk_cell = compute_fire_risk(grid, q)  # Compute fire risk for all cells
        bot_position, h_score = adaptive_astar(grid, bot_position, goal, risk_cell, h_score, lamda)
        if not bot_position:
            print("No path found. The bot is trapped.")
            break

        
        traversed_path.append(bot_position) # Save the new position to the traversed path
        print(f"Bot moved to {bot_position}")
        grid = fire_spread(grid,q,goal) # Simulate fire spreading in the environment

        plot_grid(grid, start, goal, bot_position, traversed_path[:])  # Visualize the grid with updated positions
        time.sleep(0.5)  # Pause for better visualization


if __name__ == "__main__":
    # Initialize the grid and fire placement
    grid = create_maze()
    grid = place_fire_randomly(grid)
    q = random.random() #Flammability of the ship

    # # Generate valid start and goal positions
    start, goal = generate_valid_start_goal(grid)
    print(f"Start: {start}, Goal: {goal}")
    
    simulate_bot_spread(start, goal, grid, q)
    

