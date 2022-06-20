from src.board.pieces.Pawn import Pawn
from src.board.pieces.Knight import Knight
from src.board.pieces.Bishop import Bishop
from src.board.pieces.Rook import Rook
from src.board.pieces.Queen import Queen
from src.board.pieces.King import King

class Grid:

    def __init__(self):

        self.danger = [[0 for i in range(8*8)] for color in range(2)]
        self.check = [[0 for i in range(8*8)] for color in range(2)]

        self.moves = []

        self.pieces = [dict() for color in range(2)]

        for i in range(16):
            self.pieces[i&1][i//2 + (i&1)*48 + (1 - i&1)*8] = Pawn(i&1,i//2 + (i&1)*48 + (1 - i&1)*8)

        self.pieces[0][0] = Rook(0,0)
        self.pieces[0][1] = Knight(0,1)
        self.pieces[0][2] = Bishop(0,2)
        self.pieces[0][3] = Queen(0,3)
        self.pieces[0][4] = King(0,4)
        self.pieces[0][5] = Bishop(0,5)
        self.pieces[0][6] = Knight(0,6)
        self.pieces[0][7] = Rook(0,7)

        self.pieces[1][56] = Rook(1, 56)
        self.pieces[1][57] = Knight(1, 57)
        self.pieces[1][58] = Bishop(1, 58)
        self.pieces[1][59] = Queen(1, 59)
        self.pieces[1][60] = King(1, 60)
        self.pieces[1][61] = Bishop(1, 61)
        self.pieces[1][62] = Knight(1, 62)
        self.pieces[1][63] = Rook(1, 63)

        self.check_piece = [4,60]

        self.update()

    def update(self):
        self.update_color(color=0)
        self.update_color(color=1)

    def update_color(self, color):
        for _, piece in self.pieces[color].items():
            piece.update(self)

    def is_check(self, color):
        return self.danger[color][self.check_piece[color]]

    def is_check_blocked(self, color):
        return not self.pieces[color][self.check_piece[color]].cache_legal_moves

    def is_color_blocked(self, color):
        for index, piece in self.pieces[color].items():
            if piece.cache_legal_moves:
                return False
        return True

    def is_checkmate(self, color):
        return self.pieces[color] and self.is_color_blocked(color)

    def is_stalemate(self, color):
        return not self.pieces[color] and self.is_check_blocked(color)

    def undo(self):
        if not self.moves:
            return False

        last_piece_move = self.moves.pop()
        last_piece_move.undo(self)

        return True


    def __contains__(self, item):
        return (item in self.pieces[0]) or (item in self.pieces[1])