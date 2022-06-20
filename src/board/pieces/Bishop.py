from src.board.pieces.DynamicPiece import DynamicPiece
from os import getcwd

class Bishop(DynamicPiece):
    def __init__(self, color, index):
        sprite = f"{getcwd()}/assets/pieces/{'white' if color==0 else 'black'}_bishop.png"
        super().__init__(type=2, color=color, index=index, steps=[(1,1),(1,-1),(-1,1),(-1,-1)], sprite=sprite)