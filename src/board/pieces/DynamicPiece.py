from src.board.pieces.Piece import Piece

class DynamicPiece(Piece):

    def __init__(self, color, index, type, steps, sprite):
        super().__init__(color=color, type=type, index=index, steps=steps, sprite=sprite)
        self.steps = steps

    def legal_moves(self, grid):

        legal_moves = set()

        is_check = grid.is_check(self.color)
        is_protecting = grid.check[self.color][self.index] and grid.check[self.color][grid.check_piece[self.color]]

        for step in self.steps:
            x, y = self.index % 8, self.index // 8
            first, second = None, None

            while -1 < x + step[0] < 8 and -1 < y + step[1] < 8 and second is None:
                x += step[0]
                y += step[1]

                next_index = x + 8*y

                if next_index in grid:

                    if first is None:
                        self.danger.add(next_index)
                        if (not is_check or grid.check[self.color][next_index]) and (not is_protecting or grid.check[self.color][next_index]):
                            if next_index in grid.pieces[1 - self.color]:
                                legal_moves.add(next_index)

                    if first is None:
                        first = next_index

                    elif second is None:
                        second = next_index

                else:
                    if (not is_check or grid.check[self.color][next_index]) and (not is_protecting or grid.check[self.color][next_index]):
                        if first is None:
                            legal_moves.add(next_index)
                            self.danger.add(next_index)

            if first == grid.check_piece[1 - self.color] or second == grid.check_piece[1 - self.color]:
                if second is None:
                    second = x + 8 * y
                index_step = step[0] + 8*step[1]
                while second != self.index:
                    self.check.add(second)
                    second -= index_step
                self.check.add(second)

        return legal_moves