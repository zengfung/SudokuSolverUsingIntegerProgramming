import math
import numpy as np
import cvxpy
import time

# function to obtain all constraints in the form of matrix
def obtain_constraints(sudoku_matrix):
    cell_constraints = find_cell_constraints()
    row_constraints = find_row_constraints()
    column_constraints = find_column_constraints()
    box_constraints = find_box_constraints()
    value_constraints = find_value_constraints(sudoku_matrix)
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


def find_value_constraints(sudoku_matrix):
    value_constraints = np.empty((0,729), int)
    for row_num in range(len(sudoku_matrix)):
        for col_num in range(len(sudoku_matrix)):
            if sudoku_matrix[row_num][col_num] != 0:
                value = sudoku_matrix[row_num][col_num]
                constraint = np.zeros(729, dtype = int)
                constraint_idx = (81 * row_num) + (9 * col_num) + (value - 1)
                constraint[constraint_idx] = 1
                value_constraints = np.vstack((value_constraints, constraint))
    return (value_constraints)
    
def solve_constraints(A):
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
        return 'fail'
    return (x.value.astype(int))

def print_solution(result_vector):
    result_matrix = np.zeros((9,9), dtype = int)
    vector_to_array = result_vector.reshape((9,9,9))
    for n in range(9):
        result_matrix += ((n+1) * vector_to_array[:,:,n])
    return (result_matrix)

def solve_sudoku(input_problem):
    sudoku_problem = input_problem[:]
    constraint_matrix = obtain_constraints(sudoku_problem)
    start_time = time.time()
    result = solve_constraints(constraint_matrix)
    if result == 'fail':
        return ('no solution', 'no time')
    end_time = time.time()
    solve_time = end_time - start_time
    result_matrix = print_solution(result)
    return (result_matrix, solve_time)