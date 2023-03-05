"""
###############################################################################

    Author        :   abelaro
    Copyright     :   2023

    Description   :   
        Source file for board implementations and definitions.

###############################################################################
"""
from enum import Enum, IntEnum, auto
import math
from types import MethodType
from PyQt5.QtCore import Qt

SIZE = 3
"""Hexapawn size"""

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
        assert row>=0 and row<SIZE, "Invalid row."
        assert col>=0 and col<SIZE, "Invalid col."

        self.row = row
        self.col = col

def arePositionsEqual(positionA:Position,positionB:Position)->None:
    """
    Checks two positions are equal
    
    Parameter
    ---------
    positionA : Position
    positionB : Position

    Returns
    ---------
    - True  : Positions are equal
    - False : Positions are not equal
    """
    assert not positionA == None and type(positionA) == Position
    assert not positionB == None and type(positionB) == Position
    return True if positionA.row == positionB.row and\
        positionA.col == positionB.col\
            else False

class Pawn():
    """
    Pawn.
    """
    def __init__(self,color:Color,position:Position) -> None:
        self.color = color
        self.position = position

    ######################################################################
    #                          public functions                          #
    ######################################################################

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
        return arePositionsEqual(self.position,position)

def arePawnsEqual(aPawns:list,bPawns:list)->bool:
    """
    Checks if two pawn lists are equal.

    Parameter
    ---------
    aPawns : list
        Pawn list A.
    bPawns : list
        Pawn list B.

    Returns
    ---------
    True - list of pawns are equal.
    False - list of pawns are not equal.
    """
    assert type(aPawns) == list and all(type(a)==Pawn for a in aPawns)
    assert type(bPawns) == list and all(type(b)==Pawn for b in bPawns)
    res = False
    if len(aPawns) == len(bPawns):
        res = True
        for aPawn in aPawns:
            bPawn = next((p for p in bPawns \
                            if p.color == aPawn.color and\
                            arePositionsEqual(p.position,aPawn.position)), 
                            None)
            if bPawn == None:
                res = False
                break
    return res

