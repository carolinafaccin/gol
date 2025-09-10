# Study Process Documentation

This document logs the experiments and modifications made during the development of the Game of Life project. Each entry details a specific change, the reasoning behind it, and the result.

---

### Example 1: SAW - Game of Life by Santos (2023)
Implementation of Game of Life in Python, as developed by Santos (2023)
[Article on Medium](https://c137santos.medium.com/a-implementa%C3%A7%C3%A3o-do-game-of-life-em-python-3c2da1536957)
[Repo on GitHub](https://github.com/c137santos/saw)


### Experiment 1: Simulating "Growth-Only" Rules

#### **Hypothesis**
The standard Game of Life rules include conditions for cells to die. What if the system only allowed for growth, similar to a simple urban expansion model? This would require removing the rules for cell death due to loneliness or overpopulation.

#### **Modification**
The change was implemented in the `update` method of the `Game` class. The original `if/elif` block that checked for both survival and birth was replaced with a single `if` statement that only implements the birth rule.

**Before (Standard Rules):**
```python
# A live cell is checked for survival conditions
if self.grid[i, j] == 1 and (total_vizinhos < 2 or total_vizinhos > 5):
    new_grid[i, j] = 0 # The cell dies
# A dead cell is checked for birth conditions
elif self.grid[i, j] == 0 and total_vizinhos == 3:
    new_grid[i, j] = 1
```

**After (Growth-Only Rule):**
```python
# Only the birth rule is checked.
# If a cell is already alive, it is not affected and remains alive.
if self.grid[i, j] == 0 and total_vizinhos == 3:
    new_grid[i, j] = 1
```

#### **Result**
The simulation now exhibits a "growth-only" behavior. Once a cell becomes "alive," it never reverts to "dead." New cells are born on the edges of existing clusters according to the birth rule, causing the initial pattern to expand indefinitely without ever shrinking.

---

### Experiment 2: Implementing Custom Colors

#### **Hypothesis**
The default black-and-white (`cmap='binary'`) visualization is classic, but custom colors could make the simulation more visually appealing. The goal was to change the "alive" cells from black to a specific shade of red on a white background.

#### **Modification**
This required separating the simulation **logic** (which works best with `0` for dead and `1` for alive) from the **visualization**.

1.  The `Game` class was reverted to use `0` and `1` for its internal grid state.
2.  In the `create_animation` function, a `ListedColormap` from `matplotlib.colors` was used. A two-color map was defined: `["white", "#f77877"]`.
3.  The `ax.imshow()` call was updated to use this custom colormap. Matplotlib automatically maps the grid's `0` values to the first color (white) and `1` values to the second color (red).

**Code Snippet (`create_animation` function):**
```python
# Define the colors: the first for value 0, the second for value 1
colors = ["white", "#f77877"] # 0 -> white, 1 -> red
custom_cmap = mcolors.ListedColormap(colors)

# Pass the grid with 0s and 1s. The colormap handles the color translation.
ax.imshow(game.grid, cmap=custom_cmap)
```

#### **Result**
The final `.gif` now correctly displays the simulation with a white background and red cells, as intended. This approach cleanly separates the model's data from its visual representation.