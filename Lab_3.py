import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.widgets import Slider
import random

n = 15
blue_percentage = 0.45
red_percentage = 0.45
empty_percentage = 0.10


def initialize_grid(n, blue_percentage, red_percentage, empty_percentage):
    cells = np.random.choice(
        [0, 1, 2], size=(n, n),
        p=[empty_percentage, blue_percentage, red_percentage]
    )
    return cells


def is_happy(grid, x, y):
    color = grid[x, y]
    if color == 0:
        return True

    neighbors = []
    for i in range(max(0, x - 1), min(n, x + 2)):
        for j in range(max(0, y - 1), min(n, y + 2)):
            if (i, j) != (x, y):
                neighbors.append(grid[i, j])

    same_color_neighbors = neighbors.count(color)
    return same_color_neighbors >= 2


def move_unhappy_cells(grid):
    unhappy_cells = [(x, y) for x in range(n) for y in range(n)
                     if grid[x, y] != 0 and not is_happy(grid, x, y)]
    empty_cells = [(x, y) for x in range(n) for y in range(n) if grid[x, y] == 0]

    if not unhappy_cells or not empty_cells:
        return False

    for (x, y) in unhappy_cells:
        new_x, new_y = random.choice(empty_cells)
        grid[new_x, new_y] = grid[x, y]
        grid[x, y] = 0
        empty_cells.remove((new_x, new_y))
        empty_cells.append((x, y))

    return True


def simulate_and_store(max_steps):
    global grid_states
    grid = initialize_grid(n, blue_percentage, red_percentage, empty_percentage)
    grid_states = [grid.copy()]

    for step in range(0, max_steps):
        if not move_unhappy_cells(grid):
            break  # Остановка, если все клетки счастливы
        grid_states.append(grid.copy())


simulate_and_store(50)

fig, ax = plt.subplots(figsize=(6, 6))
cmap = ListedColormap(['white', 'blue', 'red'])
im = ax.imshow(grid_states[0], cmap=cmap)
plt.axis('off')

slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor='lightgrey')
iteration_slider = Slider(slider_ax, 'Step', 0, len(grid_states) - 1, valinit=0, valstep=1)


def update(val):
    iteration = int(iteration_slider.val)
    im.set_data(grid_states[iteration])
    fig.canvas.draw_idle()


iteration_slider.on_changed(update)

plt.show()
