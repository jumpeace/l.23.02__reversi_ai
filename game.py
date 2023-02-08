from vector2 import Vector2
from piece import Piece
from board import Board

# ゲームの管理
class Game:
    def __init__(self):
        # 誰のターンかを保持
        self.my_piece_kind_key: str = 'BLACK'
        # ゲームの盤面
        self.board: Board = Board()
        # 前回のターンでパスされたか
        self.prev_passed = False
    
    # 人間による駒を置く場所の入力
    def input_place_pos_by_human(self) -> Vector2:
        print('Position to place: ', end='')
        while True:
            input_str = input()

            # 入力された文字の文字数が2文字でなかった場合
            if len(input_str) != 2:
                print('You should enter a 2-character string: ', end='')
                continue
            
            # 入力された文字の1文字目が数字でなかった場合
            try:
                place_pos_y: int = int(input_str[0])
            except ValueError:
                print('The first character must be a number: ', end='')
                continue
            
            # 入力された文字の2文字目が数字でなかった場合
            try:
                place_pos_x: int = int(input_str[1])
            except ValueError:
                print('The second character must be a number: ', end='')
                continue
            
            break
        
        return Vector2(place_pos_y, place_pos_x)

    # 1ターンの処理を行う
    #  返り値は次のターンを行うかどうか
    def play_one_turn(self) -> bool:
        # 駒を置ける場所も含めて表示する
        self.board.print(self.my_piece_kind_key)

        # 駒を置く位置を入力する
        place_pos = self.input_place_pos_by_human()

        # 駒を置く
        done_place = self.board.place(place_pos, self.my_piece_kind_key)

        if not done_place:
            # 駒を置けていない場合
            if self.prev_passed:
                # 前回のターンでパスした場合, 次のターンは行わない
                return False
            # 前回のターンでパスしていない場合, パスしたことにする
            self.prev_passed = True
        
        # 相手のターンにする
        self.my_piece_kind_key = Piece.get_enemy_kind_key(self.my_piece_kind_key)
