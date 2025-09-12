"""
A simulation of Conway's Game of Life.

This script provides a clean, modular, and extensible framework
for simulating Conway's Game of Life and its variations.

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
    advance the simulation to the next generation based on configurable rules.
    """

    def __init__(self, rows, columns, survival_rules=[2, 3], birth_rules=[3], initial_pattern=None) -> None:
        """
        Initializes the Game of Life board with a specified initial pattern.

        Args:
            rows (int): The number of rows for the simulation grid.
            columns (int): The number of columns for the simulation grid.
            survival_rules (list[int]): A list of neighbor counts for a live cell to survive.
                                        Defaults to standard B3/S23 rules.
            birth_rules (list[int]): A list of neighbor counts for a dead cell to be born.
                                     Defaults to standard B3/S23 rules.
            initial_pattern (np.ndarray, optional): A custom pattern to place on the grid.
                                                    Defaults to None, which creates an empty grid.

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

        # Initialize the grid
        self.grid = np.zeros((rows, columns), dtype=int)

        # Helper function to place a pattern at a given position
        def place_pattern(grid, pattern, center_row, center_col):
            pattern_height, pattern_width = pattern.shape
            start_row = center_row - pattern_height // 2
            start_col = center_col - pattern_width // 2
            
            if start_row >= 0 and start_col >= 0 and \
               (start_row + pattern_height) <= grid.shape[0] and \
               (start_col + pattern_width) <= grid.shape[1]:
                grid[start_row : start_row + pattern_height, start_col : start_col + pattern_width] = pattern

        # Place the pattern if one is provided
        if initial_pattern is not None:
            center_row = self.rows // 2
            center_col = self.columns // 2
            place_pattern(self.grid, initial_pattern, center_row, center_col)
    

    def update(self) -> None:
        # ... (update method is the same) ...
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])


        total_neighbors = scipy.signal.convolve2d(self.grid, kernel, mode="same", boundary="wrap")
        
        new_grid = np.zeros_like(self.grid)


        survival_mask = (self.grid == 1) & (np.isin(total_neighbors, self.survival_rules))
        new_grid[survival_mask] = 1


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

    def __init__(self, cell_colors, figsize=(6, 6), dpi=160):
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

        plt.tight_layout(pad=0.2)
        
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
    
    # --- DEFAULT TO A RANDOM INITIAL PATTERN ---
    # The random pattern is now the standard initial state, without asking the user.
    initial_pattern = np.random.randint(0, 2, (matrix_size, matrix_size), dtype=int)
    
    # Define the rules and renderer
    current_survival_rules = [2, 3]
    current_birth_rules = [3]
    cell_colors = ["white", "#f77877"]

    # Create the Game instance with the prepared pattern
    # The 'initial_state' argument is no longer needed in Game.__init__()
    game_instance = Game(matrix_size, matrix_size, 
                         survival_rules=current_survival_rules, 
                         birth_rules=current_birth_rules, 
                         initial_pattern=initial_pattern)

    # Create the Renderer instance
    renderer_instance = Renderer(cell_colors=cell_colors)

    # --- GET USER'S CHOICE for output (gif or live) ---
    choice = input("Enter 'gif' to create an animated GIF or 'live' for real-time visualization: ").lower()

    if choice == 'gif':
        # --- Logic to create folder and filename for GIF file ---
        script_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(script_dir)
        output_dir = os.path.join(project_root, 'figures', 'gif', 'tests')
        os.makedirs(output_dir, exist_ok=True)
        base_filename = os.path.splitext(os.path.basename(__file__))[0]


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
        print("Invalid choice. Please run the script again and choose a valid option.")