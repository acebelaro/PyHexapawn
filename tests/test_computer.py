"""
###############################################################################

    Author        :   abelaro
    Copyright     :   2023

    Description   :   
        Unit test for computer.

###############################################################################
"""
import unittest
from hexapawn.computer import *
from tests.test_board import TestBoardUtil

BOARD_ROW_SETTING_REGEX = "^(B|W|-) (B|W|-) (B|W|-)$"

class TestMove(unittest.TestCase):

    def test_newPosition_forward(self):
        # setup
        currentPosition = Position(0,0)
        move = Move(currentPosition,MoveColor.GREEN,Movement.FORWARD)
        # execute
        newPosition = move.newPosition()
        # assert
        self.assertIsNotNone(newPosition)
        self.assertEqual(newPosition.row,1)
        self.assertEqual(newPosition.col,0)

    def test_newPosition_diagonalLeft(self):
        # setup
        currentPosition = Position(1,1)
        move = Move(currentPosition,MoveColor.GREEN,Movement.DIAGONAL_LEFT)
        # execute
        newPosition = move.newPosition()
        # assert
        self.assertIsNotNone(newPosition)
        self.assertEqual(newPosition.row,2)
        self.assertEqual(newPosition.col,0)

    def test_newPosition_diagonalLeft(self):
        # setup
        currentPosition = Position(1,1)
        move = Move(currentPosition,MoveColor.GREEN,Movement.DIAGONAL_RIGHT)
        # execute
        newPosition = move.newPosition()
        # assert
        self.assertIsNotNone(newPosition)
        self.assertEqual(newPosition.row,2)
        self.assertEqual(newPosition.col,2)

class TestBox(unittest.TestCase):

    def test_box_raisesErrorWhenMoveBlackPawnDoesNotExists(self):
        with self.assertRaises(AssertionError) as err:
            box = Box(
                "2A",
                2,
                [
                    "B B B",
                    "W - -",
                    "- W W"
                ],
                [
                    Move(Position(0,1),MoveColor.GREEN,Movement.DIAGONAL_LEFT),
                    Move(Position(1,1),MoveColor.RED,Movement.FORWARD),
                    Move(Position(0,2),MoveColor.BLUE,Movement.FORWARD),
                ]
            )
        self.assertEqual("2 : [1,1] FORWARD : Move position must have black pawn.",str(err.exception))

    def test_box_raisesErrorWhenForwardMoveForBlackPawnInLastRow(self):
        with self.assertRaises(AssertionError) as err:
            box = Box(
                "2A",
                2,
                [
                    "- - -",
                    "W - -",
                    "B W W"
                ],
                [
                    Move(Position(2,0),MoveColor.GREEN,Movement.FORWARD)
                ]
            )
        self.assertEqual("2 : [2,0] FORWARD : Results to outside board.",str(err.exception))

    def test_box_raisesErrorWhenForwardMoveToNonEmptyTile(self):
        with self.assertRaises(AssertionError) as err:
            box = Box(
                "2A",
                2,
                [
                    "B B B",
                    "W - -",
                    "- W W"
                ],
                [
                    Move(Position(0,0),MoveColor.RED,Movement.FORWARD),
                    Move(Position(0,0),MoveColor.GREEN,Movement.DIAGONAL_LEFT),
                    Move(Position(0,2),MoveColor.BLUE,Movement.FORWARD),
                ]
            )
        self.assertEqual("2 : [0,0] FORWARD : Expecting empty tile in front.",str(err.exception))

    def test_box_raisesErrorWhenDiagonalLeftMoveIsOutsideBoard(self):
        with self.assertRaises(AssertionError) as err:
            box = Box(
                "2A",
                2,
                [
                    "B B B",
                    "W - -",
                    "- W W"
                ],
                [
                    Move(Position(0,0),MoveColor.RED,Movement.DIAGONAL_LEFT),
                    Move(Position(0,1),MoveColor.GREEN,Movement.DIAGONAL_LEFT),
                    Move(Position(0,2),MoveColor.BLUE,Movement.FORWARD),
                ]
            )
        self.assertEqual("2 : [0,0] DIAGONAL_LEFT : Results to outside board.",str(err.exception))

    def test_box_raisesErrorWhenDiagonalLeftMoveToEmptyTile(self):
        with self.assertRaises(AssertionError) as err:
            box = Box(
                "2A",
                2,
                [
                    "B B B",
                    "W - -",
                    "- W W"
                ],
                [
                    Move(Position(0,1),MoveColor.RED,Movement.FORWARD),
                    Move(Position(0,1),MoveColor.GREEN,Movement.DIAGONAL_LEFT),
                    Move(Position(0,2),MoveColor.BLUE,Movement.DIAGONAL_LEFT),
                ]
            )
        self.assertEqual("2 : [0,2] DIAGONAL_LEFT : Expecting to take white pawn.",str(err.exception))

    def test_box_raisesErrorWhenDiagonalLeftMoveToBlackPawnTile(self):
        with self.assertRaises(AssertionError) as err:
            box = Box(
                "2A",
                2,
                [
                    "B - B",
                    "W B -",
                    "- W W"
                ],
                [
                    Move(Position(0,2),MoveColor.BLUE,Movement.DIAGONAL_LEFT),
                ]
            )
        self.assertEqual("2 : [0,2] DIAGONAL_LEFT : Expecting to take white pawn.",str(err.exception))

    def test_box_raisesErrorWhenDiagonalRightMoveIsOutsideBoard(self):
        with self.assertRaises(AssertionError) as err:
            box = Box(
                "2A",
                2,
                [
                    "B B B",
                    "W - -",
                    "- W W"
                ],
                [
                    Move(Position(0,1),MoveColor.RED,Movement.FORWARD),
                    Move(Position(0,1),MoveColor.GREEN,Movement.DIAGONAL_LEFT),
                    Move(Position(0,2),MoveColor.BLUE,Movement.DIAGONAL_RIGHT),
                ]
            )
        self.assertEqual("2 : [0,2] DIAGONAL_RIGHT : Results to outside board.",str(err.exception))

    def test_box_raisesErrorWhenDiagonalRightMoveToEmptyTile(self):
        with self.assertRaises(AssertionError) as err:
            box = Box(
                "2A",
                2,
                [
                    "B B B",
                    "W - -",
                    "- W W"
                ],
                [
                    Move(Position(0,1),MoveColor.GREEN,Movement.DIAGONAL_LEFT),
                    Move(Position(0,1),MoveColor.RED,Movement.FORWARD),
                    Move(Position(0,0),MoveColor.BLUE,Movement.DIAGONAL_RIGHT),
                ]
            )
        self.assertEqual("2 : [0,0] DIAGONAL_RIGHT : Expecting to take white pawn.",str(err.exception))

    def test_box_raisesErrorWhenDiagonalRightMoveToBlackPawnTile(self):
        with self.assertRaises(AssertionError) as err:
            box = Box(
                "2A",
                2,
                [
                    "B - B",
                    "W B -",
                    "- W W"
                ],
                [
                    Move(Position(0,0),MoveColor.BLUE,Movement.DIAGONAL_RIGHT),
                ]
            )
        self.assertEqual("2 : [0,0] DIAGONAL_RIGHT : Expecting to take white pawn.",str(err.exception))

