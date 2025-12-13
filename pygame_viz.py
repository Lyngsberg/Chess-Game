import pygame
import sys
import chess

board = chess.BoardHumanVHuman()


# Initialize pygame
pygame.init()



# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Load piece images
piece_images = {
    "p": pygame.image.load("images/black_pawn.png"),
    "r": pygame.image.load("images/black_rook.png"),
    "kn": pygame.image.load("images/black_knight.png"),
    "b": pygame.image.load("images/black_bishop.png"),
    "q": pygame.image.load("images/black_queen.png"),
    "ki": pygame.image.load("images/black_king.png"),
    "P": pygame.image.load("images/white_pawn.png"),
    "R": pygame.image.load("images/white_rook.png"),
    "KN": pygame.image.load("images/white_knight.png"),
    "B": pygame.image.load("images/white_bishop.png"),
    "Q": pygame.image.load("images/white_queen.png"),
    "KI": pygame.image.load("images/white_king.png"),
}

# Resize images
for key in piece_images:
    piece_images[key] = pygame.transform.scale(piece_images[key], (SQUARE_SIZE, SQUARE_SIZE))


# Function to draw the board
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to draw pieces
def draw_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            flipped_row = ROWS - 1 - row  # Flip row index
            piece = convert_to_pygame(board.game_board[flipped_row][col])  
            if piece:
                screen.blit(piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))  


def convert_to_pygame(piece):
    sign = piece[0]
    if piece[2] == 0:
        sign = sign.upper()
    return sign

font = pygame.font.Font(None, 36)
input_text = ""  # Stores user input    


# Main loop
running = True

while running:
    draw_board()
    draw_pieces()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    board.move()

pygame.quit()
sys.exit()
