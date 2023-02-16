# 駒
class Piece:
    # 駒の種類
    KINDS: dict[str, str] = {
        'BLACK': 'X',   # 黒
        'WHITE': 'O',   # 白
    }
    
    # 敵の駒の種類のキーを取得する
    def get_enemy_kind_key(my_kind_key: str) -> str:
        if my_kind_key == 'BLACK':
            return 'WHITE'
        if my_kind_key == 'WHITE':
            return 'BLACK'
    
    def __init__(self):
        # 駒のデータ
        self.data: str | None = None
    
    # 駒の情報を文字列に変換
    def __str__(self) -> str:
        if self.check_empty():
            return ' '
        return self.data

    # 駒をコピー
    def copy(self):
        copied_instance = Piece()
        copied_instance.data = self.data
        return copied_instance
    
    # 任意の駒を置く(裏返し処理なし)
    def set(self, kind_key: str):
        self.data = self.KINDS[kind_key]
    
    # 駒が置かれていないかを判定する
    def check_empty(self) -> bool:
        return self.data is None
    
    # 任意の駒かどうかを判定する
    def check_me(self, my_kind_key: str) -> bool:
        if self.check_empty():
            return False
        return  self.data == self.KINDS[my_kind_key]
    
    # 任意の駒の敵の駒かどうかを判定する
    def check_enemy(self, my_kind_key: str) -> bool:
        if self.check_empty():
            return False
        if my_kind_key == 'BLACK':
            return self.data == self.KINDS['WHITE']
        if my_kind_key == 'WHITE':
            return self.data == self.KINDS['BLACK']
        return False
