
import random
from numpy import matrix


def add_new_tile(mat):
	import numpy as np
	m = np.copy(mat)
	row = random.randint(0,3)
	col = random.randint(0,3)
	while (m[row][col] != 0):
		row = random.randint(0,3)
		col = random.randint(0,3)
	m[row][col] = random.choice([2,4])
	return m

def get_current_state(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return True
    for i in range(len(mat)-1):
        for j in range(len(mat[0])-1):
            if mat[i][j] == mat[i+1][j] or mat[i][j+1] == mat[i][j]:
                return True
    for k in range(len(mat)-1):
        if mat[len(mat)-1][k] == mat[len(mat)-1][k+1]:
            return True
    for j in range(len(mat)-1):
        if mat[j][len(mat)-1] == mat[j+1][len(mat)-1]:
            return True
    return False

def compress(mat):

	changed = False
	new_mat = []
	for i in range(4):
		new_mat.append([0] * 4)

	for i in range(4):
		pos = 0
		for j in range(4):
			if(mat[i][j] != 0):

				new_mat[i][pos] = mat[i][j]
				
				if(j != pos):
					changed = True
				pos += 1
	return new_mat, changed

def merge(mat):
	changed = False
	for i in range(4):
		for j in range(3):
			if(mat[i][j] == mat[i][j + 1] and mat[i][j] != 0):
				mat[i][j] = mat[i][j] * 2
				mat[i][j + 1] = 0
				changed = True

	return mat, changed

def reverse(mat):
	new_mat =[]
	for i in range(4):
		new_mat.append([])
		for j in range(4):
			new_mat[i].append(mat[i][3 - j])
	return new_mat

def transpose(mat):
	new_mat = []
	for i in range(4):
		new_mat.append([])
		for j in range(4):
			new_mat[i].append(mat[j][i])
	return new_mat

def move_left(grid):
	new_grid, changed1 = compress(grid)
	new_grid, changed2 = merge(new_grid)
	changed = changed1 or changed2
	new_grid, temp = compress(new_grid)
	return new_grid,changed


def move_right(grid):
	new_grid = reverse(grid)
	new_grid, changed = move_left(new_grid)
	new_grid = reverse(new_grid)
	return new_grid, changed

def move_up(grid):
	new_grid = transpose(grid)
	new_grid, changed = move_left(new_grid)
	new_grid = transpose(new_grid)
	return new_grid, changed

def move_down(grid):
	new_grid = transpose(grid)
	new_grid, changed = move_right(new_grid)
	new_grid = transpose(new_grid)
	return new_grid, changed

def canMoveUp(matrix) :
    for j in range(4):
        k = -1
        for i in range(3, -1, -1):
            if matrix[i][j] > 0:
                k = i
                break
        if k > -1:
            for i in range(k, 0, -1):
                if matrix[i-1][j] == 0 or matrix[i][j] == matrix[i-1][j]:
                    return True
    return False

def canMoveDown(matrix):
    for j in range(4):
        k = -1
        for i in range(4):
            if matrix[i][j] > 0:
                k = i
                break
        if k > -1:
            for i in range(k, 3):
                if matrix[i+1][j] == 0 or matrix[i][j] == matrix[i+1][j]:
                    return True
    return False

def canMoveLeft(matrix):
    for i in range(4):
        k = -1
        for j in range(3, -1, -1):
            if matrix[i][j] > 0:
                k = j
                break
        if k > -1:
            for j in range(k, 0, -1):
                if matrix[i][j-1] == 0 or matrix[i][j] == matrix[i][j-1]:
                    return True
    return False

def canMoveRight(matrix) -> bool:
    for i in range(4):
        k = -1
        for j in range(4):
            if matrix[i][j] > 0:
                k = j
                break
        if k > -1:
            for j in range(k, 3):
                if matrix[i][j+1] == 0 or matrix[i][j] == matrix[i][j+1]:
                    return True
    return False