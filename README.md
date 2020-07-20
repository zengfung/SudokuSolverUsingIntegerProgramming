# sudoku_solver
Note: Majority of the code in `main.py` in building the user interface of the sudoku board was referenced from http://newcoder.io/gui/part-4/. Special thanks and credits to the author(s) of those codes.

The process of building the sudoku solver is split into 2 distinct sections:

* Building the User Interface

* Writing a program that solves sudoku puzzles via Integer (Binary) Programming methods. This method runs faster than the brute force backtracking method, but requires the user to have purchased the license for GUROBI and have its solver installed in the computer. 

## How does it work
1) By running `main.py`, we see an empty sudoku board.
2) Copy a puzzle into the sudoku board by clicking onto the cells and inputting numbers by typing on the keyboard or clicking on the numbers at the bottom part of the window.
3) Once the puzzle is copied into the sudoku board, click 'Solve' on the right hand side of the window and the solution will be displayed.
4) Click 'Restart' to clear the board and solve another puzzle.

## Error Handling
If an invalid puzzle is input into the board, "Sorry, this is not a valid puzzle. Try again." will be printed under the board. The user will then have to edit the error(s) on the sudoku board, or clear the board and try again.

## More Information on How This Works
The file 'Sudoku Solve.ipynb' contains more information regarding the logistics and how my sudoku solver works. Please refer to it for better explanations.
