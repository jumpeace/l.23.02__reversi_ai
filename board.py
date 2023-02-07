from piece import Piece
from vector2 import Vector2

# 盤面
class Board:
    # 任意の位置に任意の駒を置く(裏返し処理なし)
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

    # 任意の位置から任意の方向への位置情報の一覧を取得
    def get_poses_from_pos_to_way(self, from_pos: Vector2, way: Vector2) -> list[Vector2]:
        poses: list[Vector2] = []

        now_pos = Vector2(from_pos.y, from_pos.x)
        while True:
            if now_pos.x < 0 or now_pos.x >= self.size:
                break
            if now_pos.y < 0 or now_pos.y >= self.size:
                break
            
            poses.append(now_pos)
            
            now_pos.y += way.y
            now_pos.x = way.x
        
        return poses
    
    # 任意の位置から任意の方向への裏返せる枚数を取得
    def get_reversible_count_from_pos_to_way(self, from_pos: Vector2, way: Vector2, my_piece_kind_key: str) -> int:
        poses_from_pos_to_way: list[Vector2] = self.get_poses_from_pos_to_way(from_pos, way)
        
        # 駒を置く位置が空でない場合
        if self.data[poses_from_pos_to_way[0].y][poses_from_pos_to_way[0].x].check_empty():
            return 0
        
        # 駒を裏返せる分の駒の数がない場合
        if len(poses_from_pos_to_way) < 3:
            return 0
        
        for pos_index in range(len(poses_from_pos_to_way[1:])):
            pos_from_pos_to_way = poses_from_pos_to_way[pos_index]
            now_piece = self.data[pos_from_pos_to_way.y][pos_from_pos_to_way.x]

            if pos_index == 0:
                if not now_piece.check_enemy(my_piece_kind_key):
                    return 0
            
            else:
                if now_piece.check_empty():
                    return 0
                if now_piece.check_me(my_piece_kind_key):
                    return pos_index - 1
