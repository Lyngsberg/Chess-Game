"""Chess game logic and state management."""
from chess.board import Board


class ChessGame:
    """Manages chess game state and rules."""
    
    def __init__(self):
        self.board = Board()
        self.current_player = 'white'
        self.game_over = False
        self.winner = None
        self.selected_piece = None
        self.valid_moves = []
        self.move_history = []
        
    def select_piece(self, position):
        """Select a piece at the given position."""
        piece = self.board.get_piece(position)
        
        if piece is None or piece.color != self.current_player:
            self.selected_piece = None
            self.valid_moves = []
            return False
            
        self.selected_piece = piece
        self.valid_moves = self.get_legal_moves(piece)
        return True
        
    def get_legal_moves(self, piece):
        """Get all legal moves for a piece (considering check)."""
        possible_moves = piece.get_possible_moves(self.board)
        legal_moves = []
        
        for move in possible_moves:
            if self.is_move_legal(piece.position, move):
                legal_moves.append(move)
                
        return legal_moves
        
    def is_move_legal(self, from_pos, to_pos):
        """Check if a move is legal (doesn't leave king in check)."""
        # Create a copy of the board to test the move
        test_board = self.board.copy()
        test_board.move_piece(from_pos, to_pos)
        
        # Check if our king would be in check after the move
        return not test_board.is_in_check(self.current_player)
        
    def make_move(self, from_pos, to_pos):
        """Attempt to make a move."""
        piece = self.board.get_piece(from_pos)
        
        if piece is None or piece.color != self.current_player:
            return False
            
        if not self.is_move_legal(from_pos, to_pos):
            return False
            
        # Make the move
        self.board.move_piece(from_pos, to_pos)
        self.move_history.append((from_pos, to_pos, piece.__class__.__name__))
        
        # Check for pawn promotion
        if piece.__class__.__name__ == 'Pawn':
            if (piece.color == 'white' and to_pos[0] == 0) or \
               (piece.color == 'black' and to_pos[0] == 7):
                self.promote_pawn(to_pos)
        
        # Switch players
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        # Check for game over conditions
        self.check_game_over()
        
        self.selected_piece = None
        self.valid_moves = []
        
        return True
        
    def promote_pawn(self, position):
        """Promote a pawn to a queen (simplified - always promote to queen)."""
        from chess.piece import Queen
        piece = self.board.get_piece(position)
        if piece:
            new_queen = Queen(piece.color, position)
            new_queen.has_moved = True
            row, col = position
            self.board.grid[row][col] = new_queen
            
    def check_game_over(self):
        """Check if the game is over (checkmate or stalemate)."""
        # Get all legal moves for current player
        all_pieces = self.board.get_all_pieces(self.current_player)
        has_legal_moves = False
        
        for piece in all_pieces:
            if self.get_legal_moves(piece):
                has_legal_moves = True
                break
        
        if not has_legal_moves:
            self.game_over = True
            if self.board.is_in_check(self.current_player):
                # Checkmate
                self.winner = 'black' if self.current_player == 'white' else 'white'
            else:
                # Stalemate
                self.winner = None
                
    def is_check(self):
        """Check if current player is in check."""
        return self.board.is_in_check(self.current_player)
        
    def get_game_status(self):
        """Get current game status as a string."""
        if self.game_over:
            if self.winner:
                return f"Checkmate! {self.winner.capitalize()} wins!"
            else:
                return "Stalemate! Game is a draw."
        elif self.is_check():
            return f"Check! {self.current_player.capitalize()}'s turn."
        else:
            return f"{self.current_player.capitalize()}'s turn."
