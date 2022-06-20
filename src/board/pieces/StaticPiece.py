from src.board.pieces.Piece import Piece

class StaticPiece(Piece):

    def __init__(self, type, color, index, steps, sprite):
        super().__init__(type=type, color=color, index=index, steps=steps, sprite=sprite)

    def legal_moves(self, grid):

        legal_moves = set()

        is_check = grid.is_check(self.color)

        is_protecting = grid.check[self.color][self.index] and grid.check[self.color][grid.check_piece[self.color]]

        for step in self.steps:
            x, y = self.index % 8, self.index // 8
            if -1 < x + step[0] < 8 and -1 < y + step[1] < 8:

                next_index = self.index + step[1] * 8 + step[0]

                if (not is_check or grid.check[self.color][next_index]) and (
                        not is_protecting or grid.check[self.color][next_index]):
                    if next_index in grid.pieces[1 - self.color]:

                        self.danger.add(next_index)
                        legal_moves.add(next_index)

                        if next_index == grid.check_piece[1 - self.color]:
                            self.check.add(next_index)
                            self.check.add(self.index)

                    elif next_index not in grid.pieces[self.color]:
                            legal_moves.add(next_index)
                            self.danger.add(next_index)

        return legal_moves
