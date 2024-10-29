import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.colors import ListedColormap


n = 50
blue_ratio = 0.45
red_ratio = 0.45
empty_ratio = 0.10
threshold = 2


def initialize_grid(n, blue_ratio, red_ratio, empty_ratio):
    total_cells = n * n
    num_blue = int(total_cells * blue_ratio)
    num_red = int(total_cells * red_ratio)
    num_empty = total_cells - num_blue - num_red

    grid = np.array([1] * num_blue + [2] * num_red + [0] * num_empty)
    np.random.shuffle(grid)
    return grid.reshape((n, n))


def is_happy(grid, x, y):
    cell = grid[x, y]
    if cell == 0:
        return True

    neighbors = grid[max(0, x - 1):min(n, x + 2), max(0, y - 1):min(n, y + 2)]
    same_color_count = np.sum(neighbors == cell) - 1
    return same_color_count >= threshold


def step(grid):
    unhappy_cells = []
    empty_cells = list(zip(*np.where(grid == 0)))


    for x in range(n):
        for y in range(n):
            if grid[x, y] != 0 and not is_happy(grid, x, y):
                unhappy_cells.append((x, y))


    np.random.shuffle(unhappy_cells)
    for x, y in unhappy_cells:
        if empty_cells:
            new_x, new_y = empty_cells.pop()
            grid[new_x, new_y], grid[x, y] = grid[x, y], 0

    return grid

grid = initialize_grid(n, blue_ratio, red_ratio, empty_ratio)

cmap = ListedColormap(["white", "blue", "red"])

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
im = ax.imshow(grid, cmap=cmap)

ax_slider = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
iteration_slider = Slider(ax_slider, 'Iteration', 0, 100, valinit=0, valstep=1)


def update(val):
    iteration = int(iteration_slider.val)
    temp_grid = grid.copy()
    for _ in range(iteration):
        temp_grid = step(temp_grid)
    im.set_data(temp_grid)
    fig.canvas.draw_idle()


iteration_slider.on_changed(update)
plt.show()
