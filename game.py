from vector2 import Vector2
from piece import Piece
from board import Board
from cpu.main import get_place_pos_by_cpu

# ゲームの管理
class Game:
    def __init__(self):
        # 誰のターンかを保持
        self.my_piece_kind_key: str = 'BLACK'
        # ゲームの盤面
        self.board: Board = Board()
        # 前回のターンでパスされたか
        self.prev_passed: bool = False
        self.is_human_dict: dict[str, bool] = {
            # 先手(黒)が人間かどうか
            'BLACK': True,
            # 後手(白)が人間かどうか
            'WHITE': False,
        }
    
    # 人間による駒を置く場所の入力
    def input_place_pos_by_human(self) -> Vector2:
        print('{}\'s Turn: '.format(self.my_piece_kind_key), end='')
        while True:
            input_str: str = input()

            # 入力された文字の文字数が2文字でなかった場合
            if len(input_str) != 2:
                print('You should enter a 2-character string: ', end='')
                continue
            
            # 入力された文字の1文字目が数字でなかった場合
            try:
                tmp_place_pos_y: int = int(input_str[0])
            except ValueError:
                print('The first character must be a number: ', end='')
                continue
            
            # 入力された文字の1文字目が正しい範囲でなかった場合
            if not (1 <= tmp_place_pos_y <= self.board.size):
                print('The first character must be between 1 and {}: '.format(self.board.size), end='')
                continue
            
            # 入力された文字の2文字目が数字でなかった場合
            try:
                tmp_place_pos_x: int = int(input_str[1])
            except ValueError:
                print('The second character must be a number: ', end='')
                continue
            
            # 入力された文字の2文字目が正しい範囲でなかった場合
            if not (1 <= tmp_place_pos_x <= self.board.size):
                print('The second character must be between 1 and {}: '.format(self.board.size), end='')
                continue
            
            place_pos: Vector2 = Vector2(tmp_place_pos_y - 1, tmp_place_pos_x - 1)
            if not self.board.get_reverse_poses_from_pos(place_pos, self.my_piece_kind_key):
                print('You should enter the position where the piece can be placed: ', end='')
                continue
            
            break
        
        return Vector2(tmp_place_pos_y - 1, tmp_place_pos_x - 1)
    
    # CPUによる駒を置く場所の入力
    def input_place_pos_by_cpu(self) -> Vector2:
        place_pos: Vector2 = get_place_pos_by_cpu(self.board, self.my_piece_kind_key)
        print('{} place [{}, {}].'.format(self.my_piece_kind_key, place_pos.y, place_pos.x))

        return place_pos
    
    # 相手のターンにする
    def change_turn(self):
        self.my_piece_kind_key = Piece.get_enemy_kind_key(self.my_piece_kind_key)

    # 1ターンの処理を行う
    #  返り値は次のターンを行うかどうか
    def play_one_turn(self) -> bool:
        # 人間のターンかどうか
        is_human_turn = self.is_human_dict[self.my_piece_kind_key]

        # 駒を置ける場所も含めて表示する(人間のターンのみ)
        if is_human_turn:
            self.board.display(self.my_piece_kind_key)
        
        # 全てのマスが埋まっているかを確認
        black_piece_count: int = self.board.get_count_by_piece_kind_key('BLACK')
        white_piece_count: int = self.board.get_count_by_piece_kind_key('WHITE')
        if black_piece_count + white_piece_count == self.board.size * self.board.size:
            return False
        
        # 駒を置ける位置の一覧
        placable_poses: list[Vector2] = self.board.get_placable_poses(self.my_piece_kind_key)
        # 駒を置けない場合
        if len(placable_poses) == 0:
            # パスすることを表示する
            print('{} passed.'.format(self.my_piece_kind_key))

            # 相手のターンにする
            self.change_turn()

            # 前回のターンでパスした場合, 次のターンは行わない
            if self.prev_passed:
                return False
            
            # 前回のターンでパスしていない場合, パスしたことにする
            self.prev_passed = True
            return True

        # 駒を置く位置を入力する
        # 人間のターンの場合
        if is_human_turn:
            place_pos: Vector2 = self.input_place_pos_by_human()
        # CPUのターンの場合
        else:
            place_pos: Vector2 = self.input_place_pos_by_cpu()

        # 駒を置く
        self.board.place(place_pos, self.my_piece_kind_key)
        
        # 相手のターンにする
        self.change_turn()
        
        return True

    # ゲーム結果を表示する
    def display_result(self):
        black_piece_count: int = self.board.get_count_by_piece_kind_key('BLACK')
        white_piece_count: int = self.board.get_count_by_piece_kind_key('WHITE')
        
        print('BLACK: {}, WHITE: {}'.format(black_piece_count, white_piece_count))

        if black_piece_count > white_piece_count:
            print('BLACK WIN')
        elif black_piece_count < white_piece_count:
            print('WHITE WIN')
        else:
            print('DRAW')
    
    def play_once(self):
        # 両方のターンで駒をおけなくなるまで行う
        while True:
            do_next_turn: bool = self.play_one_turn()
            # 次のターンを行わない場合
            if not do_next_turn:
                break
        
        print('Finished.')
        
        self.display_result()
