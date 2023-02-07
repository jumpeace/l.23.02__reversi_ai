class Piece:
    KINDS: dict[str, str] = {
        'BLACK': 'X',
        'WHITE': 'O',
    }
    
    def __init__(self):
        self.data: str | None = None
    
    def set(self, kind_key: str):
        self.data = self.KINDS[kind_key]
    
    def check_empty(self) -> bool:
        return self.data is None
    
    def check_kind(self, kind_key: str) -> bool:
        if self.check_empty():
            return False
        return  self.data == self.KINDS[kind_key]
    
    def __str__(self):
        if self.check_empty():
            return ' '
        return self.data
