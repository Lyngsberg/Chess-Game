"""Chess piece definitions and movement logic."""

class Piece:
    """Base class for all chess pieces."""
    
    def __init__(self, color, position):
        self.color = color  # 'white' or 'black'
        self.position = position  # (row, col)
        self.has_moved = False
        
    def get_possible_moves(self, board):
        """Return list of possible moves for this piece."""
        raise NotImplementedError
        
    def is_valid_move(self, target_pos, board):
        """Check if move to target position is valid."""
        return target_pos in self.get_possible_moves(board)
        
    def __repr__(self):
        return f"{self.color} {self.__class__.__name__} at {self.position}"


class Pawn(Piece):
    """Pawn piece."""
    
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        direction = -1 if self.color == 'white' else 1
        
        # Forward move
        forward_pos = (row + direction, col)
        if board.is_valid_position(forward_pos) and board.get_piece(forward_pos) is None:
            moves.append(forward_pos)
            
            # Double move from starting position
            if not self.has_moved:
                double_forward = (row + 2 * direction, col)
                if board.get_piece(double_forward) is None:
                    moves.append(double_forward)
        
        # Capture moves
        for dc in [-1, 1]:
            capture_pos = (row + direction, col + dc)
            if board.is_valid_position(capture_pos):
                target = board.get_piece(capture_pos)
                if target and target.color != self.color:
                    moves.append(capture_pos)
        
        return moves


class Knight(Piece):
    """Knight piece."""
    
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        
        # All possible knight moves
        knight_moves = [
            (row + 2, col + 1), (row + 2, col - 1),
            (row - 2, col + 1), (row - 2, col - 1),
            (row + 1, col + 2), (row + 1, col - 2),
            (row - 1, col + 2), (row - 1, col - 2)
        ]
        
        for pos in knight_moves:
            if board.is_valid_position(pos):
                target = board.get_piece(pos)
                if target is None or target.color != self.color:
                    moves.append(pos)
        
        return moves


class Bishop(Piece):
    """Bishop piece."""
    
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        
        # Diagonal directions
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_pos = (row + i * dr, col + i * dc)
                if not board.is_valid_position(new_pos):
                    break
                    
                target = board.get_piece(new_pos)
                if target is None:
                    moves.append(new_pos)
                else:
                    if target.color != self.color:
                        moves.append(new_pos)
                    break
        
        return moves


class Rook(Piece):
    """Rook piece."""
    
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        
        # Horizontal and vertical directions
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_pos = (row + i * dr, col + i * dc)
                if not board.is_valid_position(new_pos):
                    break
                    
                target = board.get_piece(new_pos)
                if target is None:
                    moves.append(new_pos)
                else:
                    if target.color != self.color:
                        moves.append(new_pos)
                    break
        
        return moves


class Queen(Piece):
    """Queen piece."""
    
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        
        # All directions (horizontal, vertical, diagonal)
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_pos = (row + i * dr, col + i * dc)
                if not board.is_valid_position(new_pos):
                    break
                    
                target = board.get_piece(new_pos)
                if target is None:
                    moves.append(new_pos)
                else:
                    if target.color != self.color:
                        moves.append(new_pos)
                    break
        
        return moves


class King(Piece):
    """King piece."""
    
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        
        # All adjacent squares
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        
        for dr, dc in directions:
            new_pos = (row + dr, col + dc)
            if board.is_valid_position(new_pos):
                target = board.get_piece(new_pos)
                if target is None or target.color != self.color:
                    moves.append(new_pos)
        
        return moves
