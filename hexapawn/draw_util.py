"""
###############################################################################

    Author        :   abelaro
    Copyright     :   2023

    Description   :   
        Source file for drawing utilitity functions.

###############################################################################
"""
from enum import Enum

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt, QSize

from hexapawn.game_manager import *
from hexapawn.pawn import *
from hexapawn.board import *

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
    def drawWinnerInfo(ui:Ui_widgetHexapawn)->None:
        """
        Draws winner information.
        
        Parameter
        ---------
        ui : Ui_widgetHexapawn
            Hexapawn UI object.
        """
        ui.lblPlayerToMove.setText("WINNER")
