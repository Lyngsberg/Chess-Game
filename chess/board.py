"""Chess board representation and management."""
from chess.piece import Pawn, Knight, Bishop, Rook, Queen, King


class Board:
    """Represents the chess board and piece positions."""
    
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.captured_pieces = {'white': [], 'black': []}
        self.setup_initial_position()
        
    def setup_initial_position(self):
        """Set up the standard starting position for chess."""
        # Black pieces (row 0 and 1)
        self.grid[0][0] = Rook('black', (0, 0))
        self.grid[0][1] = Knight('black', (0, 1))
        self.grid[0][2] = Bishop('black', (0, 2))
        self.grid[0][3] = Queen('black', (0, 3))
        self.grid[0][4] = King('black', (0, 4))
        self.grid[0][5] = Bishop('black', (0, 5))
        self.grid[0][6] = Knight('black', (0, 6))
        self.grid[0][7] = Rook('black', (0, 7))
        
        for col in range(8):
            self.grid[1][col] = Pawn('black', (1, col))
        
        # White pieces (row 6 and 7)
        for col in range(8):
            self.grid[6][col] = Pawn('white', (6, col))
            
        self.grid[7][0] = Rook('white', (7, 0))
        self.grid[7][1] = Knight('white', (7, 1))
        self.grid[7][2] = Bishop('white', (7, 2))
        self.grid[7][3] = Queen('white', (7, 3))
        self.grid[7][4] = King('white', (7, 4))
        self.grid[7][5] = Bishop('white', (7, 5))
        self.grid[7][6] = Knight('white', (7, 6))
        self.grid[7][7] = Rook('white', (7, 7))
        
    def is_valid_position(self, position):
        """Check if position is within board bounds."""
        row, col = position
        return 0 <= row < 8 and 0 <= col < 8
        
    def get_piece(self, position):
        """Get piece at given position."""
        if not self.is_valid_position(position):
            return None
        row, col = position
        return self.grid[row][col]
        
    def move_piece(self, from_pos, to_pos):
        """Move piece from one position to another."""
        piece = self.get_piece(from_pos)
        if piece is None:
            return False
            
        # Capture if there's a piece at target
        target = self.get_piece(to_pos)
        if target:
            self.captured_pieces[target.color].append(target)
            
        # Move the piece
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        self.grid[to_row][to_col] = piece
        self.grid[from_row][from_col] = None
        
        piece.position = to_pos
        piece.has_moved = True
        
        return True
        
    def get_all_pieces(self, color):
        """Get all pieces of a given color."""
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    pieces.append(piece)
        return pieces
        
    def find_king(self, color):
        """Find the king of given color."""
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if isinstance(piece, King) and piece.color == color:
                    return piece
        return None
        
    def is_square_attacked(self, position, by_color):
        """Check if a square is attacked by any piece of given color."""
        attacking_pieces = self.get_all_pieces(by_color)
        for piece in attacking_pieces:
            if position in piece.get_possible_moves(self):
                return True
        return False
        
    def is_in_check(self, color):
        """Check if the king of given color is in check."""
        king = self.find_king(color)
        if king is None:
            return False
        opponent_color = 'black' if color == 'white' else 'white'
        return self.is_square_attacked(king.position, opponent_color)
        
    def copy(self):
        """Create a deep copy of the board."""
        new_board = Board.__new__(Board)
        new_board.grid = [[None for _ in range(8)] for _ in range(8)]
        new_board.captured_pieces = {
            'white': list(self.captured_pieces['white']),
            'black': list(self.captured_pieces['black'])
        }
        
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece:
                    piece_class = piece.__class__
                    new_piece = piece_class(piece.color, (row, col))
                    new_piece.has_moved = piece.has_moved
                    new_board.grid[row][col] = new_piece
                    
        return new_board
