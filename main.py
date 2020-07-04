import argparse
from tkinter import *
import tkinter.font as font
import numpy as np
import sudoku_solver


NUMBER_BUTTON_WIDTH = 12
NUMBER_BUTTON_HEIGHT = 5
RESTART_BUTTON_WIDTH = 30
RESTART_BUTTON_HEIGHT = 10
SOLVE_BUTTON_WIDTH = 30
SOLVE_BUTTON_HEIGHT = 10

MARGIN = 10  # Pixels around the board
SUDOKU_CELL_WIDTH = 50
SUDOKU_CELL_HEIGHT = 50
SUDOKU_BOARD_WIDTH = SUDOKU_CELL_WIDTH * 9 + MARGIN * 2
SUDOKU_BOARD_HEIGHT = SUDOKU_CELL_HEIGHT * 9 + MARGIN * 2

# creating own exception
class SudokuError(Exception):
    """
    An application specific error.
    """
    pass

class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        (self.row, self.col) = (-1, -1)
        self.game = np.zeros((9,9), dtype = int)

        self.__initUI()

    def __initUI(self):
        # Writing title
        self.title = Label(self.parent, text = "SUDOKU SOLVER", font = font.Font(size = 30))
        self.title.grid(row = 0, column = 0, columnspan = 10)

        # creating the sudoku board
        self.board = Canvas(self.parent, width = SUDOKU_BOARD_WIDTH, height = SUDOKU_BOARD_HEIGHT)
        self.board.grid(row = 1, column = 1, columnspan = 9, rowspan = 9)

        # setting up the solve button
        self.button_solve = Button(self.parent, text = "Solve!", font = font.Font(size = 15), padx = SOLVE_BUTTON_WIDTH, pady = SOLVE_BUTTON_HEIGHT,
            command = self.__solve)
        self.button_solve.grid(row = 5, column = 10)

        # setting up the restart button
        self.button_restart = Button(self.parent, text = "Restart", font = font.Font(size = 15), padx = RESTART_BUTTON_WIDTH, pady = RESTART_BUTTON_HEIGHT,
            command = self.__clear_board)
        self.button_restart.grid(row = 6, column = 10)

        # setting up the number buttons
        button_1 = Button(self.parent, text = "1", padx = NUMBER_BUTTON_WIDTH, pady = NUMBER_BUTTON_HEIGHT, font = font.Font(size = 15), command = lambda: self.__key_clicked(1))
        button_2 = Button(self.parent, text = "2", padx = NUMBER_BUTTON_WIDTH, pady = NUMBER_BUTTON_HEIGHT, font = font.Font(size = 15), command = lambda: self.__key_clicked(2))
        button_3 = Button(self.parent, text = "3", padx = NUMBER_BUTTON_WIDTH, pady = NUMBER_BUTTON_HEIGHT, font = font.Font(size = 15), command = lambda: self.__key_clicked(3))
        button_4 = Button(self.parent, text = "4", padx = NUMBER_BUTTON_WIDTH, pady = NUMBER_BUTTON_HEIGHT, font = font.Font(size = 15), command = lambda: self.__key_clicked(4))
        button_5 = Button(self.parent, text = "5", padx = NUMBER_BUTTON_WIDTH, pady = NUMBER_BUTTON_HEIGHT, font = font.Font(size = 15), command = lambda: self.__key_clicked(5))
        button_6 = Button(self.parent, text = "6", padx = NUMBER_BUTTON_WIDTH, pady = NUMBER_BUTTON_HEIGHT, font = font.Font(size = 15), command = lambda: self.__key_clicked(6))
        button_7 = Button(self.parent, text = "7", padx = NUMBER_BUTTON_WIDTH, pady = NUMBER_BUTTON_HEIGHT, font = font.Font(size = 15), command = lambda: self.__key_clicked(7))
        button_8 = Button(self.parent, text = "8", padx = NUMBER_BUTTON_WIDTH, pady = NUMBER_BUTTON_HEIGHT, font = font.Font(size = 15), command = lambda: self.__key_clicked(8))
        button_9 = Button(self.parent, text = "9", padx = NUMBER_BUTTON_WIDTH, pady = NUMBER_BUTTON_HEIGHT, font = font.Font(size = 15), command = lambda: self.__key_clicked(9))
        button_clear = Button(self.parent, text = "Clear", padx = NUMBER_BUTTON_WIDTH, pady = NUMBER_BUTTON_HEIGHT, font = font.Font(size = 15), command = lambda: self.__key_clicked(0))

        button_1.grid(row = 11, column = 0)
        button_2.grid(row = 11, column = 1)
        button_3.grid(row = 11, column = 2)
        button_4.grid(row = 11, column = 3)
        button_5.grid(row = 11, column = 4)
        button_6.grid(row = 11, column = 5)
        button_7.grid(row = 11, column = 6)
        button_8.grid(row = 11, column = 7)
        button_9.grid(row = 11, column = 8)
        button_clear.grid(row = 11, column = 9)

        self.result_time = StringVar()
        self.result_time.set(" ") 
        self.result_time_label = Label(self.parent, textvariable = self.result_time, font = font.Font(size = 15))
        self.result_time_label.grid(row = 10, column = 0, columnspan = 10)

        # drawing the sudoku grid
        self.__draw_grid()

        # getting input from user via clicks and keys
        self.board.bind("<Button-1>", self.__cell_clicked)
        self.board.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3 x 3 squares
        """
        for i in range(10):
            # set color and thickness of lines 
            if i % 3 == 0:
                color = "blue"
                thickness = 3
            else:
                color = "gray"
                thickness = 1

            x0 = MARGIN + i * SUDOKU_CELL_WIDTH
            y0 = MARGIN
            x1 = MARGIN + i * SUDOKU_CELL_WIDTH
            y1 = SUDOKU_BOARD_HEIGHT - MARGIN
            self.board.create_line(x0, y0, x1, y1, fill = color, width = thickness)

            x0 = MARGIN
            y0 = MARGIN + i * SUDOKU_CELL_HEIGHT
            x1 = SUDOKU_BOARD_WIDTH - MARGIN
            y1 = MARGIN + i * SUDOKU_CELL_HEIGHT
            self.board.create_line(x0, y0, x1, y1, fill = color, width = thickness)

    def __cell_clicked(self, event):
        (x, y) = event.x, event.y

        # get the coordinates of the cell if the board is clicked
        if (MARGIN < x < SUDOKU_BOARD_WIDTH - MARGIN) and (MARGIN < y < SUDOKU_BOARD_HEIGHT - MARGIN):
            self.board.focus_set()

            # get row and col numbers from x,y coordinates
            row = (y - MARGIN) // SUDOKU_CELL_HEIGHT
            col = (x - MARGIN) // SUDOKU_CELL_WIDTH

            # if cell was selected already, deselect it
            if (row, col) == (self.row, self.col):
                (self.row, self.col) = (-1, -1)
            else:
                (self.row, self.col) = (row, col)
        else:
            (self.row, self.col) = (-1, -1)

        # once the cell is selected, highlight the cursor
        self.__draw_cursor()

    def __draw_cursor(self):
        # delete previous existing cursor
        self.board.delete("cursor")
        # highlight a new cell if needed
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SUDOKU_CELL_WIDTH + 1
            y0 = MARGIN + self.row * SUDOKU_CELL_HEIGHT + 1
            x1 = MARGIN + (self.col + 1) * SUDOKU_CELL_WIDTH - 1
            y1 = MARGIN + (self.row + 1) * SUDOKU_CELL_HEIGHT - 1
            self.board.create_rectangle(x0, y0, x1, y1,
                outline = "red", fill = "yellow", stipple = "gray12", tags = "cursor")

# NEED TO FIGURE OUT HOW TO ENTER NUMBER INTO THE CELLS
# AND STORE THE INPUT SOMEWHERE IN PROGRAM'S MEMORY
    def __key_pressed(self, event):
        # if a cell is selected/highlighted, obtain input
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game[self.row][self.col] = int(event.char)
            (self.row, self.col) = (-1, -1)
            self.__draw_puzzle()
            self.__draw_cursor()

    def __key_clicked(self, number):
        # same as __key_pressed function, except that we get input via buttons
        if self.row >= 0 and self.col >= 0:
            self.game[self.row][self.col] = int(number)
            (self.row, self.col) = (-1, -1)
            self.__draw_puzzle()
            self.__draw_cursor()

    def __draw_puzzle(self):
        self.board.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game[i][j]
                if answer != 0:
                    x = MARGIN + j * SUDOKU_CELL_WIDTH + SUDOKU_CELL_WIDTH / 2
                    y = MARGIN + i * SUDOKU_CELL_HEIGHT + SUDOKU_CELL_HEIGHT / 2
                    self.board.create_text(x, y, text = answer, font = font.Font(size = 15), tags = "numbers")

    def __draw_solution(self):
        self.board.delete("numbers")
        for i in range(9):
            for j in range(9):
                if self.game[i][j] == self.solution[i][j]:
                    color = "black"
                else:
                    color = "red"
                answer = self.solution[i][j]
                x = MARGIN + j * SUDOKU_CELL_WIDTH + SUDOKU_CELL_WIDTH / 2
                y = MARGIN + i * SUDOKU_CELL_HEIGHT + SUDOKU_CELL_HEIGHT / 2
                self.board.create_text(x, y, text = answer, font = font.Font(size = 15), fill = color, tags = "numbers")

    def __solve(self):
        (self.solution, self.time_taken) = sudoku_solver.solve_sudoku(self.game)
        self.__draw_solution()
        self.result_time.set("Time taken: " + str(self.time_taken) + " seconds")

        self.result_time_label = Label(self.parent, textvariable = self.result_time, font = font.Font(size = 15))
        self.result_time_label.grid(row = 10, column = 0, columnspan = 10)

    def __clear_board(self):
        self.game = np.zeros((9,9), dtype = int)
        self.__draw_puzzle()

        self.result_time.set("    ")
        self.result_time_label = Label(self.parent, textvariable = self.result_time, font = font.Font(size = 15))
        self.result_time_label.grid(row = 10, column = 0, columnspan = 10)

root = Tk()
SudokuUI(root)
root.mainloop()