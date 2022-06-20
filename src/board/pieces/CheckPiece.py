from src.board.pieces.StaticPiece import StaticPiece


class CheckPiece(StaticPiece):

    def __init__(self, type, color, index, steps, sprite):
        super().__init__(type=type, color=color, index=index, steps=steps, sprite=sprite)

    def legal_moves(self, grid):
        legal_moves = set()

        for step in self.steps:
            x, y = self.index % 8, self.index // 8
            if -1 < x + step[0] < 8 and -1 < y + step[1] < 8:

                next_index = self.index + step[1] * 8 + step[0]

                self.danger.add(next_index)

                if not grid.danger[self.color][next_index]:
                    if next_index in grid.pieces[1 - self.color]:
                        if grid.check[self.color][next_index] <= 1:
                            legal_moves.add(next_index)

                        if next_index == grid.check_piece[1 - self.color]:
                            self.check.add(next_index)
                            self.check.add(self.index)

                    elif next_index not in grid.pieces[self.color]:
                        if not grid.check[self.color][next_index]:
                            legal_moves.add(next_index)

        return legal_moves

    def move(self, grid, next_index):
        if super().move(grid, next_index):
            grid.check_piece[self.color] = next_index

    def undo(self, grid):


        if super().undo(grid):
            grid.check_piece[self.color] = self.index
            return True

        return False
