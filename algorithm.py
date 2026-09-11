import heapq
from fire1 import is_fire_affected
from constants import *

# A heuristic function to estimate how far a point is from the goal.It uses the Manhattan Distance
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* search algorithm to find the shortest path from start to goal.
def astar(grid, start, goal, bot_algo="v2", neighbor_flag=True):
    open_list = [] # Priority queue for the cells to explore
    
    came_from = {} # Keeps track of the path that we came from
    g_score = {start: 0} # Cost from start to each cell
    h_score = {start: heuristic(start, goal)} # Estimated total cos
    heapq.heappush(open_list, (g_score[start] + h_score[start], g_score[start], start))
    
    while open_list:
        _, g, current = heapq.heappop(open_list) # Get the cell with the lowest cost.

        # If we reached the goal, trace the path back
        if current == goal:
            if bot_algo == "v1":
                return bot_v1(start, current, came_from)
            else:
                return bot_v2_v3(current, came_from)
        
         # Explore neighboring cells
        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if not (0 <= neighbor[0] < DIMENSION and 0 <= neighbor[1] < DIMENSION):  
                continue   # Ignore cells outside the grid

            # Avoid obstacles and fire-affected cells
            if grid[neighbor[0]][neighbor[1]] in [CELL_OBSTACLE, CELL_FIRE]:
                continue  # Skip this neighbor
            
            if bot_algo == "v3":
                if is_fire_affected(grid, neighbor,neighbor_flag):
                    continue
            tentative_g_score = g + 1 # The cost of moving to this cell

            # Update the path if this is a better route
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                h_score[neighbor] = heuristic(neighbor, goal)
                heapq.heappush(open_list, (g_score[neighbor] + h_score[neighbor], g_score[neighbor], neighbor))

    return None  # No path found

def bot_v1(start, current, came_from):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse() # Reverse to get the correct order from start to the goal.
    return path

def bot_v2_v3(current, came_from):
    last_node = None
    while current in came_from:
        last_node = current
        current = came_from[current]
    return last_node