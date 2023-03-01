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
from PyQt5 import QtWidgets, QtCore

from hexapawn.game_manager import *
from hexapawn.board import *
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

        self._selectedPawnPosition = None

        self._setupTiles()
        self._ui.btnReset.clicked.connect(self._reset)
    
        DrawUtil.drawBoard(self._buttonMap,self._board,self._selectedPawnPosition)
        DrawUtil.drawPlayerMoveInfo(self._ui,self._gameManager.turnPlayer)

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

    def _nextPlayer(self)->None:
        """
        Sets next player. Clears selection and update UIs.
        """
        self._selectedPawnPosition = None
        self._gameManager.nextPlayer()
        DrawUtil.drawPlayerMoveInfo(self._ui,self._gameManager.turnPlayer)

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
            res = self._board.movePawn(pawn,newPosition)
            if res == MovePawnResult.NO_WINNER:
                self._nextPlayer()
            elif res == MovePawnResult.INVALID:
                # do nothing
                print("Invalid move.")
            else:
                # has winnner
                if res == MovePawnResult.WHITE_WIN:
                    print("WHITE WINS!")
                elif res == MovePawnResult.BLACK_WIN:
                    print("BLACK WINS!")
                self._gameManager.endGame()
                DrawUtil.drawWinnerInfo(self._ui,self._gameManager)

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
            if self._selectedPawnPosition.row == clickedTilePosition.row and\
                self._selectedPawnPosition.col == clickedTilePosition.col:
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
        if self._gameManager.ended:
            return
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
        self._board.resetPawns()
        self._gameManager.reset()
        self._selectedPawnPosition = None

        DrawUtil.drawBoard(self._buttonMap,self._board,self._selectedPawnPosition)
        DrawUtil.drawPlayerMoveInfo(self._ui,self._gameManager.turnPlayer)
        DrawUtil.drawWinnerInfo(self._ui,self._gameManager)

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
 