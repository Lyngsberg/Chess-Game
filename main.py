#!/usr/bin/env python3
"""Main entry point for the chess game."""
import argparse
from chess.gui import ChessGUI


def main():
    """Run the chess game."""
    parser = argparse.ArgumentParser(description='Play chess!')
    parser.add_argument('--ai', action='store_true', 
                       help='Play against AI opponent')
    args = parser.parse_args()
    
    gui = ChessGUI(ai_opponent=args.ai)
    gui.run()


if __name__ == '__main__':
    main()
