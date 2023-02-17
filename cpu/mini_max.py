from vector2 import Vector2
from piece import Piece
from board import Board
from .eval_value import get_eval_value

# 任意の深さ分探索して最大の評価値を返す
# ※ None は駒を置くことができる位置がない場合に返す
def _get_max_eval_value(board: Board, my_piece_kind_key: str, now_piece_kind_key: str, target_depth: int, depth: int) -> int | None:
    # 探索対象の深さの場合
    if depth == target_depth:
        return get_eval_value(board, my_piece_kind_key)
    
    # 駒を置くことができる位置の一覧を取得
    placable_poses: list[Vector2] = board.get_placable_poses(my_piece_kind_key)

    # 駒を置くことができる位置がない場合
    if len(placable_poses) == 0:
        return None

    # 評価値の最大値(決められた深さ)
    max_eval_value: int | None = None
    
    # 駒を置くことができる位置に置いてみたときの評価値を比較して, 最大の評価値の場合の位置を求める
    for placable_pos in placable_poses:
        # 駒を置いてみる(盤面はコピーしたもの)
        copied_board: Board = board.copy()
        copied_board.place(placable_pos, now_piece_kind_key)

        # 自分の駒を置くか敵の駒を置くかで探索の深さを変更する
        if now_piece_kind_key == my_piece_kind_key:
            next_depth = depth + 1
        else:
            next_depth = depth
        
        # 評価値を求める
        eval_value: int = _get_max_eval_value(copied_board, my_piece_kind_key, Piece.get_enemy_kind_key(now_piece_kind_key), target_depth, next_depth)

        # 駒を置くことができる位置がなかった場合
        if eval_value is None:
            continue
        
        # 一番初めの候補の場合
        if max_eval_value is None:
            max_eval_value = eval_value
        
        # 一番初めの候補以外の場合
        else:
            # 最高の評価値を更新した場合
            if eval_value > max_eval_value:
                max_eval_value = eval_value

    # 評価値以外の評価方法がないので, 一番最初に見つけた位置を返す
    return max_eval_value

# ミニマックス法によって駒を置く場所を決める
def get_place_pos_by_mini_max(board: Board, my_piece_kind_key: str, target_depth: int) -> Vector2:
    # 探索対象の深さが自然数でない場合は, 1マスにする
    if target_depth <= 0:
        target_depth = 1
    
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
        eval_value: int = _get_max_eval_value(copied_board, my_piece_kind_key, Piece.get_enemy_kind_key(my_piece_kind_key), target_depth, 1)
        
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
    
    return place_pos
