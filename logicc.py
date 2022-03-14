# logic.py to be
# imported in the 2048.py file

# importing random package
# for methods to generate random
# numbers.
import random

from numpy import matrix

# function to initialize game / grid
# at the start
def start_game():

	# declaring an empty list then
	# appending 4 list each with four
	# elements as 0.
	mat =[]
	for i in range(4):
		mat.append([0] * 4)

	# printing controls for user
	print("Commands are as follows : ")
	print("'W' or 'w' : Move Up")
	print("'S' or 's' : Move Down")
	print("'A' or 'a' : Move Left")
	print("'D' or 'd' : Move Right")

	# calling the function to add
	# a new 2 in grid after every step
	add_new_2(mat)
	return mat

# function to add a new 2 in
# grid at any random empty cell
def add_new_2(mat):

# choosing a random index for
# row and column.
	r = random.randint(0, 3)
	c = random.randint(0, 3)

	# while loop will break as the
	# random cell chosen will be empty
	# (or contains zero)
	while(mat[r] != 0):
		r = random.randint(0, 3)
		c = random.randint(0, 3)

	# we will place a 2 at that empty
	# random cell.
	mat[r] = 2

# function to get the current
# state of game

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

	return mat





def get_current_state(mat):
    # check for win cell
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 2048:
                return True
    # check for any zero entries
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return True
    # check for same cells that touch each other
    for i in range(len(mat)-1):
        # intentionally reduced to check the row on the right and below
        # more elegant to use exceptions but most likely this will be their solution
        for j in range(len(mat[0])-1):
            if mat[i][j] == mat[i+1][j] or mat[i][j+1] == mat[i][j]:
                return True
    for k in range(len(mat)-1):  # to check the left/right entries on the last row
        if mat[len(mat)-1][k] == mat[len(mat)-1][k+1]:
            return True
    for j in range(len(mat)-1):  # check up/down entries on last column
        if mat[j][len(mat)-1] == mat[j+1][len(mat)-1]:
            return True
    return False


# all the functions defined below
# are for left swap initially.

# function to compress the grid
# after every step before and
# after merging cells.
def compress(mat):

	# bool variable to determine
	# any change happened or not
	changed = False

	# empty grid
	new_mat = []

	# with all cells empty
	for i in range(4):
		new_mat.append([0] * 4)
		
	# here we will shift entries
	# of each cell to it's extreme
	# left row by row
	# loop to traverse rows
	for i in range(4):
		pos = 0

		# loop to traverse each column
		# in respective row
		for j in range(4):
			if(mat[i][j] != 0):
				
				# if cell is non empty then
				# we will shift it's number to
				# previous empty cell in that row
				# denoted by pos variable
				new_mat[i][pos] = mat[i][j]
				
				if(j != pos):
					changed = True
				pos += 1

	# returning new compressed matrix
	# and the flag variable.
	return new_mat, changed

# function to merge the cells
# in matrix after compressing
def merge(mat):
	
	changed = False
	
	for i in range(4):
		for j in range(3):

			# if current cell has same value as
			# next cell in the row and they
			# are non empty then
			if(mat[i][j] == mat[i][j + 1] and mat[i][j] != 0):

				# double current cell value and
				# empty the next cell
				mat[i][j] = mat[i][j] * 2
				mat[i][j + 1] = 0

				# make bool variable True indicating
				# the new grid after merging is
				# different.
				changed = True

	return mat, changed

# function to reverse the matrix
# means reversing the content of
# each row (reversing the sequence)
def reverse(mat):
	new_mat =[]
	for i in range(4):
		new_mat.append([])
		for j in range(4):
			new_mat[i].append(mat[i][3 - j])
	return new_mat

# function to get the transpose
# of matrix means interchanging
# rows and column
def transpose(mat):
	new_mat = []
	for i in range(4):
		new_mat.append([])
		for j in range(4):
			new_mat[i].append(mat[j][i])
	return new_mat

# function to update the matrix
# if we move / swipe left
def move_left(grid):

	# first compress the grid
	new_grid, changed1 = compress(grid)

	# then merge the cells.
	new_grid, changed2 = merge(new_grid)
	
	changed = changed1 or changed2

	# again compress after merging.
	new_grid, temp = compress(new_grid)
	

	# return new matrix and bool changed
	# telling whether the grid is same
	# or different
	return new_grid,canMoveLeft(new_grid),changed

# function to update the matrix
# if we move / swipe right
def move_right(grid):

	# to move right we just reverse
	# the matrix
	new_grid = reverse(grid)

	# then move left
	new_grid,is_valid, changed = move_left(new_grid)

	# then again reverse matrix will
	# give us desired result
	new_grid = reverse(new_grid)
	return new_grid,canMoveRight(new_grid), changed

# function to update the matrix
# if we move / swipe up
def move_up(grid):

	# to move up we just take
	# transpose of matrix
	new_grid = transpose(grid)

	# then move left (calling all
	# included functions) then
	new_grid,is_valid, changed = move_left(new_grid)

	# again take transpose will give
	# desired results
	new_grid = transpose(new_grid)
	return new_grid,canMoveUp(new_grid), changed

# function to update the matrix
# if we move / swipe down
def move_down(grid):

	# to move down we take transpose
	new_grid = transpose(grid)

	# move right and then again
	new_grid,is_valid, changed = move_right(new_grid)

	# take transpose will give desired
	# results.
	new_grid = transpose(new_grid)
	return new_grid,canMoveDown(new_grid), changed

# this file only contains all the logic
# functions to be called in main function
# present in the other file

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