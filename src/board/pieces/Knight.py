from src.board.pieces.StaticPiece import StaticPiece
from os import getcwd

class Knight(StaticPiece):
    def __init__(self, color, index):
        sprite = f"{getcwd()}/assets/pieces/{'white' if color==0 else 'black'}_knight.png"
        super().__init__(type=1, color=color, index=index, steps=[(2,1),(-2,1),(2,-1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)], sprite=sprite)