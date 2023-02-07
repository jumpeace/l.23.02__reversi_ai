from board import Board
from vector2 import Vector2

if __name__ == '__main__':
    board: Board = Board()
    board.print()
    board.place(Vector2(2, 4), 'BLACK')
    board.print()
