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
from PyQt5.QtGui import QPainter, QPixmap, QPen, QPolygon
from PyQt5.QtCore import Qt, QSize, QPoint
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

"""Main board tile constants."""
TILE_BUTTON_SIZE = 96
PAWN_DRAWING_SIZE = 86
PAWN_ELLIPSE_XY = (TILE_BUTTON_SIZE - PAWN_DRAWING_SIZE)/2

"""Box boarrd draw constants."""
BOX_BOARD_TILE_SIZE = 60
BOX_BOARD_DRAW_SIZE = SIZE * BOX_BOARD_TILE_SIZE
BOX_BOARD_PAWN_SIZE = 40
BOX_BOARD_PAWNW_START_POINT_DIFF = (BOX_BOARD_TILE_SIZE-BOX_BOARD_PAWN_SIZE)/2
BOX_BOARD_COLOR = QtGui.QColor(255,193,116)

SELECT_MOVE_BUTTON_SIZE = QSize(180,15)

MOVEMENT_POINTS_MAP = {
    Movement.FORWARD : [
        QPoint(27,50),
        QPoint(27,58),
        QPoint(23,58),
        QPoint(30,65),
        QPoint(38,58),
        QPoint(34,58),
        QPoint(34,50)
    ],
    Movement.DIAGONAL_LEFT : [
        QPoint(-4,53),
        QPoint(-4,64),
        QPoint(7,64),
        QPoint(4,61),
        QPoint(11,54),
        QPoint(6,49),
        QPoint(-1,56),
    ],
    Movement.DIAGONAL_RIGHT : [
        QPoint(54,49),
        QPoint(61,56),
        QPoint(64,53),
        QPoint(64,64),
        QPoint(53,64),
        QPoint(56,61),
        QPoint(49,54),
    ],
}
"""Polygon point list for each movement for drawing."""

class SelectMoveButton(QtWidgets.QPushButton):
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

        size = SELECT_MOVE_BUTTON_SIZE
        pixmap = QPixmap(size)
        pixmap.fill(move.color.value)
        self.setIcon(QtGui.QIcon(pixmap))
        self.setIconSize(size)

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
        size = QSize(TILE_BUTTON_SIZE,TILE_BUTTON_SIZE)
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

    @staticmethod
    def _drawBoardTiles(painter:QPainter,box:Box)->None:
        """
        Draws board tiles and pawns.

        Parameter
        ---------
        painter : QPainter
            Initialized painter.
        box : Box
            Box  to draw.
        """
        posititions = box.getTilePositions()\
            if not box == None else None
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        for row in range(SIZE):
            for col in range(SIZE):
                # tile
                painter.setBrush(BOX_BOARD_COLOR)
                pts = [
                    QPoint( (col*BOX_BOARD_TILE_SIZE), 
                           (row*BOX_BOARD_TILE_SIZE) ),
                    QPoint( BOX_BOARD_TILE_SIZE + (col*BOX_BOARD_TILE_SIZE), 
                           (row*BOX_BOARD_TILE_SIZE) ),
                    QPoint( BOX_BOARD_TILE_SIZE + (col*BOX_BOARD_TILE_SIZE), 
                           BOX_BOARD_TILE_SIZE + (row*BOX_BOARD_TILE_SIZE) ),
                    QPoint( (col*BOX_BOARD_TILE_SIZE), 
                           BOX_BOARD_TILE_SIZE + (row*BOX_BOARD_TILE_SIZE) )
                ]
                painter.drawPolygon(QPolygon(pts))
                # pawn
                pawn = posititions[row][col]\
                    if not posititions == None else None
                if not pawn == None:
                    painter.setBrush(pawn.color.value)
                    x1 = (row*BOX_BOARD_TILE_SIZE)
                    y1 = (col*BOX_BOARD_TILE_SIZE)
                    painter.drawEllipse(
                        y1 + BOX_BOARD_PAWNW_START_POINT_DIFF,
                        x1 + BOX_BOARD_PAWNW_START_POINT_DIFF,
                        BOX_BOARD_PAWN_SIZE,
                        BOX_BOARD_PAWN_SIZE)

    @staticmethod
    def _drawMoveButtons(ui:Ui_widgetHexapawn,painter:QPainter,box:Box,moveSelectFunc:MethodType)->None:
        """
        Draws move buttons.

        Parameter
        ---------
        ui : Ui_widgetHexapawn
            Hexapawn UI object.
        painter : QPainter
            Initialized painter.
        box : Box
            Box  to draw.
        moveSelectFunc : MethodType
            Callback when move is selected.
        """
        layout = ui.grpMoves.layout()
        if layout == None:
            layout = QVBoxLayout()
            ui.grpMoves.setLayout(layout)
        else:
            DrawUtil._clearLayout(ui.grpMoves.layout())
        if not box == None:
            ui.btnMoveRandomSelect.setEnabled(True)
            for move in box.moves:
                # select move button
                btn = SelectMoveButton(move,moveSelectFunc)
                layout.addWidget(btn)
                # movement arrow
                pts = MOVEMENT_POINTS_MAP[move.movement]
                if not pts == None:
                    painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                    painter.setBrush(move.color.value)
                    adjustP = []
                    adjX = (move.position.col*BOX_BOARD_TILE_SIZE)
                    adjY = (move.position.row*BOX_BOARD_TILE_SIZE)
                    for pt in pts:
                        adjustP.append(QPoint(pt.x()+adjX,pt.y()+adjY))
                    painter.drawPolygon(QPolygon(adjustP))
            layout.addStretch()
        else:
            ui.btnMoveRandomSelect.setEnabled(False)

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
    def drawBox(ui:Ui_widgetHexapawn,box:Box,moveSelectFunc:MethodType)->None:
        """
        Draws box.

        Parameter
        ---------
        ui : Ui_widgetHexapawn
            Hexapawn UI object.
        box : Box
            Box  to draw.
        moveSelectFunc : MethodType
            Callback when move is selected.
        """
        size = QSize( BOX_BOARD_DRAW_SIZE, BOX_BOARD_DRAW_SIZE )
        pixmap = QPixmap(size)
        painter = QPainter(pixmap)
        # draw board tiles
        DrawUtil._drawBoardTiles(painter,box)
        # draw moves
        DrawUtil._drawMoveButtons(ui,painter,box,moveSelectFunc)
        painter.end()
        ui.btnComputerMove.setIcon(QtGui.QIcon(pixmap))
        ui.btnComputerMove.setIconSize(size)