import random
import json
import copy

# Defining board class
class BoardHumanVHuman():
    def __init__(self):


        self.current_turn = 0
        self.max_turn = 300

        self.turn = "white"

        self.none_piece = (0,0,3)

        self.black = 1
        self.white = 0

        self.pawn_value = 1
        self.pawn_sign = 'p'

        self.knight_value = 2
        self.knight_sign = 'kn'

        self.bishop_value = 2
        self.bishop_sign = 'b'

        self.rook_value = 5
        self.rook_sign = 'r'

        self.queen_value = 1
        self.queen_sign = 'q'

        self.king_value = 1
        self.king_sign = 'ki'

        self.white_pawn = (self.pawn_sign, self.pawn_value, self.white)
        self.black_pawn = (self.pawn_sign, self.pawn_value, self.black)
        
        self.white_knight = (self.knight_sign, self.knight_value, self.white)
        self.black_knight = (self.knight_sign, self.knight_value, self.black)

        self.white_bishop = (self.bishop_sign, self.bishop_value, self.white)
        self.black_bishop = (self.bishop_sign, self.bishop_value, self.black)

        self.white_rook = (self.rook_sign, self.rook_value, self.white)
        self.black_rook = (self.rook_sign, self.rook_value, self.black)

        self.white_queen = (self.queen_sign, self.queen_value, self.white)
        self.black_queen = (self.queen_sign, self.queen_value, self.black)

        self.white_king = (self.king_sign, self.king_value, self.white)
        self.black_king = (self.king_sign, self.king_value, self.black)

        self.game_board = self.make_board()
        self.future_board = self.game_board
        
    def make_board(self):
        self.game_board = [[self.none_piece for j in range(8)] for i in range(8)]
        for i in range(8):
            self.game_board[1][i] = self.white_pawn
            self.game_board[6][i] = self.black_pawn
            if i == 0 or  i == 7:
                self.game_board[0][i] = self.white_rook
                self.game_board[7][i] = self.black_rook
            if i == 1 or i == 6:
                self.game_board[0][i] = self.white_knight
                self.game_board[7][i] = self.black_knight
            if i == 2 or  i == 5:
                self.game_board[0][i] = self.white_bishop
                self.game_board[7][i] = self.black_bishop
            if i == 3:
                self.game_board[0][i] = self.white_queen
                self.game_board[7][i] = self.black_queen
            if i == 4:
                self.game_board[0][i] = self.white_king
                self.game_board[7][i] = self.black_king

        return self.game_board 

    def is_black_check(self) -> bool:
        # Finding Black king, White rooks, White Queen, White bishop and white knight
        rooks_pos = []
        bishop_pos = []
        queen_pos = []
        knight_pos = []
        for row in range(8):
            for column in range(8):
                if self.game_board[row][column] == self.black_king:
                    king_pos = (row,column)
                elif self.game_board[row][column] == self.white_rook:
                    rooks_pos.append((row,column))
                elif self.game_board[row][column] == self.white_queen:
                    queen_pos.append((row,column))
                elif self.game_board[row][column] == self.white_bishop:
                    bishop_pos.append((row,column))
                elif self.game_board[row][column] == self.white_knight:
                    knight_pos.append((row,column))

            
        for pos in rooks_pos:
            if self.is_on_line_and_free(current_row=king_pos[0], current_column=king_pos[1], 
                                        next_row=pos[0], next_column=pos[1]):
                return True
        for pos in bishop_pos:
            if self.is_on_diagonal_and_free(current_row=king_pos[0], current_column=king_pos[1], 
                                        next_row=pos[0], next_column=pos[1]):
                return True
        for pos in queen_pos:
            if self.is_on_line_and_free(current_row=king_pos[0], current_column=king_pos[1], 
                                        next_row=pos[0], next_column=pos[1]):
                return True
            if self.is_on_diagonal_and_free(current_row=king_pos[0], current_column=king_pos[1], 
                                        next_row=pos[0], next_column=pos[1]):
                return True


        # Checking white pawn move
        pawn_attack_offsets = [(-1, -1), (-1, 1)]  # pawns attack diagonally downward
        for dr, dc in pawn_attack_offsets:
            r, c = king_pos[0] + dr, king_pos[1] + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if self.game_board[r][c] == self.white_pawn:
                    return True
        
        # Checking for knights
        knights_check_pos = []
        # Down
        knights_check_pos.append((king_pos[0] -2,king_pos[1] -1)) 
        knights_check_pos.append((king_pos[0] -2, king_pos[1] +1))
        
        # Left 
        knights_check_pos.append((king_pos[0] - 1, king_pos[1] -2))
        knights_check_pos.append((king_pos[0] + 1, king_pos[1] -2))

        # Up
        knights_check_pos.append((king_pos[0] + 2, king_pos[1] -1))
        knights_check_pos.append((king_pos[0] + 2, king_pos[1] +1))

        # Right
        knights_check_pos.append((king_pos[0] + 1, king_pos[1] +2))
        knights_check_pos.append((king_pos[0] - 1, king_pos[1] +2))
    
        for i in knight_pos:
            if i in knights_check_pos:
                return True
        return False

    def blank_board(self):
        self.game_board = [[self.none_piece for j in range(8)] for i in range(8)]

    def is_white_check(self) -> bool:
        # Finding White king, Black rooks, Black Queen, Black bishop and black knight
        rooks_pos = []
        bishop_pos = []
        queen_pos = []
        knight_pos = []
        for row in range(8):
            for column in range(8):

                if self.game_board[row][column] == self.white_king:
                    king_pos = (row,column)
                elif self.game_board[row][column] == self.black_rook:
                    rooks_pos.append((row,column))
                elif self.game_board[row][column] == self.black_queen:
                    queen_pos.append((row,column))
                elif self.game_board[row][column] == self.black_bishop:
                    bishop_pos.append((row,column))
                elif self.game_board[row][column] == self.black_knight:
                    knight_pos.append((row,column))

        for pos in rooks_pos:
            if self.is_on_line_and_free(current_row=king_pos[0], current_column=king_pos[1], 
                                        next_row=pos[0], next_column=pos[1]):
                return True
        for pos in bishop_pos:
            if self.is_on_diagonal_and_free(current_row=king_pos[0], current_column=king_pos[1], 
                                        next_row=pos[0], next_column=pos[1]):
                return True
        for pos in queen_pos:
            if self.is_on_line_and_free(current_row=king_pos[0], current_column=king_pos[1], 
                                        next_row=pos[0], next_column=pos[1]):
                return True
            if self.is_on_diagonal_and_free(current_row=king_pos[0], current_column=king_pos[1], 
                                        next_row=pos[0], next_column=pos[1]):
                return True


        # Checking for pawns
        pawn_attack_offsets = [(1, -1), (1, 1)]
        for dr, dc in pawn_attack_offsets:
            r, c = king_pos[0] + dr, king_pos[1] + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if self.game_board[r][c] == self.black_pawn:
                    return True
        
        # Checking for knights
        knights_check_pos = []
        # Down
        knights_check_pos.append((king_pos[0] -2,king_pos[1] -1)) 
        knights_check_pos.append((king_pos[0] -2, king_pos[1] +1))
        
        # Left 
        knights_check_pos.append((king_pos[0] - 1, king_pos[1] -2))
        knights_check_pos.append((king_pos[0] + 1, king_pos[1] -2))

        # Up
        knights_check_pos.append((king_pos[0] + 2, king_pos[1] -1))
        knights_check_pos.append((king_pos[0] + 2, king_pos[1] +1))

        # Right
        knights_check_pos.append((king_pos[0] + 1, king_pos[1] +2))
        knights_check_pos.append((king_pos[0] - 1, king_pos[1] +2))
    
        for i in knight_pos:
            if i in knights_check_pos:
                return True
        return False

    def is_free(self, next_row, next_column):
        if self.game_board[next_row][next_column] == self.none_piece:
            return True
        else:
            return False

    def is_kings_in_proximity(self, next_row, next_column) -> bool:
        # Locating Kings
        for row in range(8):
            for column in range(8):
                if self.game_board[row][column] == self.white_king:
                    white_pos = (row, column)
                if self.game_board[row][column] == self.black_king:
                    black_pos = (row, column)
        if self.turn == "white":
            white_pos = (next_row, next_column)
        else:
            black_pos = (next_row, next_column)


        # Checking proximity
        # Corners
        if ((abs(white_pos[0] - black_pos[0]) == 1) and (abs(white_pos[1] - black_pos[1]) == 1)):
            return True
        # Middle (left and right)
        if ((abs(white_pos[0] - black_pos[0]) == 0) and (abs(white_pos[1] - black_pos[1]) == 1)):
            return True
        # Middle (up and down)
        if ((abs(white_pos[0] - black_pos[0]) == 1) and (abs(white_pos[1] - black_pos[1]) == 0)):
            return True
        return False

    def is_on_diagonal_and_free(self, current_row, current_column, next_row, next_column) -> bool:
        """
        Checks if diagonal is free. If the last position is not own piece it still return True.
        """
        set_of_moves = []
        valid_moves = []
        next_position = (next_row, next_column)
        # Checks for on diagonal
        if (abs(next_row - current_row) == abs(next_column - current_column)) == False:
            return False

        
        # Upper left
        if (next_row > current_row and current_column > next_column):
            for i in range(1,8):
                
                set_of_moves.append((current_row + i, current_column -i ))

        # Lower left
        elif (next_row < current_row and current_column > next_column):
            for i in range(1,8):
                set_of_moves.append((current_row - i, current_column - i))

        # Upper right
        elif (next_row > current_row and current_column < next_column):
            for i in range(1,8):
                set_of_moves.append((current_row + i, current_column + i))
        
        # Lower right
        else:
            for i in range(1,8):
                set_of_moves.append((current_row - i, current_column + i))

        # Checking if next move is on diagonal
        if next_position not in set_of_moves:
            return False

        # Sorting the set_of_moves to only be on the board
        for i in range(len(set_of_moves)):
            # Selecting only moves that is on the board
            if ((set_of_moves[i][0] >= 0 and set_of_moves[i][0] < 8)
                 and (set_of_moves[i][1] >= 0 and set_of_moves[i][1] < 8)):
                valid_moves.append(set_of_moves[i])
                # Selecting only upto the selected end position
                if (set_of_moves[i][0] == next_position[0]
                    and set_of_moves[i][1] == next_position[1]):
                    break
        # Checks if the diag but not the end point is free
        for valid_move in valid_moves[:-1]:
            if self.is_free(next_row = valid_move[0], next_column = valid_move[1]) == False:
                return False       
        
        # Checking if line is free and if the end placement is not own piece
        for i, move in enumerate(valid_moves):
            if i == len(valid_moves) -1:
                if self.turn == 'white':
                    if (self.game_board[move[0]][move[1]][2] == self.white):
                        return False
                else:
                    if (self.game_board[move[0]][move[1]][2] == self.black):
                        return False
            # Checks if the diagonal is free
            elif self.is_free(next_row = move[0], next_column = move[1]) == False:
                return False

        # if it got to this point it is both on a diagonal and all the diags is free
        return True


    def is_on_line_and_free(self, current_row: int, current_column: int, next_row: int, next_column: int) -> bool:
        """Checks if on line. If end position is not own piece it still return True.
        The set of moves does not include the ending square, that is checked down below"""

        set_of_moves = []
        # Checks if on line 
        if ((current_column != next_column) and (current_row != next_row)):
            return False
        
        # To the left
        if current_row == next_row and current_column > next_column:
            for i in range(current_column-1, next_column, -1):

                set_of_moves.append((current_row, i))
        
        # To the right
        elif current_row == next_row and current_column < next_column:
            for i in range(current_column+1, next_column):
                set_of_moves.append((current_row, i))
        
        # Up
        elif current_column == next_column and next_row > current_row:
            for i in range(current_row+1, next_row):
                set_of_moves.append((i, current_column))

        
        # Down
        else:
            for i in range(current_row-1, next_row, -1):
                set_of_moves.append((i, current_column))


        # Checking of line is free (execpt last position)
        for move in set_of_moves:
            if self.is_free(next_row= move[0], next_column= move[1]) == False:
                return False
        # Checking if last position is own piece
        if self.turn == 'white':
            if self.game_board[next_row][next_column][2] == self.white:
                return False
        else:
            if self.game_board[next_row][next_column][2] == self.black:
                return False
        # Reaching this point means that it is on line and line is free
        return True

    def print_board(self):
        cell_width = 6
        columns = [str(i) for i in range(8)]

        print("  " + "-" * (len(columns) * (cell_width + 3) - 1))  # top border

        for i, row in enumerate(reversed(self.game_board)):
            row_str = f"{7-i} |"
            for piece in row:
                if isinstance(piece, tuple) and piece[0] != 0:
                    sign = piece[0]
                    color = 'w' if piece[2] == 0 else 'b'
                    piece_str = f"{sign}_{color}"
                    row_str += f" {piece_str:^{cell_width}} |"
                else:
                    row_str += f" {'X':^{cell_width}} |"
            print(row_str)
            print("  " + "-" * (len(columns) * (cell_width + 3) - 1))

        # Print column headers centered in cell_width spaces at bottom
        print("    " + " | ".join(col.center(cell_width) for col in columns))

        

    def is_input_inbounds(self, current_row: int, current_column: int, next_row: int, next_column: int) -> bool:
        # Checking for bounds of chess board

        if ((current_column >= 0 and current_column < 8) and (current_row >= 0 and current_row < 8)
            and (next_column >= 0 and next_column < 8) and (next_row >= 0 and next_column <8)
            and (current_column, current_row) != (next_column,next_row)):
            return True
        return False

    def is_input_int(self, current_row: int, current_column: int, next_row: int, next_column: int) -> bool:
        # Checking input is integers
        if (current_row.isdigit() and current_column.isdigit()
            and next_row.isdigit() and next_column.isdigit()):
            return True
        else:
            return False


    def is_pawn_move_legal(self, current_row: int, current_column: int, next_row: int, next_column: int) -> bool:
        if self.turn == "white":
            # move 2 in the beginning
            if (((current_row == 1) and (next_row == 3)) and (current_column == next_column)
                 and (self.is_free(next_row=next_row, next_column=next_column)) 
                 and (self.is_free(next_row=next_row -1, next_column=next_column))):
                return True
            # Move 1 up
            elif ((current_row - next_row == -1) and (current_column == next_column) 
                  and self.is_free(next_row=next_row, next_column=next_column)):
                return True
            # Attack
            elif ((current_row - next_row == -1) and (abs(current_column - next_column) == 1)
                   and (self.game_board[next_row][next_column][2] == self.black)):
                return True
        # If black
        else:
            # Move 2 in the beginning
            if (((current_row == 6) and (next_row == 4)) and (current_column == next_column)
                 and (self.is_free(next_row=next_row, next_column=next_column)) 
                 and (self.is_free(next_row=next_row +1, next_column=next_column))):
                return True
            # Move 1 up
            elif ((current_row - next_row == 1) and (current_column == next_column) 
                  and self.is_free(next_row=next_row, next_column=next_column)):
                return True
            # Attack
            elif ((current_row - next_row == 1) and (abs(current_column - next_column) == 1)
                   and (self.game_board[next_row][next_column][2] == self.white)):
                return True       
        return False     

    def is_knight_move_legal(self, current_row: int, current_column: int, next_row: int, next_column: int) -> bool:
        
        if self.turn == 'white':
            # Jumps 2 up or down
            if (abs(current_row - next_row) == 2 and (abs(current_column - next_column) == 1)):
                return True
            # Jumps 2 to the left or right
            if (abs(current_row - next_row) == 1 and (abs(current_column - next_column) == 2)
                and self.game_board[next_row][next_column][2] != self.white):
                return True
        else:
            # Jumps 2 up or down
            if (abs(current_row - next_row) == 2 and (abs(current_column - next_column) == 1)):
                return True
            # Jumps 2 to the left or right
            if (abs(current_row - next_row) == 1 and (abs(current_column - next_column) == 2)
                and self.game_board[next_row][next_column][2] != self.black):
                return True
        return False

    def is_king_move_legal(self, current_row: int, current_column: int, next_row: int, next_column: int) -> bool:
        if self.turn == 'white':
            # Checking for correct movement
            if not (abs(current_row - next_row) in [0, 1] and abs(current_column - next_column) in [0, 1]):
                return False
            # Checking not own piece
            if (self.game_board[next_row][next_column][2] == self.white):
                return False
            # Checking king proximity
            if (self.is_kings_in_proximity(next_row= next_row, next_column=next_column) == True):
                return False 
            
        else:
            # Checking for correct movement
            if not (abs(current_row - next_row) in [0, 1] and abs(current_column - next_column) in [0, 1]):
                return False
            # Checking not own piece
            if (self.game_board[next_row][next_column][2] == self.black):
                return False
            # Checking king proximity
            if (self.is_kings_in_proximity(next_row= next_row, next_column=next_column) == True):
                return False 
        


    def is_move_valid(self, current_row: int, current_column: int, next_row: int, next_column: int) -> bool:
        # Checks if startposition is own piece
        if self.turn == "white":
            if self.game_board[current_row][current_column][2] != self.white:
                return False
        else:
            if self.game_board[current_row][current_column][2] != self.black:
                return False

        # Checks if end position is own piece
        if self.turn == "white":
            if self.game_board[next_row][next_column][2] == self.white:
                return False
        else:
            if self.game_board[next_row][next_column][2] == self.black:
                return False

        # If check, checks if move unchecks
        if self.turn == "white":
            if self.is_white_check():
                # copies current state 
                new_game = copy.deepcopy(self)
                current_piece = new_game.game_board[current_row][current_column]
                new_game.game_board[next_row][next_column] = current_piece
                new_game.game_board[current_row][current_column] = self.none_piece
                if new_game.is_white_check():
                    return False
        else:
            if self.is_black_check():
                # copies current state
                new_game = copy.deepcopy(self)
                current_piece = new_game.game_board[current_row][current_column]
                new_game.game_board[next_row][next_column] = current_piece
                new_game.game_board[current_row][current_column] = self.none_piece
                if new_game.is_black_check():
                    return False

        # Checks pawn movement
        if (self.game_board[current_row][current_column][0] == self.pawn_sign):
            if (self.is_pawn_move_legal(current_row= current_row, current_column= current_column, 
                             next_row= next_row, next_column= next_column)) == False:
                return False
        # Check knight movement
        elif (self.game_board[current_row][current_column][0] == self.knight_sign):
            if (self.is_knight_move_legal(current_row= current_row, current_column= current_column, 
                             next_row= next_row, next_column= next_column)) == False:
                return False
        # Check bishop movement
        elif (self.game_board[current_row][current_column][0] == self.bishop_sign):
            if (self.is_on_diagonal_and_free(current_row= current_row, current_column= current_column, 
                             next_row= next_row, next_column= next_column)) == False:
                return False
                
        # Check rook movement 
        elif (self.game_board[current_row][current_column][0] == self.rook_sign):
            if (self.is_on_line_and_free(current_row= current_row, current_column= current_column, 
                             next_row= next_row, next_column= next_column)) == False:
                return False
        
        # Check Queen movemet
        elif (self.game_board[current_row][current_column][0] == self.queen_sign):
            if (((self.is_on_diagonal_and_free(current_row= current_row, current_column= current_column, 
                             next_row= next_row, next_column= next_column)) == False) 
                            and (self.is_on_line_and_free(current_row= current_row, current_column= current_column, 
                             next_row= next_row, next_column= next_column) == False)):
                return False
        # Check King movement 
        elif (self.game_board[current_row][current_column][0] == self.king_sign):
            if (self.is_king_move_legal(current_row= current_row, current_column= current_column, 
                             next_row= next_row, next_column= next_column) == False):
                return False
            
        # Checking if move makes own king check
        if self.turn == 'white':
            new_game = copy.deepcopy(self)
            current_piece = new_game.game_board[current_row][current_column]
            new_game.game_board[next_row][next_column] = current_piece
            new_game.game_board[current_row][current_column] = self.none_piece
            if new_game.is_white_check():
                return False
        else:
            new_game = copy.deepcopy(self)
            current_board = new_game.game_board
            current_piece = new_game.game_board[current_row][current_column]
            new_game.game_board[next_row][next_column] = current_piece
            new_game.game_board[current_row][current_column] = self.none_piece
            if new_game.is_black_check():
                return False
        # Getting at this point means the move is valid
        return True
        
    def action_space(self):
        all_moves = []

        for row in range(8):
            for col in range(8):
                for next_row in range(8):
                    for next_col in range(8):
                        if (row, col) == (next_row, next_col):
                            continue  # Skip moves to the same square

                        if self.is_move_valid(
                            current_row=row, current_column=col,
                            next_row=next_row, next_column=next_col
                        ):
                            all_moves.append((row, col, next_row, next_col))

        return all_moves


    def is_checkmate(self):
        if self.turn == "white":
            return (len(self.action_space()) == 0 and self.is_white_check())
        else:
            return (len(self.action_space()) == 0 and self.is_black_check())

    def change_turn(self) -> None:
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    def random_action(self):
        current_action_space = self.action_space()
        if  len(current_action_space) == 0:
            print(f"Action space has length 0 so there must be either a mate or a draw")
            print(f"Turn: {self.turn}")
            self.print_board()

        return current_action_space[max(random.randint(0, len(current_action_space)-1),0)]
    
    def make_board_from_json(self, json_data):
        self.game_board = json.loads(json_data)

    def is_game_drawn(self):
        if self.current_turn >= self.max_turn:
            return True
        elif len(self.action_space()) == 0:
            return True
        elif any(row for row in self.game_board[0]):
            True
        return False

    def set_board(self, dict):
        for row in range(8):
            for column in range(8):
                self.game_board[row][column] = tuple(dict["game_board"][row][column])
    
    def move(self):
        while True:
            user_input = input(f"{(self.turn.upper())} to move: ")
            if user_input == '':
                print('Move cannot be empty')
                continue

            user_input = user_input.split()
            if len(user_input) != 4:
                print("Must be 4 numbers")
                continue
            
            current_row, current_column, next_row, next_column = user_input
            if self.is_input_int(current_row= current_row, current_column= current_column, 
                             next_row= next_row, next_column= next_column):
                current_row = int(current_row)
                current_column = int(current_column)
                next_row = int(next_row)
                next_column = int(next_column)
            else:
                print("Input is not integer")
                continue
            if self.is_input_inbounds(current_row= current_row, current_column= current_column, 
                             next_row= next_row, next_column= next_column) == False:
                print("Input is not inbound")
                continue
            if self.is_move_valid(current_row= current_row, current_column= current_column, 
                             next_row= next_row, next_column= next_column) == False:
                print("Input is not valid")
                continue
            break

        current_piece = self.game_board[current_row][current_column]
        self.game_board[current_row][current_column] = self.none_piece

        # Promoting pawn
        # White
        if (current_piece == self.white_pawn and next_row == 7):
            current_piece = self.white_queen
        # Black
        elif (current_piece == self.black_pawn and next_row == 0):
            current_piece = self.black_queen

        self.game_board[next_row][next_column] = current_piece

            

        self.change_turn()
        self.current_turn += 1

    def move_api(self, current_row, current_column, next_row, next_column):
        if current_row not in [0,1,2,3,4,5,6,7]:
            return 1
        if current_column not in [0,1,2,3,4,5,6,7]:
            return 1
        if next_row not in [0,1,2,3,4,5,6,7]:
            return 1
        if next_column not in [0,1,2,3,4,5,6,7]:
            return 1
        if (current_row, current_column) == (next_row, next_column):
            return 1
        
        if self.is_move_valid(current_row, current_column, next_row, next_column) == False:
            return 2

        current_piece = self.game_board[current_row][current_column]

        # Promoting pawn
        # White
        if (current_piece == self.white_pawn and next_row == 7):
            current_piece = self.white_queen
        # Black
        elif (current_piece == self.black_pawn and next_row == 0):
            current_piece = self.black_queen

        self.game_board[current_row][current_column] = self.none_piece
        self.game_board[next_row][next_column] = current_piece


        self.change_turn()
        self.current_turn += 1
        return 0

