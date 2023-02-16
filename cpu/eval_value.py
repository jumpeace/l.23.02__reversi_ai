from vector2 import Vector2
from piece import Piece
from board import Board

# 評価値テーブル
EVAL_VALUE_TABLE: list[list[int]] = [
    [30, -12, 0, -1, -1, 0, -12, 30],
    [-12, -15, -3, -3, -3, -3, -15, -12],
    [0, -3, 0, -1, -1, 0, -3, 0],
    [-1, -3, -1, -1, -1, -1, -3, -1],
    [-1, -3, -1, -1, -1, -1, -3, -1],
    [0, -3, 0, -1, -1, 0, -3, 0],
    [-12, -15, -3, -3, -3, -3, -15, -12],
    [30, -12, 0, -1, -1, 0, -12, 30],
]

# 一つの駒のみ考慮した場合の評価値を取得
def _get_eval_value_by_one_piece(board: Board, piece_kind_key: str) -> int:
    # 返す評価値
    eval_value: int = 0

    for y in range(board.size):
        for x in range(board.size):
            if board.data[y][x].check_me(piece_kind_key):
                eval_value += EVAL_VALUE_TABLE[y][x]
    
    return eval_value

# 両方の駒を考慮した場合の評価値を取得
def get_eval_value(board: Board, my_piece_kind_key: str) -> int:
    # 自分の評価値
    my_eval_value = _get_eval_value_by_one_piece(board, my_piece_kind_key)
    # 敵の評価値
    enemy_eval_value = _get_eval_value_by_one_piece(board, Piece.get_enemy_kind_key(my_piece_kind_key))
    
    return my_eval_value - enemy_eval_value

# 評価値によって駒を置く場所を決める
def get_place_pos_by_eval_value(board: Board, my_piece_kind_key: str) -> Vector2:
    # 駒を置くことができる位置の一覧を取得
    placable_poses: list[Vector2] = board.get_placable_poses(my_piece_kind_key)

    # 評価値の最大値
    max_eval_value: int | None = None
    # 駒を置く予定の位置
    place_pos: int | None = None
    
    # 駒を置くことができる位置に置いてみたときの評価値を比較して, 最大の評価値の場合の位置を求める
    for placable_pos in placable_poses:
        # 駒を置いてみる(盤面はコピーしたもの)
        copied_board: Board = board.copy()
        copied_board.place(placable_pos, my_piece_kind_key)

        # 評価値を求める
        eval_value: int = get_eval_value(copied_board, my_piece_kind_key)
        
        # 一番初めの候補の場合
        if max_eval_value is None:
            max_eval_value = eval_value
            place_pos = placable_pos
        
        # 一番初めの候補以外の場合
        else:
            # 最高の評価値を更新した場合
            if eval_value > max_eval_value:
                max_eval_value = eval_value
            place_pos = placable_pos

    # 評価値以外の評価方法がないので, 一番最初に見つけた位置を返す
    return place_pos
