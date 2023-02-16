from vector2 import Vector2
from board import Board

def get_place_pos_by_cpu(board: Board, my_piece_kind_key: str) -> Vector2:
    placable_poses: list[Vector2] = board.get_placable_poses(my_piece_kind_key)
    place_pos: Vector2 = placable_poses[0]
    return place_pos