class MovePawnResult(IntEnum):
    """
    To indicate result of pawn movement regarding winner declaration.
    """
    NO_WINNER   = auto()
    WHITE_WIN   = auto()
    BLACK_WIN   = auto()
    INVALID     = auto()

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
    
    def _isMoveValid(
            self,
            pawn:Pawn,
            newPosition:Position,
            pawnInNewPosition:Pawn)->bool:
        """
        Checks if move is valid.\n
        Valid if:\n
            1) Moving forward to empty tile; and\n
            2) Moving diagonally to take rival tile.
        
        Parameter
        ---------
        pawn : Pawn
            Pawn being moved.
        newPosition : Position
            New position of pawn being moved.
        pawnInNewPosition : Pawn
            Pawn in the tile being moved to. Can be None.

        Returns
        ---------
        - True  : move is valid
        - False : move is invalid
        """
        assert not pawn is None
        assert not newPosition is None
        res = False
        moveForwardAdjust = -1\
            if pawn.color == Color.WHITE else 1
        # white pawn moves forward by decrementing row
        # black pawn moves forward by incrementing row
        pawnColorToTake = Color.BLACK\
            if pawn.color == Color.WHITE else Color.WHITE
        # white pawn move must take black pawn
        # black pawn move must take white pawn
        if newPosition.row == (pawn.position.row+(moveForwardAdjust)):
            if newPosition.col == pawn.position.col:
                # just moving forward
                if pawnInNewPosition == None:
                    res = True
            elif newPosition.col == (pawn.position.col-1) or\
                newPosition.col == (pawn.position.col+1):
                # moving diagonal
                if not pawnInNewPosition == None and\
                    pawnInNewPosition.color == pawnColorToTake:
                    # taking rival pawn
                    res = True
        return res

    def _hasPossibleMove(
            self,
            pawns:list,
            pawnColor:Color,
            rowVerifier:MethodType,
            forwardInc:int):
        """
        """
        assert not pawns == None and type(pawns) == list
        assert type(pawnColor) == Color
        assert not rowVerifier == None
        assert type(forwardInc) == int and (forwardInc == 1 or forwardInc == -1)
        pawnColorToTake = Color.WHITE\
            if pawnColor == Color.BLACK else\
                Color.BLACK
        res = False
        for pawn in pawns:
            pawnPosition = pawn.position
            if rowVerifier(pawnPosition.row):
                pawnInFront = self._getPawnInPosition(
                    Position(pawnPosition.row+forwardInc,
                             pawnPosition.col))
                if pawnInFront == None:
                    # can move forward
                    res = True
                    break
                if pawnPosition.col > 0 and pawnPosition.col < (SIZE-1):
                    pawnInDiagonalLeft = self._getPawnInPosition(
                        Position(pawnPosition.row+forwardInc,
                                pawnPosition.col-1))
                    if not pawnInDiagonalLeft == None and\
                        pawnInDiagonalLeft.color == pawnColorToTake:
                        # can move diagonal left to take pawn
                        res = True
                        break
                    pawnInDiagonalRight = self._getPawnInPosition(
                        Position(pawnPosition.row+forwardInc,
                                pawnPosition.col+1))
                    if not pawnInDiagonalRight == None and\
                        pawnInDiagonalRight.color == pawnColorToTake:
                        # can move diagonal right to take pawn
                        res = True
                        break
        return res
    
    def _blackPawnHasPossibleMove(self)->bool:
        """
        Checks if there are possible move for black pawns.

        Returns
        ---------
        - True  : at least one black pawn can move
        - False : no black pawn can move
        """
        rowVerifier = lambda row : row < (SIZE-1)
        return self._hasPossibleMove(self._blackPawns,Color.BLACK,rowVerifier,1)
    
    def _whitePawnHasPossibleMove(self)->bool:
        """
        Checks if there are possible move for white pawns.

        Returns
        ---------
        - True  : at least one white pawn can move
        - False : no white pawn can move
        """
        rowVerifier = lambda row : row > 0
        return self._hasPossibleMove(self._whitePawns,Color.WHITE,rowVerifier,-1)

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
                If all black pawns are taken out or
                recenly moved white pawn reaches other side or
                no more possible move for black.\n
        - MovePawnResultPawn.BLACK_WIN : \n
                If all white pawns are taken out or
                recenly moved black pawn reaches other side or
                no more possible move for white.\n
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
                # check if black can still move pawn
                if self._blackPawnHasPossibleMove() == False:
                    res = MovePawnResult.WHITE_WIN
        else:
            if len(self._whitePawns) == 0:
                # all white pawns eliminated
                res = MovePawnResult.BLACK_WIN
            elif movedPawn.position.row == SIZE-1:
                # black pawn reaches other side
                res = MovePawnResult.BLACK_WIN 
            else:
                # check if white can still move pawn
                if self._whitePawnHasPossibleMove() == False:
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
        list : 2D list of pawns. None value indicates empty tile.
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
        res = MovePawnResult.INVALID
        pawnInNewPosition = self._getPawnInPosition(newPosition)
        if self._isMoveValid(pawn,newPosition,pawnInNewPosition):
            # return MovePawnResult.INVALID
            if not pawnInNewPosition == None:
                # taking rival pawn
                if pawn.color == Color.WHITE:
                    assert pawnInNewPosition.color == Color.BLACK, "Invalid move."
                    # delete pawn
                    self._blackPawns = [x for x in self._blackPawns\
                                        if not x.inPosition(newPosition)]
                else:
                    assert pawnInNewPosition.color == Color.WHITE, "Invalid move."
                    # delete pawn
                    self._whitePawns = [x for x in self._whitePawns\
                                        if not x.inPosition(newPosition)]
            
            pawn.position.row = newPosition.row
            pawn.position.col = newPosition.col

            # check for winning
            res = self._checkForWinner(pawn)
        return res

    def arePawnPositionsSymmetric(self)->bool:
        """
        Check if pawn positions in board are symmetric.

        Returns
        ---------
        True - Symmetric.
        False - Not symmetric.
        """
        res = True
        tilePositions = self.getTilePositions()
        r = math.floor(SIZE/2)
        for row in range(SIZE):
            if not res:
                break
            for col in range(r):
                reversedCol = (SIZE-1)-col
                pawnA = tilePositions[row][col]
                pawnB = tilePositions[row][reversedCol]
                if ( not pawnA == None and pawnB == None) or\
                    ( pawnA == None and not pawnB == None):
                    res = False
                elif not pawnA == None and not pawnB == None:
                    if not (pawnA.color == pawnB.color):
                        res = False
                if not res:
                    break
        return res

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

def areBoardsEqual(boardA:Board,boardB:Board)->bool:
    """
    Checks if two boards are equal.

    Parameter
    ---------
    boardA : Board
    boardB : Board

    Returns
    ---------
    True - Boards are equal.
    False - Boards are not equal.
    """
    assert not boardA == None and isinstance(boardA,Board)
    assert not boardB == None and isinstance(boardB,Board)
    return arePawnsEqual(boardA._whitePawns,boardB._whitePawns) and\
        arePawnsEqual(boardA._blackPawns,boardB._blackPawns)