class BoardHumanVRandom(BoardHumanVHuman):
    def move(self):
        if self.turn != "white":
            current_row, current_column, next_row, next_column = self.random_action()
        else:
            while True:
                user_input = input(f"{(self.turn.upper())} to move: ")
                if user_input == '':
                    print('Move cannot be empty')
                    continue

                user_input = user_input.split()
                if len(user_input) != 4:
                    print("Must be 4 numbers")
                    continue
                

                current_row, current_column, next_row, next_column = user_input
                if self.is_input_int(current_row= current_row, current_column= current_column, 
                                next_row= next_row, next_column= next_column):
                    current_row = int(current_row)
                    current_column = int(current_column)
                    next_row = int(next_row)
                    next_column = int(next_column)
                else:
                    print("Input is not integer")
                    continue
                if self.is_input_inbounds(current_row= current_row, current_column= current_column, 
                                next_row= next_row, next_column= next_column) == False:
                    print("Input is not inbound")
                    continue
                if self.is_move_valid(current_row= current_row, current_column= current_column, 
                                next_row= next_row, next_column= next_column) == False:
                    print("Input is not valid")
                    continue
                break

        current_piece = self.game_board[current_row][current_column]

        # Promoting pawn
        # White
        if (current_piece == self.white_pawn and next_row == 7):
            current_piece = self.white_queen
        # Black
        elif (current_piece == self.black_pawn and next_row == 0):
            current_piece = self.black_queen

        self.game_board[current_row][current_column] = self.none_piece
        self.game_board[next_row][next_column] = current_piece


        self.change_turn()
        self.current_turn += 1

