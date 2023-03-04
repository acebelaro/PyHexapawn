"""
###############################################################################

    Author        :   abelaro
    Copyright     :   2023

    Description   :   
        Source file for drawing utilitity functions.

###############################################################################
"""
import os
from enum import Enum
from types import MethodType

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QVBoxLayout

from hexapawn.game_manager import *
from hexapawn.board import *
from hexapawn.computer import *

from hexapawn_ui import Ui_widgetHexapawn

class TileFillColor(Enum):
    """
    Tile fill color selection.
    """
    NORMAL = Qt.gray
    SELECTED = Qt.blue

BUTTON_ICON_SIZE = 96
PAWN_DRAWING_SIZE = BUTTON_ICON_SIZE - 10
PAWN_ELLIPSE_XY = (BUTTON_ICON_SIZE - PAWN_DRAWING_SIZE)/2

COMPUTER_MOVE_IMG_PATH = "./doc/computer_moves/{}.png"
COMPUTER_MOVE_STYLE = "border-image : url({});"
COMPUTER_MOVE_CLEAR_STYLE = "background-color: rgb(255, 255, 255);"

class MoveButton(QtWidgets.QPushButton):
    """
    Move button.
    """

    def __init__(self,move:Move,moveSelectFunc:MethodType) -> None:
        """
        Parameter
        ---------
        move : Move
            Move for this button.
        moveSelectFunc : MethodType
            Callback when move is selected.
        """
        assert not move == None and type(move) == Move
        assert not moveSelectFunc == None and type(moveSelectFunc) == MethodType
        super().__init__()
        self.move = move
        self.moveSelectFunc = moveSelectFunc
        self.clicked.connect(self._clicked)
        self.setStyleSheet("background-color : {}".format(move.color.value))

    def _clicked(self)->None:
        """
        Callback when move button is clicked.
        """
        self.moveSelectFunc(self.move)

class DrawUtil():
    """
    Draw utility.
    """
    @staticmethod
    def _drawTile(
            button:QtWidgets.QPushButton,
            pawn:Pawn,
            selected:bool)->None:
        """
        Draws tile by updating target button icon.
        
        Parameter
        ---------
        button : QtWidgets.QPushButton
            Button for the tile.
        pawn : Pawn
            Pawn for the current tile. None if there is no pawn.
        selected : bool
            Indication if tile is currently selected.
        """
        size = QSize(BUTTON_ICON_SIZE,BUTTON_ICON_SIZE)
        pixmap = QPixmap(size)
        pixmap.fill(TileFillColor.NORMAL.value)
        if not pawn == None:
            if selected:
                pixmap.fill(TileFillColor.SELECTED.value)
            painter = QPainter(pixmap)
            painter.setPen(Qt.black)
            painter.setBrush(pawn.color.value)
            painter.drawEllipse(
                PAWN_ELLIPSE_XY,
                PAWN_ELLIPSE_XY,
                PAWN_DRAWING_SIZE,
                PAWN_DRAWING_SIZE)
            painter.end()
        button.setIcon(QtGui.QIcon(pixmap))
        button.setIconSize(size)

    @staticmethod
    def _clearLayout(layout):
        """
        Clears layout.
        
        Parameter
        ---------
        layout : Any
            Layout to clear.
        """
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    DrawUtil._clearLayout(item.layout())

    ######################################################################
    #                          public functions                          #
    ######################################################################

    @staticmethod
    def drawBoard(
            buttonMap:list,
            board:Board,
            selectedTilePosition:Position)->None:
        """
        Draws board by updating icons of tile buttons.
        
        Parameter
        ---------
        buttonMap : list
            2D map of button representing the tiles in board.
        board : Board
            Board to draw.
        selectedTilePosition : Position
            Selected tile position. None if there is no selected tile.
        """
        assert len(buttonMap) == SIZE, "Invalid button map"
        for i in range(SIZE):
            assert len(buttonMap[i]) == SIZE, "Invalid button map"
        tilePositions = board.getTilePositions()
        for row in range(SIZE):
            for col in range(SIZE):
                selected = True if not selectedTilePosition == None and \
                    selectedTilePosition.row == row and \
                    selectedTilePosition.col == col else \
                    False
                DrawUtil._drawTile(buttonMap[row][col],tilePositions[row][col],selected)

    @staticmethod
    def drawPlayerMoveInfo(ui:Ui_widgetHexapawn,turnPlayer:Player)->None:
        """
        Draws player move information.
        
        Parameter
        ---------
        ui : Ui_widgetHexapawn
            Hexapawn UI object.
        turnPlayer : Player
            Player making the move.
        """
        button = ui.btnPlayerToMove
        size = QSize(160,20)
        pixmap = QPixmap(size)
        fill = Qt.white
        if turnPlayer == Player.BLACK:
            fill = Qt.black
        pixmap.fill(fill)
        button.setIcon(QtGui.QIcon(pixmap))
        button.setIconSize(size)

    @staticmethod
    def drawWinnerInfo(ui:Ui_widgetHexapawn,gameManager:GameManager)->None:
        """
        Draws winner information.
        
        Parameter
        ---------
        ui : Ui_widgetHexapawn
            Hexapawn UI object.
        gameManager : GameManager
            Game manager for game information.
        """
        winner = gameManager.winner
        if not winner == None:
            ui.lblPlayerToMove.setText("WINNER")
        else:
            ui.lblPlayerToMove.setText("Player To Move")
        
    @staticmethod
    def drawComputerTurnBox(ui:Ui_widgetHexapawn,box:Box,moveSelectFunc:MethodType)->None:
        """
        Clears computer turn box UIs.
        
        Parameter
        ---------
        ui : Ui_widgetHexapawn
            Hexapawn UI object.
        box : Box
            Box to draw.
        moveSelectFunc : MethodType
            Callback when move is selected.
        """
        # assert not box == None
        # TODO: add assert for box must be not None
        assert type(ui) == Ui_widgetHexapawn
        assert not moveSelectFunc == None and type(moveSelectFunc) == MethodType
        clear = True
        if not box == None:
            imgPath = COMPUTER_MOVE_IMG_PATH.format(box.id)
            if os.path.exists(imgPath):
                ui.btnComputerMove.setStyleSheet(COMPUTER_MOVE_STYLE.format(imgPath))
                layout = ui.grpMoves.layout()
                if layout == None:
                    layout = QVBoxLayout()
                    ui.grpMoves.setLayout(layout)
                else:
                    DrawUtil._clearLayout(ui.grpMoves.layout())
                for move in box.moves:
                    btn = MoveButton(move,moveSelectFunc)
                    layout.addWidget(btn)
                layout.addStretch()
                ui.btnMoveRandomSelect.setEnabled(True)
                clear = False
            else:
                print("{} not found!".format(imgPath))
        else:
            print("Box not found!")            
        if clear:
            DrawUtil.clearComputerTurnBox(ui)

    @staticmethod
    def clearComputerTurnBox(ui:Ui_widgetHexapawn)->None:
        """
        Clears computer turn box UIs.
        
        Parameter
        ---------
        ui : Ui_widgetHexapawn
            Hexapawn UI object.
        """
        assert type(ui) == Ui_widgetHexapawn
        ui.btnComputerMove.setStyleSheet(COMPUTER_MOVE_CLEAR_STYLE)
        DrawUtil._clearLayout(ui.grpMoves.layout())
        ui.btnMoveRandomSelect.setEnabled(False)