"""
###############################################################################

    Author        :   abelaro
    Copyright     :   2023

    Description   :   
        Source file for pawn implementations and definitions.

###############################################################################
"""
from enum import Enum
from PyQt5.QtCore import Qt

class Color(Enum):
    """
    Pawn color.
    """
    WHITE = Qt.white
    BLACK = Qt.black

class Position():
    """
    Indicator of pawn position in board.
    """
    def __init__(self,row,col) -> None:
        """
        """
        self.row = row
        self.col = col

class Pawn():
    """
    Pawn.
    """
    def __init__(self,color:Color,position:Position) -> None:
        self.color = color
        self.position = position

    def inPosition(self,position:Position)->bool:
        """
        Checks if pawn is in specified position.
        
        Parameter
        ---------
        position : Position
            Position to test with.

        Returns
        ---------
        - True  : Pawn position is equal
        - False : Pawn position is not equal
        """
        return True if self.position.row == position.row\
            and self.position.col == position.col\
            else False
