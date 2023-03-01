"""
###############################################################################

    Author        :   abelaro
    Copyright     :   2023

    Description   :   
        Source file for board implementations and definitions.

###############################################################################
"""
from enum import IntEnum, auto
from hexapawn.pawn import Position, Color, Pawn

SIZE = 3
"""Hexapawn size"""

class MovePawnResult(IntEnum):
    """
    To indicate result of pawn movement regarding winner declaration.
    """
    NO_WINNER   = auto()
    WHITE_WIN   = auto()
    BLACK_WIN   = auto()

class Board():
    """
    Board containing pawns.
    """

    def __init__(self) -> None:

        self._whitePawns = []
        self._blackPawns = []
        
        self.resetPawns()

    def _getPawnInPosition(self,position:Position)->Pawn:
        """
        Gets the pawn in specified position.
        
        Parameter
        ---------
        position : Position
            Position to get pawn from.

        Returns
        ---------
        Pawn : Pawn in position. None if there is no pawn in position.
        """
        res = None
        allPawns = self._whitePawns + self._blackPawns
        for pawn in allPawns:
            if pawn.inPosition(position):
                res = pawn
                break
        return res
    
    def _checkForWinner(self,movedPawn:Pawn)->MovePawnResult:
        """
        Checks for winner based on current pawns in board.
        
        Parameter
        ---------
        movedPawn : Pawn
            Recently moved pawn.

        Returns
        ---------
        - MovePawnResultPawn.WHITE_WIN : \n
                If all black pawns are taken out or recenly moved white pawn reaches other side.\n
        - MovePawnResultPawn.BLACK_WIN : \n
                If all white pawns are taken out or recenly moved black pawn reaches other side.\n
        - MovePawnResultPawn.NO_WINNER : \n
                No winner from last pawn movement.
        """
        res = MovePawnResult.NO_WINNER
        if movedPawn.color == Color.WHITE:
            if len(self._blackPawns) == 0:
                # all black pawns eliminated
                res = MovePawnResult.WHITE_WIN
            elif movedPawn.position.row == 0:
                # white pawn reaches other side
                res = MovePawnResult.WHITE_WIN
        else:
            if len(self._whitePawns) == 0:
                # all white pawns eliminated
                res = MovePawnResult.BLACK_WIN
            elif movedPawn.position.row == SIZE-1:
                # black pawn reaches other side
                res = MovePawnResult.BLACK_WIN
        return res

    ######################################################################
    #                          public functions                          #
    ######################################################################

    def getTilePositions(self)->list:
        """
        Retruens a 2D list representing pawn positions.

        Returns
        ---------
        - list : 2D list of pawns. None value indicates empty tile.
        """
        allPawns = self._whitePawns + self._blackPawns
        positions = []
        for row in range(SIZE):
            positions.append([None] * SIZE)
            for col in range(SIZE):
                pawn = next((x for x in allPawns \
                             if x.position.row == row and \
                                x.position.col == col), 
                             None)
                positions[row][col] = pawn
        return positions

    def movePawn(self,pawn:Pawn,newPosition:Position)->MovePawnResult:
        """
        Moves pawn and checks for winner based on movement result.
        
        Parameter
        ---------
        pawn : Pawn
            Pawn to move.
        newPosition : Position
            New position the pawn will move to.

        Returns
        ---------
        - MovePawnResultPawn.WHITE_WIN : \n
                If all black pawns are taken out or recenly moved white pawn reaches other side.\n
        - MovePawnResultPawn.BLACK_WIN : \n
                If all white pawns are taken out or recenly moved black pawn reaches other side.\n
        - MovePawnResultPawn.NO_WINNER : \n
                No winner from last pawn movement.
        """
        pawnInPosition = self._getPawnInPosition(newPosition)
        if not pawnInPosition == None:
            # taking rival pawn
            if pawn.color == Color.WHITE:
                assert pawnInPosition.color == Color.BLACK, "Invalid move."
                # delete pawn
                self._blackPawns = [x for x in self._blackPawns\
                                    if not x.inPosition(newPosition)]
            else:
                assert pawnInPosition.color == Color.WHITE, "Invalid move."
                # delete pawn
                self._whitePawns = [x for x in self._whitePawns\
                                    if not x.inPosition(newPosition)]
        
        pawn.position.row = newPosition.row
        pawn.position.col = newPosition.col

        # check for winning
        return self._checkForWinner(pawn)
    
    def resetPawns(self)->None:
        """
        Resets pawns.
        """
        self._whitePawns = [
            Pawn(Color.WHITE,Position(2,0)),
            Pawn(Color.WHITE,Position(2,1)),
            Pawn(Color.WHITE,Position(2,2))
        ]
        self._blackPawns = [
            Pawn(Color.BLACK,Position(0,0)),
            Pawn(Color.BLACK,Position(0,1)),
            Pawn(Color.BLACK,Position(0,2))
        ]
