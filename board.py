from piece import Piece
from vector2 import Vector2

# 盤面
class Board:
    # 任意の座標に任意の駒を置く(裏返し処理なし)
    def set(self, pos: Vector2, piece_kind_key: str):
        self.data[pos.y][pos.x].set(piece_kind_key)
    
    def __init__(self):
        # 盤面のサイズ
        self.size = 8

        # 盤面の駒のデータ
        self.data: list[list[Piece]] = []

        # 盤面の駒のデータを初期化
        # すべてのマスを駒を置いていない状態にする
        for _ in range(self.size):
            self.data.append([])
            for _ in range(self.size):
                self.data[-1].append(Piece())
        
        # 盤面の半分のサイズ
        half_size = int(self.size / 2)
        # 真ん中の4つのマスに駒を置く
        self.set(Vector2(half_size - 1, half_size - 1), 'BLACK')
        self.set(Vector2(half_size - 1, half_size), 'WHITE')
        self.set(Vector2(half_size, half_size - 1), 'WHITE')
        self.set(Vector2(half_size, half_size), 'BLACK')
    
    # 盤面を表示
    def print(self):
        # 上側部分を描画
        print('  ', end='')
        for x in range(self.size):
            print('  {} '.format(x + 1), end='')
        print()

        print('  ', end='')
        for _ in range(self.size):
            print('+---', end='')
        print('+')

        # 各列のマスを描画
        for y in range(self.size):
            print(' {}'.format(y + 1), end='')
            for sq in self.data[y]:
                print('| {} '.format(sq), end='')
            print('|')

            print('  ', end='')
            for _ in range(self.size):
                print('+---', end='')
            print('+')
