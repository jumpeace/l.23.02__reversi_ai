from piece import Piece
from vector2 import Vector2

class Board:
    def set(self, pos: Vector2, piece_kind_key: str):
        self.data[pos.y][pos.x].set(piece_kind_key)
    
    def __init__(self):
        self.size = 8

        self.data: list[list[Piece]] = []
        for _ in range(self.size):
            self.data.append([])
            for _ in range(self.size):
                self.data[-1].append(Piece())
        
        half_size = int(self.size / 2)
        self.set(Vector2(half_size - 1, half_size - 1), 'BLACK')
        self.set(Vector2(half_size - 1, half_size), 'WHITE')
        self.set(Vector2(half_size, half_size - 1), 'WHITE')
        self.set(Vector2(half_size, half_size), 'BLACK')
    
    def print(self):
        print('  ', end='')
        for x in range(self.size):
            print('  {} '.format(x + 1), end='')
        print()

        print('  ', end='')
        for _ in range(self.size):
            print('+---', end='')
        print('+')

        for y in range(self.size):
            print(' {}'.format(y + 1), end='')
            for sq in self.data[y]:
                print('| {} '.format(sq), end='')
            print('|')

            print('  ', end='')
            for _ in range(self.size):
                print('+---', end='')
            print('+')
