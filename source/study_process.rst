.. study_process:

Study Process Documentation
===========================

This document logs the experiments and modifications made during the development of the Game of Life project.
Each entry details a specific change, the reasoning behind it, and the result.

---

V.0.0.0 - Initial Prototype based on Santos (2023)
-------------------------------------------------
This is the original implementation of the Game of Life as created by Santos (2023). It uses standard Python lists and basic loops to simulate the game, printing the grid to the console with ASCII characters.

* `Article on Medium <https://c137santos.medium.com/a-implementa%C3%A7%C3%A3o-do-game-of-life-em-python-3c2da1536957>`_
* `Repo on GitHub <https://github.com/c137santos/saw>`_

---


V.0.0.1 - Refactoring with NumPy and Matplotlib
-------------------------------------------------
This version represents a significant refactoring of the original code. It moves from a console-based, ASCII visualization to a graphical one by adopting **NumPy** for matrix operations and **Matplotlib** for visualization. This change makes the code more efficient for large grids and provides a much richer visual output.

Key changes from V.0.0.0:

* **Data Structure:** The core game grid is now a **NumPy array** instead of a Python list of lists. This allows for faster and more memory-efficient calculations.
* **Neighbor Calculation:** The `__alive_nbs` method and its complex logic were replaced by a more elegant, vectorized approach. The `update` method now uses the toroidal boundary condition with the modulo operator (`%`) to count neighbors, a common and efficient method for Game of Life.
* **Visualization:** Instead of printing to the console, the code now generates a series of plots using **Matplotlib** and compiles them into a GIF using **Imageio**. This is a massive leap in functionality and visual quality.

---

V.0.0.2 - Custom Patterns and Rules
-----------------------------------
This version shifts the focus from a random initial grid to a predefined pattern: four heart shapes. To prevent these patterns from dying under the original rules, the simulation rules were modified to be more "generous" to promote continuous growth.

Key changes from V.0.0.1:

* **Initial State:** The `__init__` method was completely changed to no longer generate a random grid based on a percentage of live cells. Instead, it creates a blank grid and places a predefined heart-shaped pattern in four quadrants.
* **Survival Rules:** The `update` method was modified. The condition for a live cell to survive was expanded from `(alive_n == 2 or alive_n == 3)` to `(alive_n == 2 or alive_n == 3 or alive_n == 4)`. This change allows the patterns to survive and grow without being killed off by overpopulation.

---

V.1.0.0 - A Single, Growing Heart
---------------------------------
This version simplifies the simulation to focus on a single, centrally located growing heart. It removes the previous four-heart pattern, making the simulation cleaner and easier to follow. The code was also translated to English and documented with clear docstrings.

Key changes from V.0.0.2:

* **Pattern Placement:** The `__init__` method was simplified to place only a **single heart pattern** in the center of the grid, rather than four.
* **Code Documentation:** All comments and variable names were translated from Portuguese to English. Comprehensive docstrings were added to the `Game` class and its methods, improving code readability and maintainability.
* **Survival Rules Refinement:** The survival rules were adjusted slightly. The new rule states that a live cell with 2, 3, 4, or 5 neighbors survives. This change further promotes growth by making the "overpopulation" rule less strict.

---

V.1.0.1 - Improved Visualization and Code Structure
-------------------------------------------------
This version enhances the visualization and further improves code structure. It introduces a custom color map for the cells and adds more detailed comments to the visualization section.

Key changes from V.1.0.0:

* **Custom Colors:** The visualization now uses a custom `ListedColormap` from `matplotlib.colors`. This allows the "alive" cells to be a specific shade of red (`#f77877`) on a white background, replacing the default black-and-white binary map.
* **Docstrings and Comments:** The docstrings were updated to include a clear explanation of the simulation's custom rules and the logic behind them. The visualization function was also given more detailed inline comments.

---

V.1.0.2 - Performance Optimization with `scipy.signal.convolve2d`
-----------------------------------------------------------------
This version addresses a major performance bottleneck: the use of nested loops for updating the grid. It introduces a vectorized, highly efficient approach using a 2D convolution from the **SciPy** library.

Key changes from V.1.0.1:

* **Vectorized Update Logic:** The `update` method was completely rewritten. It no longer uses nested `for` loops. Instead, it leverages `scipy.signal.convolve2d` to count all neighbors for the entire grid in a single, fast operation.
* **Efficient GIF Creation:** The animation logic was improved to use `imageio.get_writer`. This change eliminates the need to store all frames in memory before saving the GIF, making it possible to generate very long or large animations without running out of RAM.

---

V.1.0.3 - Parameter Inputs and Error Handling
---------------------------------------------
This version makes the script more user-friendly and flexible by allowing the user to specify the simulation parameters.

Key changes from V.1.0.2:

* **User Input:** The `if __name__ == '__main__':` block was modified to prompt the user to enter the `matrix_size` and `total_steps` at runtime using the `input()` function.
* **Robustness:** A `try-except` block was added to handle cases where the user enters non-integer input. The program now catches `ValueError` and provides a graceful exit or uses default values, preventing crashes.

---

V.1.0.4 - Adding a Visual Progress Bar
--------------------------------------
This final version improves the user experience by providing real-time feedback on the simulation's progress.

Key changes from V.1.0.3:

* **Progress Bar:** The `tqdm` library was integrated to add a dynamic progress bar to the frame generation loop. This simple change provides a clear visual indicator of the simulation's status, showing the percentage completed and the estimated time remaining, a significant improvement over simple print statements.