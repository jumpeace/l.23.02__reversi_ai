from vector2 import Vector2
from board import Board
from .eval_value import get_place_pos_by_eval_value
from .mini_max import get_place_pos_by_mini_max

def get_place_pos_by_cpu(board: Board, my_piece_kind_key: str) -> Vector2:
    # return get_place_pos_by_eval_value(board, my_piece_kind_key)
    return get_place_pos_by_mini_max(board, my_piece_kind_key, 2)