class RandomVRandom(BoardHumanVHuman):
    def move(self):
        current_row, current_column, next_row, next_column = self.random_action()
        current_piece = self.game_board[current_row][current_column]

        # Promoting pawn
        # White
        if (current_piece == self.white_pawn and next_row == 7):
            current_piece = self.white_queen
        # Black
        elif (current_piece == self.black_pawn and next_row == 0):
            current_piece = self.black_queen

        self.game_board[current_row][current_column] = self.none_piece
        self.game_board[next_row][next_column] = current_piece
        self.change_turn()
        self.current_turn += 1
        return (current_row, current_column, next_row, next_column)


    def manual_move(self, current_row, current_column, next_row, next_column):

        current_piece = self.game_board[current_row][current_column]

        # Promoting pawn
        # White
        if (current_piece == self.white_pawn and next_row == 7):
            current_piece = self.white_queen
        # Black
        elif (current_piece == self.black_pawn and next_row == 0):
            current_piece = self.black_queen

        self.game_board[next_row][next_column] = current_piece
        self.game_board[current_row][current_column] = self.none_piece
        self.change_turn() 
        self.current_turn +=1 


class AIVMCTS(BoardHumanVHuman):
    def __init__(self, depth, width):
        """Monte Carlo Tree Search in this version is always for black"""
        super().__init__()
        self.depth = depth
        self.width = width

    def get_score(self) -> int:
        score = 0
        if self.turn == "white":
            for row in range(8):
                for column in range(8):
                    if self.game_board[row][column][2] == self.black:
                        score += self.game_board[row][column][1]
        return score

    def random_move(self):
        current_row, current_column, next_row, next_column = self.random_action()
        current_piece = self.game_board[current_row][current_column]

        # Promoting pawn
        # White
        if (current_piece == self.white_pawn and next_row == 7):
            current_piece = self.white_queen
        # Black
        elif (current_piece == self.black_pawn and next_row == 0):
            current_piece = self.black_queen

        self.game_board[current_row][current_column] = self.none_piece
        self.game_board[next_row][next_column] = current_piece
        self.change_turn()
        self.current_turn += 1

    def manual_move(self, current_row, current_column, next_row, next_column):

        current_piece = self.game_board[current_row][current_column]

        # Promoting pawn
        # White
        if (current_piece == self.white_pawn and next_row == 7):
            current_piece = self.white_queen
        # Black
        elif (current_piece == self.black_pawn and next_row == 0):
            current_piece = self.black_queen

        self.game_board[next_row][next_column] = current_piece
        self.game_board[current_row][current_column] = self.none_piece
        self.change_turn() 
        self.current_turn +=1 

    def MCTS(self) -> tuple:
        # Works for both colours
        best_score_init = -999999
        best_move = -9999
        best_score = best_score_init

        for _ in range(self.width):
            # Reseting the game after each width
            MCTS_game = copy.deepcopy(self)

            # Monte Carlo Tree Seach black
            base_action = MCTS_game.random_action()
            MCTS_game.manual_move(base_action[0], base_action[1], base_action[2], base_action[3])

            # Checking if first move leads to checkmate
            if MCTS_game.is_checkmate():
                return base_action
            # Checking if no move is avaliable (Draw)
            if len(MCTS_game.action_space()) == 0:
                continue
            
            # Now white random move
            MCTS_game.random_move()

            # Checks if this leads to black checkmate
            if MCTS_game.is_checkmate():
                continue
            # Checking if no move is avaliable (Draw)
            if len(MCTS_game.action_space()) == 0:
                continue

            for _ in range(self.depth):
                # Monte Carlo Tree Search black again
                MCTS_game.random_move()

                if MCTS_game.is_checkmate():
                    return base_action
                # Checking if no move is avaliable (Draw)
                if len(MCTS_game.action_space()) == 0:
                    continue

                # White random move
                MCTS_game.random_move()

                if MCTS_game.is_checkmate():
                    break
                # Checking if no move is avaliable (Draw)
                if len(MCTS_game.action_space()) == 0:
                    continue


            score = MCTS_game.get_score()
            if score > best_score:
                best_score = score
                best_move = base_action

        # if all depths and widths leads to checkmate
        if best_score == best_score_init:
            return self.random_action()
        return best_move


        




       

