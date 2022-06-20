from src.board.pieces.Piece import Piece

class PawnoidPiece(Piece):
    def __init__(self, color, type, index, normal_steps, killer_steps, sprite):
        super().__init__(color=color, type=type, index=index, steps=[], sprite=sprite)

        self.normal_steps = [(step[0], step[1]*self.direction) for step in normal_steps]
        self.killer_steps = [(step[0], step[1]*self.direction) for step in killer_steps]

    def legal_moves(self, grid):
        color = self.color
        index = self.index
        legal_moves = set()

        is_check = grid.is_check(color)
        is_protecting = grid.check[self.color][index] and grid.check[self.color][grid.check_piece[self.color]]

        for step in self.normal_steps:
            x, y = index % 8, index // 8
            if -1 < x + step[0] < 8 and -1 < y + step[1] < 8:

                next_index = index + step[1] * 8 + step[0]

                if (not is_check or grid.check[color][next_index]) and (
                        not is_protecting or grid.check[color][next_index]):
                    if next_index not in grid:
                        legal_moves.add(next_index)

        for step in self.killer_steps:

            x, y = index % 8, index // 8
            if -1 < x + step[0] < 8 and -1 < y + step[1] < 8:

                next_index = index + step[1] * 8 + step[0]

                if (not is_check or grid.check[color][next_index]) and (not is_protecting or grid.check[color][next_index]):
                    self.danger.add(next_index)
                    if next_index in grid.pieces[1 - self.color]:

                        legal_moves.add(next_index)

                        if next_index == grid.check_piece[1 - color]:
                            self.check.add(next_index)
                            self.check.add(index)

        return legal_moves