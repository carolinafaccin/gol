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

class Game():
    """
    Manages the state and rules of a Game of Life simulation.

    This class holds the grid of cells and provides the mechanism to
    advance the simulation to the next generation.
    """

    def __init__(self, rows, columns, survival_rules=[2, 3, 4, 5], birth_rules=[3]) -> None:
        """
        Initializes the Game of Life board with configurable rules.

        Sets up an empty grid of a given size and places a single, 
        predefined heart-shaped pattern in the center.

        Args:
            rows (int): The number of rows for the simulation grid.
            columns (int): The number of columns for the simulation grid.
            survival_rules (list[int]): A list of neighbor counts for a live cell to survive.
            birth_rules (list[int]): A list of neighbor counts for a dead cell to be born.
        
        Attributes:
            rows (int): Stores the number of rows.
            columns (int): Stores the number of columns.
            grid (np.ndarray): A 2D NumPy array representing the cell states
                (0 for dead, 1 for alive).
            survival_rules (list[int]): Stores the survival rules.
            birth_rules (list[int]): Stores the birth rules.
        """
        
        self.rows = rows
        self.columns = columns
        self.survival_rules = survival_rules
        self.birth_rules = birth_rules
        
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
        
        # 3. Calculate the cent≤er of the grid
        center_row = self.rows // 2
        center_col = self.columns // 2

        # 4. Place the heart pattern in the center of the grid
        place_pattern(self.grid, heart_pattern, center_row, center_col)
    
    def update(self) -> None:
        """
        Advances the simulation by one generation according to configurable rules.

        This method calculates the number of live neighbors for each cell on the
        grid using a highly optimized 2D convolution from the SciPy library. It
        then applies the rules defined in the `survival_rules` and `birth_rules`
        attributes of the class to the entire grid using efficient vectorized
        NumPy operations.

        This approach replaces the slower nested for-loops, making the simulation
        significantly more performant, especially for larger grids. The use of
        configurable rules allows the same code to simulate different "universes"
        or rule sets (e.g., standard Conway's Life, HighLife, Day & Night) by
        simply passing different lists during initialization.

        The core logic is as follows:
        - A dead cell becomes alive if its neighbor count is in `self.birth_rules`.
        - A live cell survives if its neighbor count is in `self.survival_rules`.
        - All other cells die or remain dead.
        """

        # Define the 3x3 kernel for the 2D convolution.
        kernel = np.array([[1, 1, 1],
                        [1, 0, 1],
                        [1, 1, 1]])

        # Apply 2D convolution to count live neighbors for every cell at once.
        total_neighbors = scipy.signal.convolve2d(self.grid, kernel, mode="same", boundary="wrap")

        # Create the new grid based on the rules using vectorized operations.
        new_grid = np.zeros_like(self.grid)

        # Survival Rule: A live cell survives if its neighbor count is in the survival_rules list.
        survival_mask = (self.grid == 1) & (np.isin(total_neighbors, self.survival_rules))
        new_grid[survival_mask] = 1

        # Birth Rule: A dead cell is born if its neighbor count is in the birth_rules list.
        birth_mask = (self.grid == 0) & (np.isin(total_neighbors, self.birth_rules))
        new_grid[birth_mask] = 1

        self.grid = new_grid


# --- Renderer Class ---

class Renderer():
    """
    The Renderer class encapsulates all the visualization logic.
    It receives style parameters and is responsible for generating images (frames).

    Handles the visualization of the Game of Life grid using Matplotlib.
    """

    def __init__(self, cell_colors, figsize=(3.5, 3.5), dpi=110):
        """
        Initializes the renderer with specific visualization parameters.

        Args:
            cell_colors (list): A list of colors for dead and alive cells.
            figsize (tuple): The figure size for the plot.
            dpi (int): The resolution of the figure.
        """
        self.colors = cell_colors
        self.cmap = mcolors.ListedColormap(self.colors)
        self.figsize = figsize
        self.dpi = dpi

    def render_frame(self, grid, step_num):
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        ax.imshow(grid, cmap=self.cmap)
        ax.set_title(f"Step: {step_num}", fontsize=14, fontname='Helvetica', pad=10)
        ax.set_xticks([])
        ax.set_yticks([])

        plt.tight_layout(pad=0)
        fig.canvas.draw()

        # Pega dimensões corretas pelo renderer (funciona no Mac)
        width, height = map(int, fig.canvas.renderer.get_canvas_width_height())

        buffer = fig.canvas.tostring_argb()
        plt.close(fig)

        # Converte buffer em array
        image_argb = np.frombuffer(buffer, dtype=np.uint8).reshape((height, width, 4))

        # ARGB → RGB
        return image_argb[:, :, [1, 2, 3]]


