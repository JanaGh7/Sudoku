# Sudoku Solver and Generator (Python + Tkinter)

This is a GUI-based Sudoku solver and puzzle generator implemented using Python. It uses **Constraint Satisfaction Problem (CSP)** solving techniques like **AC-3** (Arc Consistency) and **Backtracking Search** with heuristics to efficiently solve Sudoku puzzles. Users can input their own puzzle, generate one of varying difficulty, solve it with animation, or submit their own solution for validation.

## Features

- Solves Sudoku puzzles using AC-3 and Backtracking algorithms.
- Randomly generates puzzles with three difficulty levels: Easy, Medium, Hard.
- Built-in GUI using Tkinter with grid entry for user input.
- Validates user-submitted solutions.
- Allows users to input custom initial Sudoku puzzles.

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- Numpy

Install NumPy if needed:

```bash
pip install numpy
```

## How to Run

1. Save the code in a file called `sudoku_solver.py`.

2. Run the script:

```bash
python sudoku_solver.py
```

The GUI window will open where you can interact with the Sudoku board.

## How to Use

### Generating a Puzzle
- Click **Easy**, **Medium**, or **Hard** to generate a Sudoku puzzle of that difficulty.
- Pre-filled numbers will be disabled and can't be edited.

### Solving a Puzzle
- Click **Solve** to let the program solve the currently loaded puzzle. The solving process is animated.

### Submitting Your Own Solution
- Fill in your solution and click **Submit**.
- The program compares your solution with the correct one and highlights:
  - Green: Correct
  - Red: Incorrect

### Inputting a Custom Puzzle
- Type numbers (1–9) into the grid. Leave empty for blank cells.
- Click **Set Initial Puzzle** to register your puzzle.
- Then click **Solve** to see the solution or **Submit** to check your own filled values.

### Reset
- Click **Reset** to clear the board and input a new puzzle.

## Algorithms Used

### AC-3 (Arc Consistency Algorithm 3)
Enforces consistency between variables by removing incompatible values from domains.

### Backtracking Search
Recursively assigns values using:
- **Minimum Remaining Values (MRV)**: Chooses variable with the smallest domain.
- **Least Constraining Value (LCV)**: Tries values that rule out the fewest options for neighboring cells.

## Project Structure

All code is self-contained in one Python script:
- GUI setup with Tkinter
- CSP data structures and logic
- Puzzle generation and validation
- Solving logic with animated visualization

## Example

You can generate puzzles and see the animated solution, or copy your favorite Sudoku puzzle into the grid and solve it using the built-in logic.

## License

All rights reserved.

This project is proprietary. No part of this codebase may be copied, distributed, or modified without explicit written permission from the author.

© [Jana Ghoneim] [2024]