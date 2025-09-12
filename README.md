# GOL
**GOL** - _Game of Life_ - is a coding project for hands-on practice with programming logic, data structures, and algorithms. 

The project aims to build a functional version of John Conway's classic cellular automaton, a system that simulates the evolution of cells based on a set of simple rules.

[![Documentation](https://img.shields.io/badge/docs-read%20the%20documentation-brightgreen)](https://carolinafaccin.github.io/gol/)

## Project Goals
- Implement core logic: Develop the rules for a two-dimensional grid based on Conway's four rules.
- Visualize the simulation: Create a visual representation of the grid and its evolution over time.
- Explore different patterns: Experiment with famous initial patterns like the Glider, Lightweight Spaceship, and the Gosper Glider Gun.

## Outputs

Example output from the `growing heart` pattern:

<img src="https://raw.githubusercontent.com/carolinafaccin/gol/main/figures/gif/growingheart_intro1.gif?raw=true" alt="Animated GIF of a growing heart pattern" width="350">

## Installing and Running GOL on a Local Machine

Follow these steps to get started:

1) Install `python 3`.
2) Install the following Python dependencies:
   * `numpy`
   * `matplotlib`
   * `imageio`
   * `scipy`
   * `tqdm`
3) Clone the [latest release of this repository](https://github.com/carolinafaccin/gol.git) (or download the `asset zip` folder).
4) Extract the files to a folder of your choice (e.g., `C:\Users\Home\Documents\gol`).
> **Warning**: Do not change internal folder or file names.
5) You can choose one of two options to run the project:
   * **a. Run `src/gol.py`:**
     * Set the matrix size and number of steps parameters on the inputs.
     * Choose to generate a live animation or a GIF, which will be saved in `figures/gif/tests`.
   * **b. Run the notebook `notebook/gol.ipynb`:**
     * Select the desired pattern and parameters, or create a new pattern.
     * This will create `.gif` figures in the `figures/gif/notebook_gifs` folder.

## Repository Structure
```
gol/
├── docs/           # Final HTML output for GitHub Pages
├── figures/        # Figures generated
├── notebooks/      # Notebook with different patterns to run
├── source/         # Sphinx source files for the documentation
├── src/            # Source code for the Game of Life
├── .gitignore
├── LICENSE
├── make.bat        # Sphinx file
├── Makefile        # Sphinx file
└── README.md
```
