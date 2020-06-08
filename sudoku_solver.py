# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 00:12:22 2020

@author: Zeng Fung Liew
Sudoku Solver
"""

import math
import numpy as np
import cvxpy
import time

# function to call for input of puzzle
def input_puzzle(filename):
    print("No such file exists. Please write the puzzle row by row.")
    f = open(filename, "w+")

    rows = [""] * 9
    
    for i in range(9):
        rows[i] = input("Print row " + str(i+1) + " (input 0 for empty cells): ")
        if rows[i] == "exit":
            break
        while len(rows[i]) != 9:
            rows[i] = input("Incorrect number of input, try again: ")
            if rows[i] == "exit":
                break
        f.write(rows[i] + "\n")
    f.close()

# function to obtain all constraints in the form of matrix
def obtain_constraints(textline):
    cell_constraints = find_cell_constraints()
    row_constraints = find_row_constraints()
    column_constraints = find_column_constraints()
    box_constraints = find_box_constraints()
    value_constraints = find_value_constraints(textline)
    constraints = np.vstack((cell_constraints, row_constraints, 
                             column_constraints, box_constraints, 
                             value_constraints))
    return (constraints)


def find_cell_constraints():
    all_cell_constraints = np.zeros((81,729), dtype = int)
    for i in range(0,9):
        for j in range(0,9):
            # row to adjust
            row = (9 * i) + j
            # set of constrainted cells
            idx_start = (81 * i) + (9 * j) 
            idx_end = (81 * i) + (9 * j) + 9
            all_cell_constraints[row][range(idx_start, idx_end)] = 1
    return (all_cell_constraints)
            
def find_row_constraints():
    all_row_constraints = np.zeros((81,729), dtype = int)
    for i in range(0,9):
        for k in range(0,9):
            # row to adjust
            row = (9 * i) + k
            # set of constrainted cells
            idx_start = (81 * i) + k
            idx_end = (81 * i) + 81 + k
            all_row_constraints[row][range(idx_start, idx_end, 9)] = 1
    return (all_row_constraints)
    
def find_column_constraints():
    all_column_constraints = np.zeros((81,729), dtype = int)
    for j in range(0,9):
        for k in range(0,9):
            # row to adjust
            row = (9 * j) + k
            # set of constrainted cells
            idx_start = (9 * j) + k
            idx_end = (81 * 9) + (9 * j) + k
            all_column_constraints[row][range(idx_start, idx_end, 81)] = 1
    return (all_column_constraints)
    
def find_box_constraints():
    all_box_constraints = np.zeros((81,729), dtype = int)
    box_cells = np.array([0,9,18,81,90,99,162,171,180], dtype = int)
    for m in range(0,3):
        for n in range(0,3):
            for k in range(0,9):
                row = 9 * (3 * m + n) + k
                mn_box_cells = (243 * m) + (27 * n) + k + box_cells
                all_box_constraints[row][mn_box_cells] = 1
    return all_box_constraints


def find_value_constraints(textline):
    value_constraints = np.empty((0,729), int)
    for idx in range(len(textline)):
        if textline[idx] != "0" and textline[idx] != "\n":
            row = math.floor(idx / 10)
            col = idx % 10
            value = int(textline[idx])
            constraint = np.zeros(729, dtype = int)
            constraint_idx = (81 * row) + (9 * col) + (value - 1)
            constraint[constraint_idx] = 1
            value_constraints = np.vstack((value_constraints, constraint))
    return (value_constraints)

def solve_sudoku(A):
    num_constraints = np.shape(A)[0]
    num_var = np.shape(A)[1]
    # constraints formulation of Ax=b
    b = np.ones((num_constraints,1), dtype = int)
    x = cvxpy.Variable((num_var,1), boolean = True)
    constraint = A @ x == b
    # objective function
    obj = np.ones((1,num_var)) @ x
    # solving the sudoku problem
    sudoku_problem = cvxpy.Problem(cvxpy.Maximize(obj), [constraint])
    sudoku_problem.solve(solver = cvxpy.GUROBI)
    if obj.value != 81:
        print("Wrong Calculation")
    return (x.value)

def print_solution(result_vector):
    result_matrix = np.zeros((9,9), dtype = int)
    for i in range(0,9):
        for j in range(0,9):
            cell_start = (81 * i) + (9 * j)
            cell_end = (81 * i) + (9 * j) + 9
            for k in range(cell_start, cell_end):
                if result_vector[k][0] == 1:
                    value = (k + 1) % 9
                    if value == 0:
                        value = 9
                    result_matrix[i][j] = value
                    print(str(value), end = "")
                    continue
            if j == 2 or j ==5:
                print("|", end = "")
        print("")
        if i == 2 or i == 5:
            print("---+---+---")
    return (result_matrix)


# ask for puzzle to solve
filename = input("File name for Sudoku puzzle: ")
try:
    f = open(filename, "r")
except:
    input_puzzle(filename)
    f = open(filename, "r")
finally:
    lines = f.read()
    f.close()

# find value constraints
constraint_matrix = obtain_constraints(lines)
start_time = time.time()
result = solve_sudoku(constraint_matrix)
end_time = time.time()
result_matrix = print_solution(result)
solve_time = end_time - start_time
print ("Solve time: ", solve_time, " seconds")

# write solutions file
solutions_file = "solutions_" + filename
sf = open(solutions_file, "w+")
for i in range(0,9):
    for j in range(0,9):
        sf.write(str(result_matrix[i][j]))
    sf.write("\n")
sf.close()

