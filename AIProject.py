import numpy as np
import random
import math

def sudoku_cost(sudoku):
    cost = 0
    for i in range(9):
        row = sudoku[i, :]
        col = sudoku[:, i]
        cost += (9 - len(np.unique(row))) + (9 - len(np.unique(col)))
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block = sudoku[i:i+3, j:j+3].flatten()
            cost += 9 - len(np.unique(block))
    return cost

def random_fill(sudoku):
    filled_sudoku = sudoku.copy()
    for i in range(9):
        missing_nums = list(set(range(1, 10)) - set(filled_sudoku[i, :]))
        random.shuffle(missing_nums)
        for j in range(9):
            if filled_sudoku[i, j] == 0:
                filled_sudoku[i, j] = missing_nums.pop()
    return filled_sudoku

def swap_cells(sudoku, initial_sudoku):
    new_sudoku = sudoku.copy()
    empty_cells = [(i, j) for i in range(9) for j in range(9) if initial_sudoku[i, j] == 0]
    if len(empty_cells) < 2:
        return new_sudoku  # If less than 2 Block are empty, we will not change.
    
    (i1, j1), (i2, j2) = random.sample(empty_cells, 2)
    new_sudoku[i1, j1], new_sudoku[i2, j2] = new_sudoku[i2, j2], new_sudoku[i1, j1]
    return new_sudoku

def simulated_annealing(sudoku, max_iter=10000, initial_temp=100.0, cooling_rate=0.995):
    initial_sudoku = sudoku.copy()
    current_sudoku = random_fill(initial_sudoku)
    current_cost = sudoku_cost(current_sudoku)
    temp = initial_temp
    
    for iteration in range(max_iter):
        new_sudoku = swap_cells(current_sudoku, initial_sudoku)
        new_cost = sudoku_cost(new_sudoku)
        delta_cost = new_cost - current_cost
        
        if delta_cost < 0 or math.exp(-delta_cost / temp) > random.random():
            current_sudoku = new_sudoku
            current_cost = new_cost
        
        temp *= cooling_rate
        if current_cost == 0:
            break
    
    return current_sudoku

# Sample
initial_sudoku = np.array([
    [4, 9, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 9, 5, 0, 0, 2, 0],
    [0, 0, 0, 3, 0, 0, 2, 6, 1],
    [0, 0, 0, 6, 0, 4, 0, 3, 0],
    [0, 0, 0, 6, 0, 4, 0, 9, 0],
    [0, 0, 4, 0, 0, 0, 0, 1, 7],
    [0, 1, 0, 2, 0, 9, 3, 0, 0],
    [5, 0, 6, 0, 0, 1, 0, 0, 0]
])

solved_sudoku = simulated_annealing(initial_sudoku)
print(solved_sudoku)
