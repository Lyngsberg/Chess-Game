"""Chess piece definitions and movement logic."""

class Piece:
    """Base class for all chess pieces."""
    
    def __init__(self, color, position):
        self.color = color  # 'white' or 'black'
        self.position = position  # (row, col)
        self.has_moved = False
        
    def get_possible_moves(self, board, for_attack_check=False):
        """Return list of possible moves for this piece.
        
        Args:
            board: The chess board
            for_attack_check: If True, only return attacking moves (no castling)
        """
        raise NotImplementedError
        
    def is_valid_move(self, target_pos, board):
        """Check if move to target position is valid."""
        return target_pos in self.get_possible_moves(board)
        
    def __repr__(self):
        return f"{self.color} {self.__class__.__name__} at {self.position}"


class Pawn(Piece):
    """Pawn piece."""
    
    def get_possible_moves(self, board, for_attack_check=False):
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
                # For attack checking, pawns always attack diagonally
                if for_attack_check:
                    moves.append(capture_pos)
                else:
                    target = board.get_piece(capture_pos)
                    if target and target.color != self.color:
                        moves.append(capture_pos)
                        
                    # En passant
                    elif (board.last_move and 
                          isinstance(board.last_move.get('piece'), Pawn) and
                          board.last_move.get('from') and board.last_move.get('to') and
                          abs(board.last_move['from'][0] - board.last_move['to'][0]) == 2 and
                          board.last_move['to'][0] == row and
                          board.last_move['to'][1] == col + dc):
                        # Verify the pawn is actually there
                        if board.get_piece((row, col + dc)) is not None:
                            moves.append(capture_pos)
        
        return moves


class Knight(Piece):
    """Knight piece."""
    
    def get_possible_moves(self, board, for_attack_check=False):
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
    
    def get_possible_moves(self, board, for_attack_check=False):
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
    
    def get_possible_moves(self, board, for_attack_check=False):
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
    
    def get_possible_moves(self, board, for_attack_check=False):
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
    
    def get_possible_moves(self, board, for_attack_check=False):
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
        
        # Castling (only when not checking for attacks to avoid recursion)
        if not for_attack_check and not self.has_moved and not board.is_in_check(self.color):
            # Kingside castling
            if self._can_castle_kingside(board):
                moves.append((row, col + 2))
            # Queenside castling
            if self._can_castle_queenside(board):
                moves.append((row, col - 2))
        
        return moves
    
    def _can_castle_kingside(self, board):
        """Check if kingside castling is possible."""
        row, col = self.position
        rook = board.get_piece((row, 7))
        
        if not isinstance(rook, Rook) or rook.has_moved:
            return False
        
        # Check if squares between king and rook are empty
        for c in range(col + 1, 7):
            if board.get_piece((row, c)) is not None:
                return False
        
        # Check if squares king passes through are not attacked
        opponent_color = 'black' if self.color == 'white' else 'white'
        for c in range(col, col + 3):
            if board.is_square_attacked((row, c), opponent_color):
                return False
        
        return True
    
    def _can_castle_queenside(self, board):
        """Check if queenside castling is possible."""
        row, col = self.position
        rook = board.get_piece((row, 0))
        
        if not isinstance(rook, Rook) or rook.has_moved:
            return False
        
        # Check if squares between king and rook are empty
        for c in range(1, col):
            if board.get_piece((row, c)) is not None:
                return False
        
        # Check if squares king passes through are not attacked
        opponent_color = 'black' if self.color == 'white' else 'white'
        for c in range(col - 2, col + 1):
            if board.is_square_attacked((row, c), opponent_color):
                return False
        
        return True
