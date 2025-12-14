import pygame
import sys
import chess

# --- Configuration ---
BOARD_SIZE = 600
MARGIN = 40
WIDTH = BOARD_SIZE + (2 * MARGIN)
HEIGHT = BOARD_SIZE + (2 * MARGIN) + 100
SQ_SIZE = BOARD_SIZE // 8
FPS = 60

# Colors
WHITE_COLOR = (240, 217, 181)
BLACK_COLOR = (181, 136, 99)
BG_COLOR = (30, 30, 30)
BORDER_COLOR = (70, 50, 40)
TEXT_COLOR = (255, 255, 255)
COORD_COLOR = (220, 220, 220)
INPUT_BOX_COLOR = (50, 50, 50)
ACTIVE_BORDER_COLOR = (0, 200, 255)
INACTIVE_BORDER_COLOR = (100, 100, 100)

PIECE_NAMES = {
    'p': 'pawn', 'kn': 'knight', 'b': 'bishop', 
    'r': 'rook', 'q': 'queen', 'ki': 'king'
}

def parse_move(user_input):
    """
    Translates 'e2 e4' OR 'e2e4' -> (row, col) integers.
    """
    clean_input = user_input.strip().lower()
    parts = clean_input.split()
    
    start, end = "", ""
    
    # Case 1: Space separated "e2 e4"
    if len(parts) == 2:
        start, end = parts[0], parts[1]
    # Case 2: No space "e2e4"
    elif len(parts) == 1 and len(parts[0]) == 4:
        start = parts[0][:2]
        end = parts[0][2:]
    else:
        return None

    if len(start) != 2 or len(end) != 2: 
        return None

    file_map = {c: i for i, c in enumerate('abcdefgh')}
    try:
        c_col = file_map[start[0]]
        c_row = int(start[1]) - 1 
        n_col = file_map[end[0]]
        n_row = int(end[1]) - 1
        return (c_row, c_col, n_row, n_col)
    except (KeyError, ValueError):
        return None

def load_images():
    images = {}
    pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
    colors = ['white', 'black']
    for p in pieces:
        for c in colors:
            key = f"{c}_{p}"
            try:
                path = f"images/{key}.png"
                img = pygame.image.load(path)
                images[key] = pygame.transform.scale(img, (SQ_SIZE, SQ_SIZE))
            except FileNotFoundError:
                s = pygame.Surface((SQ_SIZE, SQ_SIZE))
                s.fill((255, 0, 0))
                images[key] = s
    return images

def draw_board_and_coordinates(screen, font):
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WIDTH, BOARD_SIZE + 2*MARGIN))
    files = "ABCDEFGH"
    for col in range(8):
        x = MARGIN + (col * SQ_SIZE) + (SQ_SIZE // 2)
        y = MARGIN + BOARD_SIZE + 10
        label = font.render(files[col], True, COORD_COLOR)
        screen.blit(label, label.get_rect(center=(x, y)))
    for row in range(8):
        rank_label = str(row + 1)
        x = MARGIN // 2
        y = MARGIN + ((7 - row) * SQ_SIZE) + (SQ_SIZE // 2)
        label = font.render(rank_label, True, COORD_COLOR)
        screen.blit(label, label.get_rect(center=(x, y)))
    for row in range(8):
        for col in range(8):
            color = WHITE_COLOR if (row + col) % 2 == 0 else BLACK_COLOR
            x = MARGIN + (col * SQ_SIZE)
            y = MARGIN + ((7 - row) * SQ_SIZE)
            pygame.draw.rect(screen, color, (x, y, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board, images):
    for row in range(8):
        for col in range(8):
            piece = board.game_board[row][col]
            if piece != board.none_piece:
                sign, _, color_code = piece
                color_name = "white" if color_code == 0 else "black"
                piece_name = PIECE_NAMES.get(sign, "pawn")
                image_key = f"{color_name}_{piece_name}"
                if image_key in images:
                    x = MARGIN + (col * SQ_SIZE)
                    y = MARGIN + ((7 - row) * SQ_SIZE)
                    screen.blit(images[image_key], (x, y))

def draw_ui(screen, font, user_text, status_message, is_white_turn):
    ui_y_start = BOARD_SIZE + (2 * MARGIN)
    
    pygame.draw.rect(screen, BG_COLOR, (0, ui_y_start, WIDTH, HEIGHT - ui_y_start))
    
    input_rect = pygame.Rect(MARGIN, ui_y_start + 10, WIDTH - (2*MARGIN), 40)
    pygame.draw.rect(screen, INPUT_BOX_COLOR, input_rect)
    
    border_color = ACTIVE_BORDER_COLOR if is_white_turn else INACTIVE_BORDER_COLOR
    pygame.draw.rect(screen, border_color, input_rect, 2)
    
    text_surface = font.render(user_text, True, TEXT_COLOR)
    screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))
    
    if is_white_turn:
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            text_width = text_surface.get_width()
            cursor_x = input_rect.x + 10 + text_width
            cursor_y_start = input_rect.y + 8
            cursor_y_end = input_rect.y + 32
            pygame.draw.line(screen, TEXT_COLOR, (cursor_x, cursor_y_start), (cursor_x, cursor_y_end), 2)

    status_surface = font.render(status_message, True, (200, 200, 200))
    screen.blit(status_surface, (MARGIN, ui_y_start + 60))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    
    pygame.key.set_repeat(400, 50)
    
    images = load_images()
    board = chess.BoardHumanVRandom()
    
    user_text = ''
    status_message = "White to move. Input e.g., 'e2e4' or 'e2 e4'"
    running = True
    game_over = False
    
    last_move_time = 0
    ai_delay_ms = 500

    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if board.turn == "white" and not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        coords = parse_move(user_text)
                        if coords:
                            cur_r, cur_c, next_r, next_c = coords
                            result = board.move_api(cur_r, cur_c, next_r, next_c)
                            if result == 0:
                                status_message = ""
                                user_text = ""
                                last_move_time = current_time
                            elif result == 1: status_message = "Error: Out of bounds."
                            elif result == 2: status_message = "Error: Invalid move."
                        else:
                            status_message = "Format error. Use: 'e2e4' or 'e2 e4'"
                    else:
                        user_text += event.unicode

        if not game_over:
            if board.is_checkmate():
                game_over = True
                winner = "Black" if board.turn == "white" else "White"
                status_message = f"Checkmate! {winner} Won."
            elif len(board.action_space()) == 0:
                game_over = True
                status_message = "Stalemate."
            elif board.current_turn >= board.max_turn:
                game_over = True
                status_message = "Draw (Max turns)."

        if board.turn == "black" and not game_over:
            if current_time - last_move_time > ai_delay_ms:
                try:
                    ai_move = board.random_action()
                    board.move_api(*ai_move)
                    
                    files = "abcdefgh"
                    r1, c1, r2, c2 = ai_move
                    move_str = f"{files[c1]}{r1+1}->{files[c2]}{r2+1}"
                    status_message = f"Black played {move_str}. Your turn."
                except Exception as e:
                    print(f"AI Error: {e}")

        screen.fill(BG_COLOR)
        draw_board_and_coordinates(screen, font)
        draw_pieces(screen, board, images)
        
        is_white_turn = (board.turn == "white" and not game_over)
        draw_ui(screen, font, user_text, status_message, is_white_turn)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()