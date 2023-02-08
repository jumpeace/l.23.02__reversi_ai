from vector2 import Vector2
from piece import Piece

# 盤面
class Board:
    # 任意の位置に任意の駒を置く(裏返し処理なし)
    def set(self, pos: Vector2, my_piece_kind_key: str):
        self.data[pos.y][pos.x].set(my_piece_kind_key)
    
    def __init__(self):
        # 盤面のサイズ
        self.size: int = 8

        # 盤面の駒のデータ
        self.data: list[list[Piece]] = []

        # 盤面の駒のデータを初期化
        # すべてのマスを駒を置いていない状態にする
        for _ in range(self.size):
            self.data.append([])
            for _ in range(self.size):
                self.data[-1].append(Piece())
        
        # 盤面の半分のサイズ
        half_size: int = int(self.size / 2)
        # 真ん中の4つのマスに駒を置く
        self.set(Vector2(half_size - 1, half_size - 1), 'BLACK')
        self.set(Vector2(half_size - 1, half_size), 'WHITE')
        self.set(Vector2(half_size, half_size - 1), 'WHITE')
        self.set(Vector2(half_size, half_size), 'BLACK')

    # 任意の位置から任意の方向への位置情報の一覧を取得
    def get_poses_from_pos_to_way(self, place_pos: Vector2, way: Vector2) -> list[Vector2]:
        poses: list[Vector2] = []

        now_pos: Vector2 = place_pos.copy()
        while True:
            if now_pos.x < 0 or now_pos.x >= self.size:
                break
            if now_pos.y < 0 or now_pos.y >= self.size:
                break
            
            poses.append(now_pos.copy())
            
            now_pos.y += way.y
            now_pos.x += way.x
        
        return poses
    
    # 任意の位置から任意の方向への裏返す位置を取得
    def get_reverse_poses_from_pos_to_way(self, place_pos: Vector2, way: Vector2, my_piece_kind_key: str) -> list[Vector2]:
        poses_from_pos_to_way: list[Vector2] = self.get_poses_from_pos_to_way(place_pos, way)
        
        # 駒を裏返せる分の駒の数がない場合
        if len(poses_from_pos_to_way) < 3:
            return []
        
        # 駒を置く位置が空でない場合
        if not self.data[poses_from_pos_to_way[0].y][poses_from_pos_to_way[0].x].check_empty():
            return []
        
        for pos_index in range(1, len(poses_from_pos_to_way)):
            now_pos: Vector2 = poses_from_pos_to_way[pos_index]
            now_piece: Piece = self.data[now_pos.y][now_pos.x]

            if pos_index == 0:
                # 駒を置く位置の隣の駒が敵の駒でない場合
                if not now_piece.check_enemy(my_piece_kind_key):
                    return []
            
            else:
                # どこまで裏返すかを探すときに駒がない位置がある場合
                if now_piece.check_empty():
                    return []
                # どこまで裏返すかが分かった場合
                if now_piece.check_me(my_piece_kind_key):
                    return poses_from_pos_to_way[1:pos_index]
        
        return []
    
    # 任意の位置から任意の方向へ裏返せるかを判定
    def get_reverse_poses_from_pos(self, place_pos: Vector2, my_piece_kind_key: str) -> list[Vector2]:
        reverse_poses: list[Piece] = []
        
        for way_y in range(-1, 2):
            for way_x in range(-1, 2):
                if way_y == 0 and way_x == 0:
                    continue
                
                for reverse_pos in self.get_reverse_poses_from_pos_to_way(place_pos, Vector2(way_y, way_x), my_piece_kind_key):
                    reverse_poses.append(reverse_pos)
        
        return reverse_poses
    
    # 任意の位置から任意の方向へ裏返せるかを判定
    # ※ 返り値は駒を置けたかどうかを返す
    def place(self, place_pos: Vector2, my_piece_kind_key: str) -> bool:
        reverse_poses: list[Vector2] = self.get_reverse_poses_from_pos(place_pos, my_piece_kind_key)
        
        # 裏返せる位置がない場合
        if len(reverse_poses) == 0:
            return False
        
        # 駒を置く
        self.data[place_pos.y][place_pos.x].set(my_piece_kind_key)
        # 駒を裏返す
        for reverse_pos in reverse_poses:
            self.data[reverse_pos.y][reverse_pos.x].set(my_piece_kind_key)
        
        return True
    
    # 任意の駒の置ける位置の一覧を取得
    def get_placable_poses(self, my_piece_kind_key: str) -> list[Vector2]:
        placable_poses: list[Vector2] = []
        
        for pos_y in range(self.size):
            for pos_x in range(self.size):
                now_pos = Vector2(pos_y, pos_x)
                reverse_poses = self.get_reverse_poses_from_pos(now_pos, my_piece_kind_key)
                if len(reverse_poses) > 0:
                    placable_poses.append(now_pos)
        
        return placable_poses
    
    # 任意の駒を置こうとしている場合の盤面を表示
    def display(self, my_piece_kind_key: str):
        # 任意の駒の置ける位置の一覧
        placable_poses = self.get_placable_poses(my_piece_kind_key)
        
        # 上側部分を描画
        print('  ', end='')
        for pos_x in range(self.size):
            print('  {} '.format(pos_x + 1), end='')
        print()

        print('  ', end='')
        
        for _ in range(self.size):
            print('+---', end='')
        print('+')

        # 各列のマスを描画
        for pos_y in range(self.size):
            print(' {}'.format(pos_y + 1), end='')
            for pos_x in range(self.size):
                # 任意の駒の置ける位置の一覧も表示する
                sq: str = self.data[pos_y][pos_x]
                if self.data[pos_y][pos_x].check_empty():
                    if Vector2(pos_y, pos_x) in placable_poses:
                        sq = '-'
                
                print('| {} '.format(sq), end='')
            print('|')

            print('  ', end='')
            for _ in range(self.size):
                print('+---', end='')
            print('+')
    
    # 盤面上の任意の駒の数を数える
    def get_count_by_piece_kind_key(self, my_piece_kind_key: str) -> int:
        count: int = 0

        for pos_y in range(self.size):
            for pos_x in range(self.size):
                if self.data[pos_y][pos_x].check_me(my_piece_kind_key):
                    count += 1
        
        return count
