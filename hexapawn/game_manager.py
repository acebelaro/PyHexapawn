"""
###############################################################################

    Author        :   abelaro
    Copyright     :   2023

    Description   :   
        Source file for Game manager implementations and definitions.

###############################################################################
"""
from enum import IntEnum, auto

class Player(IntEnum):
    """
    Player options.
    """
    WHITE = auto()
    BLACK = auto()

FIRST_PLAYER_TO_MOVE = Player.WHITE
"""First player to move."""

class GameManager():
    """
    Game manager.
    """
    turnPlayer = FIRST_PLAYER_TO_MOVE
    """Player making move."""

    ended = False
    """Game end flag."""

    winner = None
    """Winning player"""

    def __init__(self) -> None:
        self.reset()

    ######################################################################
    #                          public functions                          #
    ######################################################################

    def nextPlayer(self)->None:
        """
        Switched to next player making move.
        """
        self.turnPlayer = Player.BLACK if\
            self.turnPlayer == Player.WHITE\
            else Player.WHITE
        
    def endGame(self)->None:
        """
        Ends game.
        """
        self.ended = True
        self.winner = self.turnPlayer

    def reset(self)->None:
        """
        Resets game.
        """
        self.turnPlayer = FIRST_PLAYER_TO_MOVE
        self.ended = False
        self.winner = None
