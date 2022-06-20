from src.board.pieces.PawnoidPiece import PawnoidPiece
from os import getcwd

class Pawn(PawnoidPiece):

    def __init__(self, color, index):
        sprite = f"{getcwd()}/assets/pieces/{'white' if color == 0 else 'black'}_pawn.png"
        super().__init__(color=color, type=0, index=index, normal_steps=[(0,1)], killer_steps= [(1,1),(-1,1)], sprite=sprite)