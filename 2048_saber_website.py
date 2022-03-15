from pyrsistent import CheckedKeyTypeError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import keyboard
import neat
import os
import numpy as np
from sympy import false
import pyautogui
import random
from logicc import canMoveDown, canMoveLeft, canMoveRight, canMoveUp, move_down,move_left,move_right,move_up,add_new_2,add_new_tile



class GameDriver:    
    def __init__(self):
        self.url = 'https://puzzle-2048.onrender.com/'
        self.PATH = 'C:/Program Files (x86)/chromedriver.exe'
        self.driver = webdriver.Chrome(self.PATH)
        self.driver.get(self.url)
        self.body = self.driver.find_element_by_tag_name('body')
        self.score = 0
        self.moves = {
            0: 'w',
            1: 's',
            2: 'a',
            3: 'd'
        }
    
    def getGrid(self):
        matrix = [[0 for i in range(4)] for j in range(4)]
        tiles = self.driver.find_elements_by_class_name('tile')
        for tile in tiles:       
            style = tile.get_attribute('style')
            col,row =  int(style[4]),int(style[11])
            num = int(tile.text)
            if num > matrix[row][col]:
                matrix[row][col] = num
        
        return matrix

    def close(self):
        self.driver.find_element_by_css_selector('main .btns:nth-child(6) button:first-child').click()
        time.sleep(0.11)
    
    def move(self, moveCode):
        self.body.send_keys(self.moves[moveCode])
        score = self.driver.find_element_by_css_selector('.score span:first-child')
        self.score = int(score.text[7:])
        time.sleep(0.01)

    def get_current_state(self):
        mat = self.getGrid()
        # for i in range(4):
        #     for j in range(4):
        #         if(mat[i][j]== 2048):
        #             return True

        for i in range(4):
            for j in range(4):
                if(mat[i][j]== 0):
                    return True

        for i in range(3):
            for j in range(3):
                if(mat[i][j]== mat[i + 1][j] or mat[i][j]== mat[i][j + 1]):
                    return True

        for j in range(3):
            if(mat[3][j]== mat[3][j + 1]):
                return True

        for i in range(3):
            if(mat[i][3]== mat[i + 1][3]):
                return True

        return False


def check_add_tiles(mat):
    lst = []
    for i in mat:
        for j in i:
            lst.append(str(j))
    if '0' in lst:
        return True
    return False


def monte_carlo(matrix,searches_per_move,search_length,node2,node3):
    moves = [move_up,move_down,move_left,move_right]
    can_move=[canMoveUp,canMoveDown,canMoveLeft,canMoveRight]
    scores = [0,0,0,0]
    
    for first_index in range(len(moves)):

        is_valid = can_move[first_index](matrix)
        print(is_valid)
        if is_valid:
            search_matrix ,is_valid,change = moves[first_index](matrix)
            search_matrix = add_new_tile(search_matrix)
            scores[first_index] += change
        else:
            continue
        
        for _ in range(searches_per_move):
            new_mat = np.copy(search_matrix)
            n=random.choice(moves)
            is_valid = can_move[moves.index(n)]
            if is_valid:
                new_mat,_,change = n(search_matrix)
                if check_add_tiles(new_mat):
                    new_mat = add_new_tile(new_mat)
                    scores[first_index] += change
                else:    
                    continue
            else:
                continue

            for _ in range(search_length):
                length_mat = np.copy(new_mat)
                n=random.choice(moves)
                is_valid = can_move[moves.index(n)]
                if is_valid:
                    length_mat,_,change = n(new_mat)
                    if check_add_tiles(length_mat):
                        length_mat = add_new_tile(length_mat)
                        scores[first_index] += change
                    else:
                        continue
                else:
                    continue
                for node2 in range(node2):
                    node2_mat = np.copy(length_mat)
                    node2_mat ,is_valid,change = random.choice(moves)(length_mat)
                    if is_valid:
                        if check_add_tiles(node2_mat):
                            node2_mat = add_new_tile(node2_mat)
                            scores[first_index] += change
                    else:
                        continue
                    for node3 in range(node3):
                        node3_mat = np.copy(node2_mat)
                        node3_mat,is_valid,change = random.choice(moves)(node2_mat)
                        if is_valid:
                            if check_add_tiles(node3_mat):
                                node3_mat = add_new_tile(node3_mat)
                                scores[first_index] += change
                        else:
                            continue
                #         for node4 in range(node4):
                #             node4_mat = np.copy(node3_mat)
                #             node4_mat,is_valid,change = random.choice(moves)(node3_mat)
                #             if is_valid:
                #                 # node3_mat = add_new_tile(node3_mat)
                #                 scores[first_index] += change
                #             else:
                #                 continue


    best_move = np.argmax(scores)
    return best_move


        
game = GameDriver()
inital_mat = 0
moves = ['move_up','move_down','move_left','move_right']

time.sleep(1)
while True:
    matrix = game.getGrid()
    index = monte_carlo(matrix,20,10,10,10)
    game.move(index)
    print(moves[index])

    if keyboard.is_pressed('control'):
        break
