
class Square:

    def __init__(self, row, col, piece=None):
        self.col = col #col number
        self.row = row #row number
        self.piece = piece #piece on current square

    #getters:
    def get_col(self) -> int:
        return self.col 
    def get_row(self) -> int:
        return self.row
    def get_piece(self) ->str:
        return self.piece
    #setters:
    def set_piece(self, new_piece):
        self.piece = new_piece

    def has_piece(self) -> bool:
        return self.piece != None