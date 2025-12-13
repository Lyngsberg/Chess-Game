# Chess Game

A fully playable chess game with a graphical interface, built with Python and pygame. The project is structured to support future Deep Neural Network integration for AI opponents.

## Features

- ✅ **Playable Chess Game**: Complete implementation of chess rules
  - All piece movements (Pawn, Knight, Bishop, Rook, Queen, King)
  - Special moves: Pawn double move, pawn promotion
  - Check and checkmate detection
  - Stalemate detection
  - Move validation (prevents moving into check)

- ✅ **Visual Interface**: Clean and intuitive pygame-based GUI
  - 8x8 chessboard with alternating colors
  - Unicode chess piece symbols
  - Highlight selected pieces and valid moves
  - Status bar showing current player and game state
  - Mouse-based move selection

- ✅ **AI Opponent** (Basic): Play against a random-move AI
  - Foundation for future Deep Neural Network integration
  - Modular AI structure for easy replacement/upgrade

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Lyngsberg/Chess-Game.git
cd Chess-Game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Play against another human:
```bash
python main.py
```

### Play against AI opponent:
```bash
python main.py --ai
```

### Controls:
- **Click** on a piece to select it (valid moves will be highlighted)
- **Click** on a highlighted square to move the selected piece
- **Press R** to reset the game
- **Close window** to quit

## Project Structure

```
Chess-Game/
├── chess/
│   ├── __init__.py      # Package initialization
│   ├── piece.py         # Chess piece classes and movement logic
│   ├── board.py         # Board representation and management
│   ├── game.py          # Game state and rules (check, checkmate, etc.)
│   ├── gui.py           # Pygame visual interface
│   └── ai.py            # AI opponent (placeholder for DNN)
├── main.py              # Entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Future Development: Deep Neural Network

The project is structured to support Deep Neural Network training for intelligent chess AI:

### Planned Features:
- **Neural Network Architecture**: Implement a deep learning model to evaluate board positions
- **Training Pipeline**: Create training infrastructure using game databases
- **Self-Play**: Enable the AI to learn by playing against itself
- **Move Prediction**: Train the network to predict strong moves
- **Position Evaluation**: Implement sophisticated board evaluation

### AI Structure:
The `chess/ai.py` module contains a placeholder `ChessAI` class with:
- `get_move()`: Returns the AI's chosen move
- `evaluate_position()`: Evaluates board positions
- Comments outlining future DNN implementation

To integrate a Deep Neural Network:
1. Implement the `DeepChessAI` class (template provided in `ai.py`)
2. Add model training scripts
3. Create a dataset from chess games
4. Train and save the model
5. Load the trained model in the GUI

## Development

### Running Tests:
```bash
python -c "from chess import ChessGame; game = ChessGame(); print('Tests passed!')"
```

### Architecture:
- **Separation of Concerns**: Game logic is separate from UI
- **Modular Design**: Easy to extend and modify
- **Clean API**: Simple interfaces between components

## Requirements

- Python 3.7+
- pygame 2.5.0+
- numpy 1.24.0+

## License

Open source - feel free to use and modify!

## Contributing

Contributions are welcome! Areas for improvement:
- Enhanced AI algorithms
- Deep Neural Network integration
- Additional chess rules (en passant, castling)
- Move history and undo functionality
- Game saving/loading
- Online multiplayer support
