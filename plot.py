import matplotlib.pyplot as plt
import numpy as np

# Plots the grid, including the bot, obstacles, fire, start, and goal.
def plot_grid(grid, initial_start, goal, bot_position, path=None):
    grid_array = np.array(grid)
    plt.figure(figsize=(10, 10))
    plt.imshow(grid_array, cmap='gray_r')

    # Plot obstacles
    obstacle_x, obstacle_y = np.where(grid_array == 1)
    plt.scatter(obstacle_y, obstacle_x, color='black', marker='s', label='Obstacles')

    # Plot fire dynamically at each timestep
    fire_x, fire_y = np.where(grid_array == 2)
    plt.scatter(fire_y, fire_x, color='orange', marker='s', label='Fire')

    # Plot initial start position (fixed)
    plt.scatter(initial_start[1], initial_start[0], color='green', label='Start', s=100, edgecolors='black', linewidth=1.5)

    # Plot goal position (fixed)
    plt.scatter(goal[1], goal[0], color='red', label='Goal', s=100, edgecolors='black', linewidth=1.5)

    # Plot the bot's path dynamically (only up to its current position)
    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_y, path_x, color='blue', linewidth=2, label='Path')

    # Plot the bot's current position
    if bot_position:
        plt.scatter(bot_position[1], bot_position[0], color='blue', s=120, label='Bot', edgecolors='black', linewidth=1.5)

    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(range(len(grid[0])))
    plt.yticks(range(len(grid)))
    plt.show()