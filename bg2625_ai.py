#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to  
complete and submit. 

@author: Bhaskar Ghosh UNI: bg2625
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move
import math
import sys
from heapq import heappush

player1_cache = {}
player2_cache = {}
caching_states = {}

def compute_utility(board, color):
    """
    Return the utility of the given board state
    (represented as a tuple of tuples) from the perspective
    of the player "color" (1 for dark, 2 for light)
    """
    player1_score = 0
    player2_score = 0

    score = get_score(board)
    if color == 1:
        return  score[0] - score[1]
    else:
        return  score[1] - score[0]

############ MINIMAX ###############################

def minimax_min_node(board, color):

    sys.setrecursionlimit(100000)

    utility = math.inf

    # get possible moves.
    possible_moves = get_possible_moves(board, color)

    best_utility = math.inf
    max_color = 1 if color == 2 else 2
    if len(possible_moves) > 0:
        sorted_states_list = []
        # Sorting successor states as per their utility values
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])
            sort_utility = compute_utility(new_board, color)
            heappush(sorted_states_list, (sort_utility, new_board))

        # getting sorted states from list of tuples
        sorted_states = [x[1] for x in sorted_states_list]

        # iterating over sorted_states
        for board_state in sorted_states:

            if board_state in caching_states:
                best_utility = caching_states[board_state]
            else:
                best_utility = min(best_utility, minimax_max_node(board_state, max_color))
                caching_states[board_state] = best_utility

    else:
        orig_color = 1 if color == 2 else 2
        best_utility = compute_utility(board, orig_color)

    return best_utility


def minimax_max_node(board, color):

    sys.setrecursionlimit(100000)

    best_utility = -math.inf
    min_color = 1 if color == 2 else 2
    # get possible moves. If result set is empty return None
    possible_moves = get_possible_moves(board, color)

    if len(possible_moves) > 0:

        sorted_states_list = []
        # Sorting successors
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])
            sort_utility = compute_utility(new_board, color)
            heappush(sorted_states_list, (-sort_utility, new_board))


        # get states from sorted states
        sorted_states = [x[1] for x in sorted_states_list]
        # Iterate over sorted states
        for board_state in sorted_states:

            if board_state in caching_states:
                best_utility = caching_states[board_state]
            else:
                best_utility = max(best_utility, minimax_min_node(board_state, min_color))
                caching_states[board_state] = best_utility

    else:
        orig_color = 1 if color == 2 else 2
        best_utility = compute_utility(board, orig_color)

    return best_utility

    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """
    best_utility = -math.inf
    new_color = 1 if color == 2 else 2
    possible_moves = get_possible_moves(board, color)
    best_move = 0,0
    if len(possible_moves) > 0:
        best_move = possible_moves[0]
        sorted_states_list = []
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])
            sort_utility = compute_utility(new_board, color)
            heappush(sorted_states_list, (sort_utility, new_board, move))

        sorted_states = [x[1] for x in sorted_states_list]
        moves = [x[2] for x in sorted_states_list]
        index = 0
        for board_state in sorted_states:
            if board_state in caching_states:

                utility = caching_states[board_state]
            else:
                utility = minimax_min_node(board_state, new_color)
                caching_states[board_state] = utility

            if utility > best_utility:
                best_move = moves[index]
                best_utility = utility
            index += 1

    return best_move



############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, level, limit):

    if level == limit:
        return compute_utility(board, color)

    # caching_states = get_cached_states(color)
    utility = math.inf
    possible_moves = get_possible_moves(board, color)
    min_color = 1 if color == 2 else 2
    if len(possible_moves) > 0:
        sorted_states_list = []
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])
            sort_utility = compute_utility(new_board, min_color)
            heappush(sorted_states_list, (sort_utility, new_board))

        sorted_states = [x[1] for x in sorted_states_list]
        for board_state in sorted_states:
            if board_state in caching_states:
                utility = caching_states[board_state]
            else:
                utility = min(utility, alphabeta_max_node(board_state, min_color, alpha, beta, level + 1, limit))
                caching_states[board_state] = utility

            if utility <= alpha:
                return utility
            beta = min(beta, utility)

    else:
        orig_color = 1 if color == 2 else 2
        utility = compute_utility(board, color)

    return utility


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, level, limit):

    if level == limit:
        return compute_utility(board, color)

    # caching_states = get_cached_states(color)
    utility = -math.inf
    possible_moves = get_possible_moves(board, color)
    max_color = 1 if color == 2 else 2
    if len(possible_moves) > 0:
        sorted_states_list = []
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])
            sort_utility = compute_utility(new_board, max_color)
            heappush(sorted_states_list, (-sort_utility, new_board))

        sorted_states = [x[1] for x in sorted_states_list]

        for board_state in sorted_states:
            if board_state in caching_states:
                utility = caching_states[board_state]
            else:
                utility = max(utility, alphabeta_min_node(board_state, max_color, alpha, beta, level + 1, limit))
                caching_states[board_state] = utility

            if utility >= beta:
                return utility
            alpha = max(alpha, utility)
    else:
        orig_color = 1 if color == 2 else 2
        utility = compute_utility(board, orig_color)

    return utility


def select_move_alphabeta(board, color):

    best_utility = -math.inf
    beta = math.inf
    best_move = 0, 0
    new_color = 1 if color == 2 else 2
    # caching_states = get_cached_states(color)
    possible_moves = get_possible_moves(board, color)
    level = 0
    limit = 5
    if len(possible_moves) > 0:
        sorted_states_list = []
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])
            sort_utility = compute_utility(new_board, new_color)
            heappush(sorted_states_list, (sort_utility, new_board, move))

        sorted_states = [x[1] for x in sorted_states_list]
        moves = [x[2] for x in sorted_states_list]
        index = 0
        for board_state in sorted_states:
            if board_state in caching_states:
                utility = caching_states[board_state]
            else:
                utility = alphabeta_min_node(board_state, new_color, best_utility, beta, level + 1, limit)
                caching_states[board_state] = utility
            if utility > best_utility:
                best_utility = utility
                best_move = moves[index]
            index += 1
        """
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])
            if new_board in caching_states:
                utility = caching_states[new_board]
            else:
                utility = alphabeta_min_node(new_board, new_color, best_utility, beta, level + 1, limit)
                caching_states[new_board] = utility
            if utility > best_utility:
                best_utility = utility
                best_move = move
        """
    return best_move

####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)


        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager
            movei, movej = select_move_minimax(board, color)
            # movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
