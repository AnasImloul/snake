from src.board.pieces.DynamicPiece import DynamicPiece
from os import getcwd

class Queen(DynamicPiece):
    def __init__(self, color, index):
        sprite = f"{getcwd()}/assets/pieces/{'white' if color==0 else 'black'}_queen.png"
        super().__init__(type=4, color=color, index=index, steps=[(1,1),(1,-1),(-1,1),(-1,-1),(0,1),(0,-1),(1,0),(-1,0)], sprite=sprite)