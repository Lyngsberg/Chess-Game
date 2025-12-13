"""Chess game graphical user interface using pygame."""
import pygame
from chess.game import ChessGame
from chess.ai import ChessAI
from chess.piece import Pawn, Knight, Bishop, Rook, Queen, King


class ChessGUI:
    """Graphical interface for the chess game."""
    
    # Colors
    WHITE = (240, 217, 181)
    BLACK = (181, 136, 99)
    HIGHLIGHT = (186, 202, 68)
    SELECTED = (246, 246, 105)
    
    def __init__(self, square_size=80, ai_opponent=False):
        pygame.init()
        self.square_size = square_size
        self.width = self.square_size * 8
        self.height = self.square_size * 8 + 60  # Extra space for status
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Chess Game")
        
        self.game = ChessGame()
        self.ai_opponent = ai_opponent
        self.ai = ChessAI('black') if ai_opponent else None
        self.ai_move_delay = 500  # milliseconds
        self.last_ai_move_time = 0
        self.font = pygame.font.Font(None, 36)
        self.status_font = pygame.font.Font(None, 28)
        
        # Unicode chess pieces
        self.piece_symbols = {
            ('white', 'King'): '♔',
            ('white', 'Queen'): '♕',
            ('white', 'Rook'): '♖',
            ('white', 'Bishop'): '♗',
            ('white', 'Knight'): '♘',
            ('white', 'Pawn'): '♙',
            ('black', 'King'): '♚',
            ('black', 'Queen'): '♛',
            ('black', 'Rook'): '♜',
            ('black', 'Bishop'): '♝',
            ('black', 'Knight'): '♞',
            ('black', 'Pawn'): '♟',
        }
        
    def get_square_from_mouse(self, pos):
        """Convert mouse position to board square."""
        x, y = pos
        if y >= self.square_size * 8:
            return None
        col = x // self.square_size
        row = y // self.square_size
        if 0 <= row < 8 and 0 <= col < 8:
            return (row, col)
        return None
        
    def draw_board(self):
        """Draw the chess board."""
        for row in range(8):
            for col in range(8):
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                rect = pygame.Rect(
                    col * self.square_size,
                    row * self.square_size,
                    self.square_size,
                    self.square_size
                )
                pygame.draw.rect(self.screen, color, rect)
                
    def draw_highlights(self):
        """Draw highlights for selected piece and valid moves."""
        if self.game.selected_piece:
            row, col = self.game.selected_piece.position
            rect = pygame.Rect(
                col * self.square_size,
                row * self.square_size,
                self.square_size,
                self.square_size
            )
            pygame.draw.rect(self.screen, self.SELECTED, rect)
            
        for move in self.game.valid_moves:
            row, col = move
            center_x = col * self.square_size + self.square_size // 2
            center_y = row * self.square_size + self.square_size // 2
            pygame.draw.circle(self.screen, self.HIGHLIGHT, (center_x, center_y), 10)
            
    def draw_pieces(self):
        """Draw all pieces on the board."""
        for row in range(8):
            for col in range(8):
                piece = self.game.board.get_piece((row, col))
                if piece:
                    symbol = self.piece_symbols.get(
                        (piece.color, piece.__class__.__name__),
                        '?'
                    )
                    text = self.font.render(symbol, True, (0, 0, 0))
                    text_rect = text.get_rect(
                        center=(
                            col * self.square_size + self.square_size // 2,
                            row * self.square_size + self.square_size // 2
                        )
                    )
                    self.screen.blit(text, text_rect)
                    
    def draw_status(self):
        """Draw game status bar."""
        status_rect = pygame.Rect(0, self.square_size * 8, self.width, 60)
        pygame.draw.rect(self.screen, (50, 50, 50), status_rect)
        
        status_text = self.game.get_game_status()
        text = self.status_font.render(status_text, True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.width // 2, self.square_size * 8 + 30)
        )
        self.screen.blit(text, text_rect)
        
    def draw(self):
        """Draw the entire game state."""
        self.draw_board()
        self.draw_highlights()
        self.draw_pieces()
        self.draw_status()
        pygame.display.flip()
        
    def handle_click(self, pos):
        """Handle mouse click on the board."""
        square = self.get_square_from_mouse(pos)
        if square is None:
            return
            
        if self.game.selected_piece is None:
            # Try to select a piece
            self.game.select_piece(square)
        else:
            # Try to move the selected piece
            if square in self.game.valid_moves:
                self.game.make_move(self.game.selected_piece.position, square)
            else:
                # Try selecting a different piece
                self.game.select_piece(square)
                
    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # Handle AI moves with delay for better UX
            current_time = pygame.time.get_ticks()
            if (self.ai_opponent and 
                self.game.current_player == 'black' and 
                not self.game.game_over and
                current_time - self.last_ai_move_time > self.ai_move_delay):
                move = self.ai.get_move(self.game)
                if move:
                    from_pos, to_pos = move
                    self.game.make_move(from_pos, to_pos)
                    self.last_ai_move_time = current_time
                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game.game_over:
                    # Only allow human moves if it's not AI's turn
                    if not self.ai_opponent or self.game.current_player == 'white':
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset game
                        self.game = ChessGame()
                        self.last_ai_move_time = 0
                        
            self.draw()
            clock.tick(60)
            
        pygame.quit()
