from src.board.pieces.CheckPiece import CheckPiece
from os import getcwd

class King(CheckPiece):
    def __init__(self, color, index):
        sprite = f"{getcwd()}/assets/pieces/{'white' if color == 0 else 'black'}_king.png"
        super().__init__(color=color, type=5, index=index, steps=[(1,1),(-1,1),(1,-1),(-1,-1),(1,0),(0,-1),(0,1),(-1,0)], sprite=sprite)