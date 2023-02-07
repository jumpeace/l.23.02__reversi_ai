# 駒
class Piece:
    # 駒の種類
    KINDS: dict[str, str] = {
        'BLACK': 'X',   # 黒
        'WHITE': 'O',   # 白
    }
    
    def __init__(self):
        # 駒のデータ
        self.data: str | None = None
    
    # 任意の駒を置く(裏返し処理なし)
    def set(self, kind_key: str):
        self.data = self.KINDS[kind_key]
    
    # 駒が置かれていないかを判定する
    def check_empty(self) -> bool:
        return self.data is None
    
    # 任意の駒かどうかを判定する
    def check_kind(self, kind_key: str) -> bool:
        if self.check_empty():
            return False
        return  self.data == self.KINDS[kind_key]
    
    # 駒の情報を文字列に変換
    def __str__(self):
        if self.check_empty():
            return ' '
        return self.data
