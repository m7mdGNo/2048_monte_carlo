from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
import random
from logic import canMoveDown, canMoveLeft, canMoveRight, canMoveUp, move_down,move_left,move_right,move_up,add_new_tile,get_current_state
import keyboard

class GameDriver:    
    def __init__(self):
        self.url = 'https://hczhcz.github.io/2048/20ez/'
        self.PATH = 'C:/Program Files (x86)/chromedriver.exe'
        self.driver = webdriver.Chrome(self.PATH)
        self.driver.get(self.url)
        self.body = self.driver.find_element_by_tag_name('body')
        self.moves = {
            0: Keys.ARROW_UP,
            1: Keys.ARROW_DOWN,
            2: Keys.ARROW_LEFT,
            3: Keys.ARROW_RIGHT
        }
    
    def getGrid(self):
        matrix = [[0 for i in range(4)] for j in range(4)]
        tiles = self.driver.find_elements_by_class_name('tile')
        
        for tile in tiles:
            cls = tile.get_attribute('class')
            col, row = cls.split('tile-position-')[1].split(' ')[0].split('-')
            col, row = int(col)-1, int(row)-1
            num = int(cls.split('tile tile-')[1].split(' ')[0])
            if num > matrix[row][col]:
                matrix[row][col] = num
        return matrix
    
    def move(self, moveCode):
        self.body.send_keys(self.moves[moveCode])
        time.sleep(0.1)

def check_add_tiles(mat):
    lst = []
    for i in mat:
        for j in i:
            lst.append(str(j))
    if '0' in lst:
        return True
    return False

def monte_carlo(matrix,searches_per_move,search_length):
    moves = [move_up,move_down,move_left,move_right]
    can_move=[canMoveUp,canMoveDown,canMoveLeft,canMoveRight]
    scores = [0,0,0,0]
    
    for first_index in range(len(moves)):

        is_valid = can_move[first_index](matrix)
        if is_valid:
            search_matrix ,change = moves[first_index](matrix)
            search_matrix = add_new_tile(search_matrix)
            scores[first_index] += change
        else:
            continue
        
        for _ in range(searches_per_move):
            new_mat = np.copy(search_matrix)
            random_move=random.choice(moves)
            is_valid = can_move[moves.index(random_move)]
            if is_valid:
                new_mat,change = random_move(search_matrix)
                if check_add_tiles(new_mat):
                    new_mat = add_new_tile(new_mat)
                    scores[first_index] += change
                else:    
                    continue
            else:
                continue

            for _ in range(search_length):
                length_mat = np.copy(new_mat)
                random_move=random.choice(moves)
                is_valid = can_move[moves.index(random_move)]
                if is_valid:
                    length_mat,change = random_move(new_mat)
                    if check_add_tiles(length_mat):
                        length_mat = add_new_tile(length_mat)
                        scores[first_index] += change
                    else:
                        continue
                else:
                    continue
    best_move = np.argmax(scores)
    return best_move

game = GameDriver()
moves = ['move_up','move_down','move_left','move_right']
time.sleep(2)
while True:
    matrix = game.getGrid()
    best_move = monte_carlo(matrix,50,20)
    game.move(best_move)
    print(f'best move is : {moves[best_move]}')
    if not get_current_state(matrix):
        break