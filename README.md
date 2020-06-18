# sudoku_solver
Solves sudoku puzzles and output its solution in a text file.

How does it work:
1) Obtains user input of .txt file that contains sudoku puzzle, if file exists, skip to step (3).
2) If no such file exist, ask for user input of the sudoku puzzle row by row. Empty cells will be written as 0.
3) Solves the sudoku puzzle by solving an integer (binary) program.
4) Outputs the solution in a .txt file.
