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
from functools import partial
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QScrollArea

from hexapawn.game_manager import *
from hexapawn.board import *
from hexapawn.computer import *
from hexapawn.draw_util import DrawUtil

TILE_SIZE               = 101
CURRENT_BOX_BOARD       = 200

class TileButton(QtWidgets.QPushButton):
    
    def __init__(self,row,col,tileSelectCallback):
        super().__init__()
        clicked = lambda event,position=Position(row,col):\
            tileSelectCallback(position)
        self.clicked.connect(clicked)

        self.setFixedHeight(TILE_SIZE)
        self.setFixedWidth(TILE_SIZE)

class Hexapawn():
    """
    """

    def __init__(self) -> None:
        self._widgetMain = QtWidgets.QWidget()
        self._widgetMain.layout = QtWidgets.QGridLayout(self._widgetMain)
     
        self._gameManager = GameManager()
        self._computer = Computer()
        self._board = Board()
        self._mainBoardButtons = []
        self._selectedPawnPosition = None
        self._currentBox = None
        self._recordedMoves = []
        
        # Main Board
        self._grpBoxMainBoard = QtWidgets.QGroupBox()
        self._grpBoxMainBoard.layout = QtWidgets.QGridLayout(self._grpBoxMainBoard)
        self._grpBoxMainBoard.layout.setSpacing(0)

        # Player Information
        self._grpBoxPlayerInformation = QtWidgets.QGroupBox()
        self._grpBoxPlayerInformation.layout = QtWidgets.QHBoxLayout(self._grpBoxPlayerInformation)
        self._lblPlayerInfo = QtWidgets.QLabel(text="Player to Move: ")
        self._btnPlayerInfo = QtWidgets.QPushButton()
        self._btnReset = QtWidgets.QPushButton(text="Reset")

        self._grpBoxPlayerInformation.layout.addWidget(self._lblPlayerInfo)
        self._grpBoxPlayerInformation.layout.addWidget(self._btnPlayerInfo)
        self._grpBoxPlayerInformation.layout.addWidget(self._btnReset)

        # Current Box Information
        self._grpBoxCurrentBoxInfo = QtWidgets.QGroupBox()
        self._grpBoxCurrentBoxInfo.layout = QtWidgets.QVBoxLayout(self._grpBoxCurrentBoxInfo)
        self._btnCurrentBoxBoard = QtWidgets.QPushButton()
        self._btnCurrentBoxBoard.setFixedSize(QtCore.QSize(CURRENT_BOX_BOARD,CURRENT_BOX_BOARD))
        self._btnRandomMove = QtWidgets.QPushButton("Random")
        self._grpBoxMoves = QtWidgets.QGroupBox()
        self._grpBoxMoves.layout = QtWidgets.QVBoxLayout(self._grpBoxMoves)
        # self._grpBoxMoves.layout.setSpacing(0)

        self._grpBoxCurrentBoxInfo.layout.addWidget(self._btnCurrentBoxBoard)
        self._grpBoxCurrentBoxInfo.layout.addWidget(self._grpBoxMoves)
        self._grpBoxCurrentBoxInfo.layout.addStretch()
        self._grpBoxCurrentBoxInfo.layout.addWidget(self._btnRandomMove)

        # Record
        self._grpBoxRecord = QtWidgets.QGroupBox()
        self._grpBoxRecord.setFixedWidth(300)
        self._grpBoxRecord.layout = QtWidgets.QVBoxLayout(self._grpBoxRecord)
        self._tableResults = QtWidgets.QTableWidget()
        columns = ["Winner"]
        self._tableResults.setColumnCount(len(columns))
        self._tableResults.setHorizontalHeaderLabels(columns)
        self._tableResults.horizontalHeader().setStretchLastSection(True)
        self._tableResults.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self._grpBoxRecord.layout.addWidget(self._tableResults)
        self._btnResetIntelligence = QtWidgets.QPushButton(text="Reset Intelligence")
        self._grpBoxRecord.layout.addWidget(self._btnResetIntelligence)

        # Box informations
        self._grpBoxBoxes = QtWidgets.QGroupBox()
        
        # Assemble
        self._widgetMain.layout.addWidget(self._grpBoxMainBoard,0,0)
        self._widgetMain.layout.addWidget(self._grpBoxCurrentBoxInfo,0,1,2,1)
        self._widgetMain.layout.addWidget(self._grpBoxRecord,0,2,2,1)
        self._widgetMain.layout.addWidget(self._grpBoxPlayerInformation,1,0)

        self._setupMainBoard()
        self._btnReset.clicked.connect(self._reset)
        self._btnRandomMove.clicked.connect(self._moveRandomSelect)
        self._btnResetIntelligence.clicked.connect(self._resetIntelligence)
    
        DrawUtil.drawMainBoard(self._mainBoardButtons,self._board,self._selectedPawnPosition)
        DrawUtil.drawPlayerMoveInfo(self._btnPlayerInfo,self._gameManager.turnPlayer)
        DrawUtil.drawCurrentBox(self._btnCurrentBoxBoard,self._grpBoxMoves,self._currentBox,self._selectMove)
        DrawUtil.drawBoxes(self._grpBoxBoxes,self._computer)
        self._setComputerMoveUi()

        scrollArea = QScrollArea()
        scrollArea.setWidget(self._grpBoxBoxes)
        self._widgetMain.layout.addWidget(scrollArea,2,0,1,3)

    def _setupMainBoard(self):
        """
        """
        for row in range(SIZE):
            oneRow = []
            for col in range(SIZE):
                btnTile = TileButton(row,col,self._boardTileClicked)
                oneRow.append(btnTile)
                self._grpBoxMainBoard.layout.addWidget(btnTile,row,col)
            self._mainBoardButtons.append(oneRow)
        
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
        self._grpBoxMoves.setEnabled(enabled)
        self._btnRandomMove.setEnabled(enabled)

    def _recordMove(self,move:Move)->None:
        """
        Records move.

        Parameter
        ---------
        move : Move
            Move to record.
        """
        newMoveRecord = MoveRecord(self._currentBox,move)
        self._recordedMoves.append(newMoveRecord)

    def _selectMove(self,move:Move)->None:
        """
        Selects a move for black.

        Parameter
        ---------
        move : Move
            Move selected. Cannot be None.
        """
        assert not move == None and type(move) == Move
        self._recordMove(move)
        tilePositions = self._board.getTilePositions()
        blackPawnToMove = tilePositions[move.position.row][move.position.col]
        newPosition = move.newPosition()
        self._movePawn(blackPawnToMove,newPosition)
        DrawUtil.drawMainBoard(self._mainBoardButtons,self._board,self._selectedPawnPosition)

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
        DrawUtil.drawPlayerMoveInfo(self._btnPlayerInfo,self._gameManager.turnPlayer)
        if self._gameManager.turnPlayer == Player.BLACK:
            self._currentBox = self._computer.getBoxForCurrentBlackTurn(
                self._gameManager.turn,
                self._board)
        DrawUtil.drawCurrentBox(self._btnCurrentBoxBoard,self._grpBoxMoves,self._currentBox,self._selectMove)
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
        DrawUtil.drawWinnerInfo(self._lblPlayerInfo,self._gameManager)
        # update result
        index = self._tableResults.rowCount()
        self._tableResults.setRowCount(index + 1)
        winDetails = winner.name
        if winner == Player.WHITE and len(self._recordedMoves)>0:
            moveRecord = self._removeMoveCausingBlackPlayerLose()
            if not moveRecord == None:
                winDetails = "{} : Removed {} for from {}."\
                    .format(winDetails,moveRecord.move.color.name,moveRecord.box.id)
                moveRecord.move.remove()
        item = QtWidgets.QTableWidgetItem()
        item.setText(winDetails)
        self._tableResults.setItem(index, 0, item)

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
                self._recordMove(move)
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
            
    def _boardTileClicked(self,clickedTilePosition:Position)->None:
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
                DrawUtil.drawMainBoard(self._mainBoardButtons,self._board,self._selectedPawnPosition)
            DrawUtil.drawBoxes(self._grpBoxBoxes,self._computer)

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
        self._setComputerMoveUi()

        DrawUtil.drawMainBoard(self._mainBoardButtons,self._board,self._selectedPawnPosition)
        DrawUtil.drawPlayerMoveInfo(self._btnPlayerInfo,self._gameManager.turnPlayer)
        DrawUtil.drawWinnerInfo(self._lblPlayerInfo,self._gameManager)
        DrawUtil.drawCurrentBox(self._btnCurrentBoxBoard,self._grpBoxMoves,self._currentBox,self._selectMove)

    def _resetIntelligence(self):
        """
        Resets intelligence.
        """
        self._tableResults.setRowCount(0)
        self._computer.resetIntelligence()
        self._reset()
        DrawUtil.drawBoxes(self._grpBoxBoxes,self._computer)

    ######################################################################
    #                          public functions                          #
    ######################################################################

    def show(self)->None:
        """
        Show hexapawn application.
        """
        self._widgetMain.show()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    hexapawnApp = Hexapawn()
    hexapawnApp.show()
    sys.exit(app.exec_())
 