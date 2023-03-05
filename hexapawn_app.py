"""
###############################################################################

    Author        :   abelaro
    Copyright     :   2023

    Description   :   
        Main source file for 3x3 hexapawn application.
        Uses PyQt5 module for UIs.

        Contains main to execute application.

###############################################################################
"""
import random
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout

from hexapawn.game_manager import *
from hexapawn.board import *
from hexapawn.computer import *
from hexapawn.draw_util import DrawUtil

from hexapawn_ui import Ui_widgetHexapawn

class HexapawnApp():
    """
    Hexpawn application.
    """

    def __init__(self) -> None:

        self._widgetHexapawn = QtWidgets.QWidget()
        self._widgetHexapawn.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | 
            QtCore.Qt.WindowMinimizeButtonHint)
        self._ui = Ui_widgetHexapawn()
        self._ui.setupUi(self._widgetHexapawn)

        self._gameManager = GameManager()
        self._board = Board()
        self._buttonMap = []
        self._computer = Computer()
        self._currentBox = None
        self._recordedMoves = []

        self._selectedPawnPosition = None

        self._setupTiles()
        self._ui.btnReset.clicked.connect(self._reset)
        self._ui.btnMoveRandomSelect.clicked.connect(self._moveRandomSelect)
        self._ui.btnResetIntelligence.clicked.connect(self._resetIntelligence)
    
        DrawUtil.drawBoard(self._buttonMap,self._board,self._selectedPawnPosition)
        DrawUtil.drawPlayerMoveInfo(self._ui,self._gameManager.turnPlayer)
        DrawUtil.drawBox(self._ui,self._currentBox,self._selectMove)

        self._setComputerMoveUi()

    def _setupTiles(self)->None:
        """
        Setups board tiles by assigning corresponding button callbacks.
        Each callback passes the equivalent position for each button.
        """
        self._buttonMap = [
            [ self._ui.btnPawn0, self._ui.btnPawn1, self._ui.btnPawn2 ],
            [ self._ui.btnPawn3, self._ui.btnPawn4, self._ui.btnPawn5 ],
            [ self._ui.btnPawn6, self._ui.btnPawn7, self._ui.btnPawn8 ]
        ]
        self._ui.btnPawn0.clicked.connect(
            lambda event:self._boardTileClicked(event,Position(0,0)))
        self._ui.btnPawn1.clicked.connect(
            lambda event:self._boardTileClicked(event,Position(0,1)))
        self._ui.btnPawn2.clicked.connect(
            lambda event:self._boardTileClicked(event,Position(0,2)))
        self._ui.btnPawn3.clicked.connect(
            lambda event:self._boardTileClicked(event,Position(1,0)))
        self._ui.btnPawn4.clicked.connect(
            lambda event:self._boardTileClicked(event,Position(1,1)))
        self._ui.btnPawn5.clicked.connect(
            lambda event:self._boardTileClicked(event,Position(1,2)))
        self._ui.btnPawn6.clicked.connect(
            lambda event:self._boardTileClicked(event,Position(2,0)))
        self._ui.btnPawn7.clicked.connect(
            lambda event:self._boardTileClicked(event,Position(2,1)))
        self._ui.btnPawn8.clicked.connect(
            lambda event:self._boardTileClicked(event,Position(2,2)))
        
    def _setComputerMoveUi(self,enabled:bool=None)->None:
        """
        Enables or disables computer move ui.

        Parameter
        ---------
        enabled : bool
            Boolean for enable. If None, enable if turn of Black player.
        """
        if enabled == None:
            enabled = True if self._gameManager.turnPlayer == Player.BLACK else False
        self._ui.grpMoves.setEnabled(enabled)
        self._ui.btnMoveRandomSelect.setEnabled(enabled)

    def _selectMove(self,move:Move)->None:
        """
        Selects a move for black.

        Parameter
        ---------
        move : Move
            Move selected. Cannot be None.
        """
        assert not move == None and type(move) == Move
        self._recordedMoves.append(MoveRecord(self._gameManager.turn,move))
        tilePositions = self._board.getTilePositions()
        blackPawnToMove = tilePositions[move.position.row][move.position.col]
        newPosition = move.newPosition()
        self._movePawn(blackPawnToMove,newPosition)
        DrawUtil.drawBoard(self._buttonMap,self._board,self._selectedPawnPosition)

    def _moveRandomSelect(self)->None:
        """
        Selects a random move for black to execute.\n

        Precondition: It is turn of black and there is current box.\n
        """
        assert self._gameManager.turnPlayer == Player.BLACK
        assert not self._currentBox == None
        remainingMoves = list(filter(lambda m : not m.removed,self._currentBox.moves))
        move = None
        if len(remainingMoves) > 0:
            rand = random.choice(range(len(remainingMoves)))
            move = remainingMoves[rand]
            self._selectMove(move)
        else:
            # move manually
            pass

    def _nextPlayer(self)->None:
        """
        Sets next player. Clears selection and update UIs.
        """
        self._selectedPawnPosition = None
        self._gameManager.nextPlayer()
        DrawUtil.drawPlayerMoveInfo(self._ui,self._gameManager.turnPlayer)
        if self._gameManager.turnPlayer == Player.BLACK:
            self._currentBox = self._computer.getBoxForCurrentBlackTurn(
                self._gameManager.turn,
                self._board)
        DrawUtil.drawBox(self._ui,self._currentBox,self._selectMove)
        self._setComputerMoveUi()

    def _removeMoveCausingBlackPlayerLose(self)->MoveRecord:
        """
        Finds the latest move record causing black player lost that is not yet
        tagged as removed move.

        Returns
        ---------
        MoveRecord : Move record with move causing black player lost. None if not found.
        """
        moveRecord = None
        if len(self._recordedMoves)>0:
            for recordedMove in reversed(self._recordedMoves):
                if not recordedMove.move.removed:
                    moveRecord = recordedMove
                    break
        return moveRecord

    def _declareWinner(self,winner:Player)->None:
        """
        Declare winner.
        """
        self._gameManager.endGame()
        DrawUtil.drawWinnerInfo(self._ui,self._gameManager)
        # update result
        index = self._ui.tableResults.rowCount()
        self._ui.tableResults.setRowCount(index + 1)
        winDetails = winner.name
        if winner == Player.WHITE and len(self._recordedMoves)>0:
            moveRecord = self._removeMoveCausingBlackPlayerLose()
            if not moveRecord == None:
                winDetails = "{} : Removed {} for turn {}."\
                    .format(winDetails,moveRecord.move.color.name,moveRecord.turn)
                moveRecord.move.remove()
        item = QtWidgets.QTableWidgetItem()
        item.setText(winDetails)
        self._ui.tableResults.setItem(index, 0, item)        

    def _findMoveInCurrentBox(self,pawn:Pawn,newPosition:Position)->None:
        """
        Finds the equivalent move in current box.
        The equivalent move will be set to last move,
        will be used to remmove the move if it resulted to lost.

        Parameter
        ---------
        pawn : Pawn
            Pawn to be moved.
        newPosition: Position
            New position of moved pawn
        """
        # Find move to evaluate
        for move in self._currentBox.moves:
            if pawn.inPosition(move.position) and\
                arePositionsEqual(move.newPosition(),newPosition):
                self._recordedMoves.append(MoveRecord(self._gameManager.turn,move))
                break

    def _movePawn(self,pawn:Pawn,newPosition:Position)->None:
        """
        Moves pawn. Also handles setting of next player and
        checking of winner. Ends the game if winner is declared.

        Parameter
        ---------
        pawn : Pawn
            Pawn to be moved.
        newPosition: Position
            New position of moved pawn
        """
        assert not pawn == None
        assert not newPosition == None
        if pawn.color == Color.BLACK:
            if not self._currentBox == None:
                # Find move to evaluate
                self._findMoveInCurrentBox(pawn,newPosition)
        res = self._board.movePawn(pawn,newPosition)
        if res == MovePawnResult.NO_WINNER:
            self._nextPlayer()
        elif res == MovePawnResult.INVALID:
            # do nothing
            pass
        else:
            # has winnner
            self._setComputerMoveUi(False)
            winner = None
            if res == MovePawnResult.WHITE_WIN:
                winner = Player.WHITE
            elif res == MovePawnResult.BLACK_WIN:
                winner = Player.BLACK
            self._declareWinner(winner)
        
    def _handleSelectedPawnMovement(
            self,
            pawnInSelectedPosition:Pawn,
            clickedTilePosition:Position,
            pawnInClickedTile:Pawn,
            pawnClickedMatchedTurnPlayer:bool)->None:
        """
        Handles selected pawn movement.\n

        Precondition: Selected position contains pawn.\n
        Parameter
        ---------
        pawnInSelectedPosition : Pawn
            Pawn in selected position. Can not be None.
        clickedTilePosition: Position
            Position of clicked tile
        pawnInClickedTile : Pawn
            Pawn in clicked tile. Can be None indicating tile clicked is empty.
        """
        assert not pawnInSelectedPosition == None,\
            "Selected position does not contain pawn"
        if not pawnInClickedTile == None:
            if arePositionsEqual(self._selectedPawnPosition,clickedTilePosition):
                # deselect since selected pawn reselected
                self._selectedPawnPosition = None
            else:
                if pawnClickedMatchedTurnPlayer:
                    # update selected
                    self._selectedPawnPosition = clickedTilePosition
                else:
                    # pawn movement taking rival pawn
                    if not pawnInSelectedPosition == None:
                        self._movePawn(pawnInSelectedPosition,clickedTilePosition)
        else:
            # pawn movement to empty slot
            if not pawnInSelectedPosition == None:
                self._movePawn(pawnInSelectedPosition,clickedTilePosition)
            
    def _boardTileClicked(self,event,clickedTilePosition:Position)->None:
        """
        Callback when board tile is clicked.\n
        Handles pawn selection/deselection and movement.

        Parameter
        ---------
        event : Any
            Not used.
        clickedTilePosition : Position
            Indicator parameter of which tile was clicked. See initialization
            of board tiles in __init__.
        """
        if not self._gameManager.ended:
            tilePositions = self._board.getTilePositions()
            pawnInClickedTile = tilePositions[clickedTilePosition.row][clickedTilePosition.col]
            pawnClicked = True if not pawnInClickedTile == None else False
            pawnClickedMatchedTurnPlayer = False
            if pawnClicked:
                turnPlayer = self._gameManager.turnPlayer
                pawnClickedMatchedTurnPlayer = \
                    (turnPlayer == Player.WHITE and\
                        pawnInClickedTile.color == Color.WHITE) or\
                    (turnPlayer == Player.BLACK and\
                        pawnInClickedTile.color == Color.BLACK)
            redrawBoard = True
            if not self._selectedPawnPosition == None:
                selectedRow = self._selectedPawnPosition.row
                selectedCol = self._selectedPawnPosition.col
                pawnInSelectedPosition = tilePositions[selectedRow][selectedCol]
                self._handleSelectedPawnMovement(
                    pawnInSelectedPosition,
                    clickedTilePosition,
                    pawnInClickedTile,
                    pawnClickedMatchedTurnPlayer)
            else:
                # no selected pawn
                if pawnClickedMatchedTurnPlayer:
                    # set selected
                    self._selectedPawnPosition = clickedTilePosition
                else:
                    # attemmpt to select rival pawn
                    redrawBoard = False
            if redrawBoard:
                DrawUtil.drawBoard(self._buttonMap,self._board,self._selectedPawnPosition)

    def _reset(self):
        """
        Resets hexapawn.
        """
        print("Reset game...")
        self._board.resetPawns()
        self._gameManager.reset()
        self._selectedPawnPosition = None
        self._currentBox = None
        self._recordedMoves = []

        DrawUtil.drawBoard(self._buttonMap,self._board,self._selectedPawnPosition)
        DrawUtil.drawPlayerMoveInfo(self._ui,self._gameManager.turnPlayer)
        DrawUtil.drawWinnerInfo(self._ui,self._gameManager)
        DrawUtil.drawBox(self._ui,self._currentBox,self._selectMove)

    def _resetIntelligence(self):
        """
        Resets intelligence.
        """
        self._ui.tableResults.setRowCount(0)
        self._computer.resetIntelligence()
        self._reset()

    ######################################################################
    #                          public functions                          #
    ######################################################################

    def show(self)->None:
        """
        Show hexapawn application.
        """
        self._widgetHexapawn.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    hexapawnApp = HexapawnApp()
    hexapawnApp.show()
    sys.exit(app.exec_())
 