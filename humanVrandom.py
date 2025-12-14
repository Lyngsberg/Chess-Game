import chess
import copy
import sys



board = chess.BoardHumanVRandom()

number_of_games = 1


for i in range(number_of_games):
    while True:
        # Checking for checkmate
        if board.turn == 'white':
            if board.is_checkmate():
                print("Black Won")
                break
        else:
            if board.is_checkmate():
                print("White Won")
                break
        if len(board.action_space()) == 0:
            print("Draw, nobody can move")
            break

        # Checking number of turns 
        if board.current_turn == board.max_turn:
            print("Draw, max turns reached")
            break

        #board.show_current_board()
        board.move()