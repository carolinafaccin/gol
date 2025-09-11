"""
A simulation of Conway's Game of Life with custom growth rules.

This script implements a variation of Conway's Game of Life that starts
with a single heart-shaped pattern. The rules are modified to favor
continuous growth, preventing cells from dying.


Under traditional rules, the cells forming the heart would diminish
due to the rules of loneliness (a live cell with fewer than 2 neighbors dies)
and overpopulation (a live cell with more than 3 neighbors dies).

To make the heart "grow", the rules needed to be made more "generous",
allowing cells to survive with more neighbors and thus expand.

To change this rule, the 'update' method within the 'Game' class was adjusted.



The simulation is visualized using Matplotlib and saved as an animated,
infinitely looping GIF.
"""


# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import imageio
import scipy.signal
import os
from tqdm import tqdm

# --- Main Game of Life Class ---
# --- Main Game of Life Class ---
class Game():
    """
    Manages the state and rules of a Game of Life simulation.

    This class holds the grid of cells and provides the mechanism to
    advance the simulation to the next generation.
    """

    def __init__(self, rows, columns) -> None:
        """
        Initializes the Game of Life board.

        Sets up an empty grid of a given size and places a single, 
        predefined heart-shaped pattern in the center.

        Args:
            rows (int): The number of rows for the simulation grid.
            columns (int): The number of columns for the simulation grid.
        
        Attributes:
            rows (int): Stores the number of rows.
            columns (int): Stores the number of columns.
            grid (np.ndarray): A 2D NumPy array representing the cell states
                (0 for dead, 1 for alive).
        """
        
        self.rows = rows
        self.columns = columns
        
        # 1. Start with a completely empty grid (dtype=int is fine for 0s and 1s)
        self.grid = np.zeros((rows, columns), dtype=int)

        # 2. Define the heart pattern using 1 for "alive"
        heart_pattern = np.array([
            [0, 1, 1, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ], dtype=int)

        # Helper function to place a pattern at a given position
        def place_pattern(grid, pattern, center_row, center_col):
            pattern_height, pattern_width = pattern.shape
            start_row = center_row - pattern_height // 2
            start_col = center_col - pattern_width // 2
            
            # Ensures the pattern fits on the grid before placing it
            if start_row >= 0 and start_col >= 0 and \
               (start_row + pattern_height) <= grid.shape[0] and \
               (start_col + pattern_width) <= grid.shape[1]:
                grid[start_row : start_row + pattern_height, start_col : start_col + pattern_width] = pattern
        
        # 3. Calculate the center of the grid
        center_row = self.rows // 2
        center_col = self.columns // 2

        # 4. Place the heart pattern in the center of the grid
        place_pattern(self.grid, heart_pattern, center_row, center_col)

    def update(self) -> None:
            """
            Advances the simulation by one generation according to custom rules.

            This method optimizes the calculation of live neighbors using a 2D
            convolution and applies a modified set of Game of Life rules to the entire
            grid simultaneously using vectorized NumPy operations. This approach
            significantly improves performance compared to an iterative loop.

            The custom rules for this simulation are designed to promote continuous
            growth, preventing cells from dying easily. They are:

            * **Survival (S2345):** A live cell survives if it has 2, 3, 4, or 5 live
                neighbors. This deviates from the standard rule (S23) to prevent
                overpopulation from killing off cell clusters.
            * **Birth (B3):** A dead cell becomes a live cell if it has exactly 3
                live neighbors. This rule remains the same as in the original Game of Life.

            The use of a convolutional kernel and bitwise operations allows for a
            highly efficient, non-iterative update of the entire grid.
            """

            # Define the 3x3 kernel for the 2D convolution.
            # This kernel is used to count the 8 surrounding neighbors for each cell.
            kernel = np.array([[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]])

            # Apply 2D convolution to count live neighbors for every cell at once.
            # The 'mode="same"' parameter ensures the output grid has the same dimensions
            # as the input. The 'boundary="wrap"' parameter treats the grid's edges as
            # if they wrap around, creating a toroidal (donut-shaped) surface.
            total_neighbors = scipy.signal.convolve2d(self.grid, kernel, mode="same", boundary="wrap")

            # Create the new grid based on the rules using vectorized operations.
            # This approach applies the logic to the entire array at once, which is
            # much faster than using nested for-loops.
            new_grid = np.zeros_like(self.grid)

            # Survival Rule: A live cell with 2, 3, 4, or 5 neighbors remains alive.
            # The '&' operator performs a bitwise AND on the boolean masks.
            survival_mask = (self.grid == 1) & ((total_neighbors >= 2) & (total_neighbors <= 5))
            new_grid[survival_mask] = 1

            # Birth Rule: A dead cell with exactly 3 neighbors becomes a live cell.
            birth_mask = (self.grid == 0) & (total_neighbors == 3)
            new_grid[birth_mask] = 1

            # Update the main grid with the newly calculated states.
            self.grid = new_grid

# --- Function to create and save the animation ---
def create_animation(grid_size, steps, output_filename):
    """
    Creates and saves an animated GIF of the Game of Life simulation.

    This function initializes a Game instance, runs the simulation for a
    specified number of steps, and generates a visual representation of each
    step using Matplotlib. These frames are then compiled into a single,
    infinitely looping GIF file.

    Args:
        grid_size (int): The size (width and height) of the square grid.
        steps (int): The total number of simulation steps (frames) to generate.
        output_filename (str): The full path and filename for the output GIF.
    """

    game = Game(grid_size, grid_size)

    print("Generating frames for the animation...")

    # Use the writer's context to ensure the file is closed properly
    with imageio.get_writer(output_filename, mode='I', fps=10, loop=0) as writer:
        # Wrap the range() function with tqdm() to create a progress bar
        for step_num in tqdm(range(steps), desc="Generating frames"):
            fig, ax = plt.subplots(figsize=(3.5, 3.5), dpi=110)

            colors = ["white", "#f77877"]
            custom_cmap = mcolors.ListedColormap(colors)
            ax.imshow(game.grid, cmap=custom_cmap)

            ax.set_title(
                f"Step: {step_num}",
                fontsize=14,
                fontname='Helvetica',
                pad=10
            )
            ax.set_xticks([])
            ax.set_yticks([])

            fig.canvas.draw()
            
            width_float, height_float = fig.canvas.renderer.get_canvas_width_height()
            width = int(width_float)
            height = int(height_float)

            buffer = fig.canvas.tostring_argb()
            image_rgba = np.frombuffer(buffer, dtype='uint8').reshape(height, width, 4)
            
            # Add the frame directly to the writer, saving memory
            writer.append_data(image_rgba[:, :, 1:].copy())

            plt.close(fig)
            game.update()
            # Remove the old print statement, as tqdm handles progress display
            # print(f"  - Step {step_num + 1}/{steps} completed.")

    print(f"\nAnimation saved successfully to '{output_filename}'!")

# --- Main Script Execution ---
# --- Main Script Execution ---
if __name__ == '__main__':
    
    # --- GET SIMULATION PARAMETERS FROM USER INPUT ---
    # Ask for the grid size and convert the input to an integer
    try:
        matrix_size = int(input("Enter the grid size (e.g., 40): "))
        total_steps = int(input("Enter the number of simulation steps (e.g., 50): "))
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        # Exit the script or set default values if the input is not a number
        matrix_size = 40
        total_steps = 41
        print(f"Using default values: grid size = {matrix_size}, steps = {total_steps}")

    # --- Logic to create folder and filename ---

    # Get the current script's directory
    script_dir = os.path.dirname(__file__)
    # Go up one level to the project root directory
    project_root = os.path.dirname(script_dir)
    # Create the path for the output folder
    output_dir = os.path.join(project_root, 'figures', 'gif', 'tests')

    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Dynamically create the base filename from the script's name
    base_filename = os.path.splitext(os.path.basename(__file__))[0]

    # Find the next available version number
    version = 1
    while True:
        # Format the version number with 3 digits (e.g., 1 -> '001')
        version_str = f"v{version:03d}"
        # Assemble the filename with the version
        gif_filename = f"{base_filename}_{version_str}.gif"
        # Assemble the full path for the file
        full_path = os.path.join(output_dir, gif_filename)

        # Check if a file with this name already exists
        if not os.path.exists(full_path):
            break # If it doesn't exist, we've found the right name and exit the loop
        version += 1 # If it exists, try the next version
    
    # Call the main function with the fixed values and the versioned path
    create_animation(matrix_size, total_steps, full_path)