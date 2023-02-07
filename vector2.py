# 2次元座標
class Vector2:
    def __init__(self, y: int, x: int):
        # Y座標
        self.y: int = y
        # X座標
        self.x: int = x
    
    # 2次元座標の情報を文字列に変換
    def __str__(self) -> str:
        return 'Vector2[{}, {}]'.format(self.y, self.x)
    
    # 2次元座標の情報をコピー
    def copy(self):
        return Vector2(self.y, self.x)
