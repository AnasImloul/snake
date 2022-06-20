from src.board.pieces.DynamicPiece import DynamicPiece
from os import getcwd

class Rook(DynamicPiece):
    def __init__(self, color, index):
        sprite = f"{getcwd()}/assets/pieces/{'white' if color==0 else 'black'}_rook.png"
        super().__init__(type=3, color=color, index=index, steps=[(0,1),(0,-1),(1,0),(-1,0)], sprite=sprite)