class TestComputer(unittest.TestCase):

    def test_computer(self):
        computer = Computer()

    ### Computer._createMirroredBox ###

    def test_createMirroredBox(self):
        # setup
        box = Box(
            "4D", 4,
            [
                "B B -",
                "W - W",
                "- - W"
            ],
            [
                Move(Position(0,1),MoveColor.GREEN,Movement.DIAGONAL_LEFT),
                Move(Position(0,1),MoveColor.RED,Movement.FORWARD),
                Move(Position(0,1),MoveColor.BLUE,Movement.DIAGONAL_RIGHT)
            ]
        )
        # execute
        mirroredBox = Computer._createMirroredBox(box)
        # assert
        TestBoardUtil.assertBoard(self,mirroredBox,[
                "- B B",
                "W - W",
                "W - -"
        ])
        index = 0
        move = mirroredBox.moves[index]
        self.assertEqual(move.position.row,0)
        self.assertEqual(move.position.col,1)
        self.assertEqual(move.color,MoveColor.GREEN)
        self.assertEqual(move.movement,Movement.DIAGONAL_RIGHT)
        index+=1
        move = mirroredBox.moves[index]
        self.assertEqual(move.position.row,0)
        self.assertEqual(move.position.col,1)
        self.assertEqual(move.color,MoveColor.RED)
        self.assertEqual(move.movement,Movement.FORWARD)
        index+=1
        move = mirroredBox.moves[index]
        self.assertEqual(move.position.row,0)
        self.assertEqual(move.position.col,1)
        self.assertEqual(move.color,MoveColor.BLUE)
        self.assertEqual(move.movement,Movement.DIAGONAL_LEFT)
        index+=1
        # setup
        box = Box(
            "6G", 6,
            [
                "- - B",
                "B W -",
                "- - -"
            ],
            [
                Move(Position(0,2),MoveColor.RED,Movement.DIAGONAL_LEFT),
                Move(Position(0,2),MoveColor.BLUE,Movement.FORWARD),
                Move(Position(1,0),MoveColor.GREEN,Movement.FORWARD)
            ]
        )
        # execute
        mirroredBox = Computer._createMirroredBox(box)
        # assert
        TestBoardUtil.assertBoard(self,mirroredBox,[
                "B - -",
                "- W B",
                "- - -"
        ])
        index = 0

        move = mirroredBox.moves[index]
        self.assertEqual(move.position.row,0)
        self.assertEqual(move.position.col,0)
        self.assertEqual(move.color,MoveColor.RED)
        self.assertEqual(move.movement,Movement.DIAGONAL_RIGHT)
        index+=1
        
        move = mirroredBox.moves[index]
        self.assertEqual(move.position.row,0)
        self.assertEqual(move.position.col,0)
        self.assertEqual(move.color,MoveColor.BLUE)
        self.assertEqual(move.movement,Movement.FORWARD)
        index+=1
        
        move = mirroredBox.moves[index]
        self.assertEqual(move.position.row,1)
        self.assertEqual(move.position.col,2)
        self.assertEqual(move.color,MoveColor.GREEN)
        self.assertEqual(move.movement,Movement.FORWARD)
        index+=1