# --- Create Gif Function ---

def create_gif(game_instance, renderer_instance, steps, output_filename):
    """
    Creates and saves an animated GIF of the simulation.

    Args:
        game_instance (Game): The Game object to simulate.
        renderer_instance (Renderer): The Renderer object for visualization.
        steps (int): The total number of simulation steps to generate.
        output_filename (str): The full path for the output GIF file.
    """
    print("Generating frames for the animation...")

    with imageio.get_writer(output_filename, mode='I', fps=10, loop=0) as writer:
        for step_num in tqdm(range(steps), desc="Generating GIF frames"):
            frame = renderer_instance.render_frame(game_instance.grid, step_num)
            writer.append_data(frame)
            game_instance.update()

    print(f"\nAnimation saved successfully to '{output_filename}'!")


# --- Create Visualization Function ---

def create_visualization(game_instance, renderer_instance, steps):
    """
    Generates a real-time visualization of the simulation in a pop-up window.

    Args:
        game_instance (Game): The Game object to simulate.
        renderer_instance (Renderer): The Renderer object for visualization.
        steps (int): The total number of simulation steps to run.
    """
    print("Starting real-time visualization (close the window to stop)...")
    
    # Enable interactive mode for real-time plotting
    plt.ion()
    fig, ax = plt.subplots(figsize=renderer_instance.figsize, dpi=renderer_instance.dpi)

    ax.set_xticks([])
    ax.set_yticks([])

    for step_num in range(steps):
        ax.imshow(game_instance.grid, cmap=renderer_instance.cmap)
        ax.set_title(f"Step: {step_num}")
        
        # Update the plot in real-time
        plt.draw()
        plt.pause(0.1)  # Pause for a brief moment to show the frame
        
        game_instance.update()
    
    plt.ioff()
    plt.show() # Keep the last frame displayed until the user closes the window


if __name__ == '__main__':
    
    # --- GET SIMULATION PARAMETERS FROM USER INPUT ---
    try:
        matrix_size = int(input("Enter the grid size (e.g., 40): "))
        total_steps = int(input("Enter the number of simulation steps (e.g., 50): "))
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        matrix_size = 40
        total_steps = 41
        print(f"Using default values: grid size = {matrix_size}, steps = {total_steps}")
    
    # Define the rules and renderer
    current_survival_rules = [2, 3, 4, 5]
    current_birth_rules = [3]
    cell_colors = ["white", "#f77877"]

    # Create the Game instance
    game_instance = Game(matrix_size, matrix_size, survival_rules=current_survival_rules, birth_rules=current_birth_rules)
    
    # Create the Renderer instance
    renderer_instance = Renderer(cell_colors=cell_colors)
    
    # --- GET USER'S CHOICE (BEFORE THE GIF LOGIC) ---
    choice = input("Enter 'gif' to create an animated GIF or 'live' for real-time visualization: ").lower()

    if choice == 'gif':
        # --- Logic to create folder and filename for GIF file ---
        script_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(script_dir)
        output_dir = os.path.join(project_root, 'figures', 'gif', 'tests')
        os.makedirs(output_dir, exist_ok=True)
        base_filename = os.path.splitext(os.path.basename(__file__))[0]

        # Find the next available version number
        version = 1
        while True:
            version_str = f"v{version:03d}"
            gif_filename = f"{base_filename}_{version_str}.gif"
            full_path = os.path.join(output_dir, gif_filename)

            if not os.path.exists(full_path):
                break
            version += 1
        
        create_gif(game_instance, renderer_instance, total_steps, full_path)
    
    elif choice == 'live':
        create_visualization(game_instance, renderer_instance, total_steps)
    else:
        print("Invalid choice. Please run the script again and choose 'gif' or 'live'.")