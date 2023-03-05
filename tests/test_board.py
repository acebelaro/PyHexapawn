"""
###############################################################################

    Author        :   abelaro
    Copyright     :   2023

    Description   :   
        Unit test for board.

###############################################################################
"""
import unittest
import re
from hexapawn.board import *
from hexapawn.computer import *

BOARD_ROW_SETTING_REGEX = "^(B|W|-) (B|W|-) (B|W|-)$"

class TestBoardUtil():

    @staticmethod
    def getTargetPositions(setting:list):
        assert type(setting) == list
        assert len(setting) == SIZE
        assert all(re.match(BOARD_ROW_SETTING_REGEX,s) for s in setting)
        positions = []
        for row in range(SIZE):
            tokens = setting[row].split(' ')
            oneRow = []
            for col in range(len(tokens)):
                oneRow.append(tokens[col])
            positions.append(oneRow)
        return positions

    @staticmethod
    def setBoard(board:Board,setting:list):
        Box._setPawnsFromStringSetup(board,setting)
        
    @staticmethod
    def assertBoard(self,board:Board,expectedSetting:list):
        """
        Asserts pawn positions in board.
        """
        targetPositions = TestBoardUtil.getTargetPositions(expectedSetting)
        for row in range(SIZE):
            for col in range(SIZE):
                char = targetPositions[row][col]
                pawn = board._getPawnInPosition(Position(row,col))
                if char == "W":
                    self.assertIsNotNone(pawn,"Expecting white pawn.")
                    self.assertEqual(pawn.color,Color.WHITE,"Expecting white pawn.")
                elif char == "B":
                    self.assertIsNotNone(pawn,"Expecting white pawn.")
                    self.assertEqual(pawn.color,Color.BLACK,"Expecting white pawn.")
                elif char == "-":
                    self.assertIsNone(pawn,"Expecting no pawn.")

class TestPosition(unittest.TestCase):

    def test_position(self):

        position = Position(0,0)

        position = Position(1,0)

        position = Position(0,1)

        position = Position(SIZE-1,SIZE-1)

    def test_creatingPositionWithOutofBoundsRowRaisesError(self):

        with self.assertRaises(AssertionError):
            position = Position(-1,2)

        with self.assertRaises(AssertionError):
            position = Position(SIZE,0)

    def test_creatingPositionWithOutofBoundsColRaisesError(self):

        with self.assertRaises(AssertionError):
            Position(0,-1)

        with self.assertRaises(AssertionError):
            position = Position(0,SIZE)

class TestPawn(unittest.TestCase):

    ### Pawn.__init__ ###

    def test_pawn(self):

        pawn = Pawn(Color.BLACK,Position(0,0))
        self.assertEqual(pawn.color,Color.BLACK)
        self.assertEqual(pawn.position.row,0)
        self.assertEqual(pawn.position.col,0)

        pawn = Pawn(Color.WHITE,Position(1,2))
        self.assertEqual(pawn.color,Color.WHITE)
        self.assertEqual(pawn.position.row,1)
        self.assertEqual(pawn.position.col,2)

    ### Pawn.inPosition ###

    def test_inPosition(self):

        pawn = Pawn(Color.BLACK,Position(0,0))

        self.assertTrue(pawn.inPosition(Position(0,0)))

        self.assertFalse(pawn.inPosition(Position(1,0)))

        with self.assertRaises(AssertionError):
            pawn.inPosition(None)

    ### arePawnsEqual ###

    def test_arePawnsEqual_mismatchPawnCountReturnsFalse(self):
        # setup
        aPawns = [
            Pawn(Color.BLACK,Position(0,0)),
            Pawn(Color.BLACK,Position(0,1)),
            Pawn(Color.BLACK,Position(0,2)),
        ]
        bPawns = [
            Pawn(Color.BLACK,Position(0,0)),
            Pawn(Color.BLACK,Position(0,1)),
            # Pawn(Color.BLACK,Position(0,2)),
        ]
        # execute
        res = arePawnsEqual(aPawns,bPawns)
        # assert
        self.assertFalse(res)

    def test_arePawnsEqual_mismatchPawnPositionReturnsFalse(self):
        # setup
        aPawns = [
            Pawn(Color.BLACK,Position(0,0)),
            Pawn(Color.BLACK,Position(0,1)),
            Pawn(Color.BLACK,Position(0,2)),
        ]
        bPawns = [
            Pawn(Color.BLACK,Position(0,0)),
            Pawn(Color.BLACK,Position(0,1)),
            Pawn(Color.BLACK,Position(1,1)),
        ]
        # execute
        res = arePawnsEqual(aPawns,bPawns)
        # assert
        self.assertFalse(res)

    def test_arePawnsEqual_mismatchPawnColorReturnsFalse(self):
        # setup
        aPawns = [
            Pawn(Color.BLACK,Position(0,0)),
            Pawn(Color.BLACK,Position(0,1)),
            Pawn(Color.BLACK,Position(0,2)),
        ]
        bPawns = [
            Pawn(Color.WHITE,Position(0,0)),
            Pawn(Color.BLACK,Position(0,1)),
            Pawn(Color.BLACK,Position(0,2)),
        ]
        # execute
        res = arePawnsEqual(aPawns,bPawns)
        # assert
        self.assertFalse(res)

    def test_arePawnsEqual_returnsTrueForExactMatch(self):
        # setup
        aPawns = [
            Pawn(Color.BLACK,Position(0,0)),
            Pawn(Color.BLACK,Position(0,1)),
            Pawn(Color.BLACK,Position(0,2)),
        ]
        bPawns = [
            Pawn(Color.BLACK,Position(0,0)),
            Pawn(Color.BLACK,Position(0,1)),
            Pawn(Color.BLACK,Position(0,2)),
        ]
        # execute
        res = arePawnsEqual(aPawns,bPawns)
        # assert
        self.assertTrue(res)
        
        # setup
        aPawns = []
        bPawns = []
        # execute
        res = arePawnsEqual(aPawns,bPawns)
        # assert
        self.assertTrue(res)

class TestBoard(unittest.TestCase):

    def assertBoard(self,board:Board,expectedSetting:list):
        """
        Asserts pawn positions in board.
        """
        TestBoardUtil.assertBoard(self,board,expectedSetting)

    ### Board._getPawnInPosition ###

    def test_getPawnInPosition(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - -",
                "- - -",
                "- W -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(0,0))
        # assert
        self.assertIsNotNone(pawn)
        self.assertEqual(pawn.color,Color.BLACK)
        # execute
        pawn = board._getPawnInPosition(Position(2,1))
        # assert
        self.assertIsNotNone(pawn)
        self.assertEqual(pawn.color,Color.WHITE)
        # execute
        pawn = board._getPawnInPosition(Position(0,1))
        # assert
        self.assertIsNone(pawn)

    ### Board._isMoveValid ###

    def test_isMoveValid_blackPawnMovingForwardToEmptyTileIsValidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "- - -",
                "- W -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(0,1))
        assert not pawn == None and pawn.color == Color.BLACK
        newPosition = Position(1,1)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertTrue(res)

    def test_isMoveValid_blackPawnMovingDiagonalRightToTakeWhitePawnIsValidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "- - W",
                "- - -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(0,1))
        assert not pawn == None and pawn.color == Color.BLACK
        newPosition = Position(1,2)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertTrue(res)

    def test_isMoveValid_blackPawnMovingDiagonalLeftToTakeWhitePawnIsValidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "W - -",
                "- - -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(0,1))
        assert not pawn == None and pawn.color == Color.BLACK
        newPosition = Position(1,0)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertTrue(res)

    def test_isMoveValid_blackPawnMovingForwardToEmptyTileMoreThanOneTileAwayIsInvalidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "- - -",
                "- - W",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(0,1))
        assert not pawn == None and pawn.color == Color.BLACK
        newPosition = Position(2,1)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)

    def test_isMoveValid_blackPawnMovingToSideInvalidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "- - -",
                "- - W",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(0,1))
        assert not pawn == None and pawn.color == Color.BLACK
        newPosition = Position(0,0)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)
        # execute
        pawn = board._getPawnInPosition(Position(0,1))
        assert not pawn == None and pawn.color == Color.BLACK
        newPosition = Position(0,2)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)

    def test_isMoveValid_blackPawnMovingBackwardInvalidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - -",
                "- B -",
                "- - W",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(1,1))
        assert not pawn == None and pawn.color == Color.BLACK
        newPosition = Position(0,1)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)

    def test_isMoveValid_blackPawnMovingForwardToNonEmptyTileIsInvalidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "- W -",
                "- - -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(0,1))
        assert not pawn == None and pawn.color == Color.BLACK
        newPosition = Position(1,1)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "- B -",
                "- - W",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(0,1))
        assert not pawn == None and pawn.color == Color.BLACK
        newPosition = Position(1,1)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)

    def test_isMoveValid_blackPawnMovingDiagonalRightToEmptyTileIsValidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "W B -",
                "- - -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(0,1))
        assert not pawn == None and pawn.color == Color.BLACK
        newPosition = Position(1,2)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)

    def test_isMoveValid_blackPawnMovingDiagonalLeftToEmptyTileIsValidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "- B W",
                "- - -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(0,1))
        assert not pawn == None and pawn.color == Color.BLACK
        newPosition = Position(1,0)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)

    def test_isMoveValid_whitePawnMovingForwardToEmptyTileIsValidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "- - -",
                "- W -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(2,1))
        assert not pawn == None and pawn.color == Color.WHITE
        newPosition = Position(1,1)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertTrue(res)

    def test_isMoveValid_whitePawnMovingDiagonalRightToTakeBlackPawnIsValidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - -",
                "- - B",
                "- W -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(2,1))
        assert not pawn == None and pawn.color == Color.WHITE
        newPosition = Position(1,2)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertTrue(res)

    def test_isMoveValid_whitePawnMovingDiagonalLeftToTakeBlackPawnIsValidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - -",
                "B - -",
                "- W -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(2,1))
        assert not pawn == None and pawn.color == Color.WHITE
        newPosition = Position(1,0)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertTrue(res)

    def test_isMoveValid_whitePawnMovingForwardToEmptyTileMoreThanOneTileAwayIsInvalidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "- - -",
                "- - W",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(2,2))
        assert not pawn == None and pawn.color == Color.WHITE
        newPosition = Position(0,2)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)

    def test_isMoveValid_whitePawnMovingToSideInvalidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - -",
                "- - -",
                "- W -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(2,1))
        assert not pawn == None and pawn.color == Color.WHITE
        newPosition = Position(2,0)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)
        # execute
        pawn = board._getPawnInPosition(Position(2,1))
        assert not pawn == None and pawn.color == Color.WHITE
        newPosition = Position(2,2)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)

    def test_isMoveValid_whitePawnMovingBackwardInvalidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - -",
                "- W -",
                "- - -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(1,1))
        assert not pawn == None and pawn.color == Color.WHITE
        newPosition = Position(2,1)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)

    def test_isMoveValid_whitePawnMovingForwardToNonEmptyTileIsInvalidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - B",
                "- B -",
                "- W -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(2,1))
        assert not pawn == None and pawn.color == Color.WHITE
        newPosition = Position(1,1)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - B",
                "- W -",
                "- W -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(2,1))
        assert not pawn == None and pawn.color == Color.WHITE
        newPosition = Position(1,1)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)

    def test_isMoveValid_whitePawnMovingDiagonalRightToEmptyTileIsValidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - -",
                "B W -",
                "- W -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(2,1))
        assert not pawn == None and pawn.color == Color.WHITE
        newPosition = Position(1,2)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)

    def test_isMoveValid_whitePawnMovingDiagonalLeftToEmptyTileIsValidMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - -",
                "- W B",
                "- W -",
            ])
        # execute
        pawn = board._getPawnInPosition(Position(2,1))
        assert not pawn == None and pawn.color == Color.WHITE
        newPosition = Position(1,0)
        pawnInPosition = board._getPawnInPosition(newPosition)
        res = board._isMoveValid(pawn,newPosition,pawnInPosition)
        # assert
        self.assertFalse(res)

    ### Board._blackPawnPossibleMove ###

    def test_blackPawnPossibleMove_canMoveForward(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - -",
                "- - -",
                "- W -",
            ])
        # execute
        res = board._blackPawnHasPossibleMove()
        # assert
        self.assertTrue(res)

    def test_blackPawnPossibleMove_canMoveDiagonalLeft(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "W B -",
                "- W -",
            ])
        # execute
        res = board._blackPawnHasPossibleMove()
        # assert
        self.assertTrue(res)

    def test_blackPawnPossibleMove_canMoveDiagonalRight(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "- B W",
                "- W -",
            ])
        # execute
        res = board._blackPawnHasPossibleMove()
        # assert
        self.assertTrue(res)

    def test_blackPawnPossibleMove_noPossibleMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - -",
                "- B -",
                "B W -",
            ])
        # execute
        res = board._blackPawnHasPossibleMove()
        # assert
        self.assertFalse(res)

    ### Board._whitePawnHasPossibleMove ###

    def test_whitePawnHasPossibleMove_canMoveForward(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - -",
                "- - -",
                "- W -",
            ])
        # execute
        res = board._whitePawnHasPossibleMove()
        # assert
        self.assertTrue(res)

    def test_whitePawnHasPossibleMove_canMoveDiagonalLeft(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - -",
                "B B -",
                "- W -",
            ])
        # execute
        res = board._whitePawnHasPossibleMove()
        # assert
        self.assertTrue(res)

    def test_whitePawnHasPossibleMove_canMoveDiagonalRight(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - -",
                "- B B",
                "- W -",
            ])
        # execute
        res = board._whitePawnHasPossibleMove()
        # assert
        self.assertTrue(res)

    def test_whitePawnHasPossibleMove_noPossibleMove(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "W B -",
                "- W -",
                "- - -",
            ])
        # execute
        res = board._whitePawnHasPossibleMove()
        # assert
        self.assertFalse(res)

    ### Board.getTilePositions ###

    def test_getTilePositions(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B B B",
                "- - -",
                "W W W",
            ])
        # execute
        tilePositions = board.getTilePositions()
        # assert
        self.assertIsNotNone(tilePositions)
        self.assertEqual(len(tilePositions),SIZE)
        self.assertTrue(all(len(tilePosition)==SIZE for tilePosition in tilePositions))
        blackPawns = board._blackPawns
        whitePawns = board._whitePawns
        self.assertEqual([blackPawns[0],blackPawns[1],blackPawns[2]],tilePositions[0])
        self.assertEqual([None,None,None],tilePositions[1])
        self.assertEqual([whitePawns[0],whitePawns[1],whitePawns[2]],tilePositions[2])
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - -",
                "- - -",
                "- - -",
            ])
        # execute
        tilePositions = board.getTilePositions()
        # assert
        self.assertIsNotNone(tilePositions)
        self.assertEqual(len(tilePositions),SIZE)
        self.assertTrue(all(len(tilePosition)==SIZE for tilePosition in tilePositions))
        self.assertEqual([None,None,None],tilePositions[0])
        self.assertEqual([None,None,None],tilePositions[1])
        self.assertEqual([None,None,None],tilePositions[2])
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "- W B",
                "W - -",
            ])
        # execute
        tilePositions = board.getTilePositions()
        # assert
        self.assertIsNotNone(tilePositions)
        self.assertEqual(len(tilePositions),SIZE)
        self.assertTrue(all(len(tilePosition)==SIZE for tilePosition in tilePositions))
        blackPawns = board._blackPawns
        whitePawns = board._whitePawns
        self.assertEqual([None,blackPawns[0],None],tilePositions[0])
        self.assertEqual([None,whitePawns[0],blackPawns[1]],tilePositions[1])
        self.assertEqual([whitePawns[1],None,None],tilePositions[2])

    ### Board.movePawn ####

    def test_movePawn_whiteMovingForwardMoreThanOneTileAwayIsInvalidMove(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B B",
                "- - -",
                "W W W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(2,0))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(0,0))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "- B B",
                "- - -",
                "W W W",
            ])

    def test_movePawn_whiteMovingToSideIsInvalidMove(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - B",
                "- W -",
                "- - -",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,1))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(1,0))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "B - B",
                "- W -",
                "- - -",
            ])

        # execute
        res = board.movePawn(pawn,Position(1,2))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "B - B",
                "- W -",
                "- - -",
            ])

    def test_movePawn_whiteMovingBackwardIsInvalidMove(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - B",
                "- W -",
                "- - -",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,1))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(2,1))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "B - B",
                "- W -",
                "- - -",
            ])
        
    def test_movePawn_whiteMovingForwardToEmptyTileAndNoWinner(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B B B",
                "- - -",
                "W W W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(2,0))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(1,0))
        
        # assert
        self.assertEqual(res,MovePawnResult.NO_WINNER)
        self.assertBoard(
            board,
            [
                "B B B",
                "W - -",
                "- W W"
            ])

        # execute
        pawn = board._getPawnInPosition(Position(2,1))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(1,1))

        # assert
        self.assertEqual(res,MovePawnResult.NO_WINNER)
        self.assertBoard(
            board,
            [
                "B B B",
                "W W -",
                "- - W"
            ])

        # execute
        pawn = board._getPawnInPosition(Position(2,2))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(1,2))

        # assert
        self.assertEqual(res,MovePawnResult.NO_WINNER)
        self.assertBoard(
            board,
            [
                "B B B",
                "W W W",
                "- - -"
            ])

    def test_movePawn_whiteMovingForwardToEmptyTileAndWhiteWins(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B B",
                "W - -",
                "- W W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,0))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(0,0))

        # assert
        self.assertEqual(res,MovePawnResult.WHITE_WIN)
        self.assertBoard(
            board,
            [
                "W B B",
                "- - -",
                "- W W",
            ])

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - B",
                "- W -",
                "W - W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,1))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(0,1))

        # assert
        self.assertEqual(res,MovePawnResult.WHITE_WIN)
        self.assertBoard(
            board,
            [
                "B W B",
                "- - -",
                "W - W",
            ])

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B B -",
                "- - W",
                "W W -",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,2))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(0,2))

        # assert
        self.assertEqual(res,MovePawnResult.WHITE_WIN)
        self.assertBoard(
            board,
            [
                "B B W",
                "- - -",
                "W W -",
            ])

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - B",
                "W B -",
                "- W W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(2,2))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(1,2))

        # assert
        self.assertEqual(res,MovePawnResult.WHITE_WIN)
        self.assertBoard(
            board,
            [
                "B - B",
                "W B W",
                "- W -",
            ])
        
    def test_movePawn_whiteMovingForwardToNonEmptyTileIsInvalidMove(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - -",
                "W - -",
                "- W W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,0))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(0,0))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "B - -",
                "W - -",
                "- W W",
            ])

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "- W -",
                "W - W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,1))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(0,1))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "- B -",
                "- W -",
                "W - W",
            ])

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - B",
                "- - W",
                "W W -",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,2))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(0,2))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "- - B",
                "- - W",
                "W W -",
            ])

    def test_movePawn_whiteMovingDiagonalRightToBlackPawnAndNoWinner(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - B",
                "- B -",
                "W - -",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(2,0))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(1,1))

        # assert
        self.assertEqual(res,MovePawnResult.NO_WINNER)
        self.assertBoard(
            board,
            [
                "- - B",
                "- W -",
                "- - -",
            ])
        
    def test_movePawn_whiteMovingDiagonalRightToBlackPawnAndWinner(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - B",
                "B W -",
                "- - -",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,1))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(0,2))

        # assert
        self.assertEqual(res,MovePawnResult.WHITE_WIN)
        self.assertBoard(
            board,
            [
                "- - W",
                "B - -",
                "- - -",
            ])
        
    def test_movePawn_whiteMovingDiagonalRightToEmptyTileIsInvalidMove(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - B",
                "- - B",
                "W - -",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(2,0))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(1,1))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "- - B",
                "- - B",
                "W - -",
            ])

    def test_movePawn_whiteMovingDiagonalLeftToBlackPawnAndNoWinner(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - B",
                "- B -",
                "- - W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(2,2))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(1,1))

        # assert
        self.assertEqual(res,MovePawnResult.NO_WINNER)
        self.assertBoard(
            board,
            [
                "- - B",
                "- W -",
                "- - -",
            ])
        
    def test_movePawn_whiteMovingDiagonalLeftToBlackPawnAndWinner(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - -",
                "- W B",
                "- - -",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,1))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(0,0))

        # assert
        self.assertEqual(res,MovePawnResult.WHITE_WIN)
        self.assertBoard(
            board,
            [
                "W - -",
                "- - B",
                "- - -",
            ])
        
    def test_movePawn_whiteMovingDiagonalLeftToEmptyTileIsInvalidMove(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - -",
                "B - W",
                "- - W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(2,2))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.WHITE, "Expecting white pawn."
        res = board.movePawn(pawn,Position(1,1))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "B - -",
                "B - W",
                "- - W",
            ])

    def test_movePawn_blackMovingForwardMoreThanOneTileAwayIsInvalidMove(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B B",
                "W - -",
                "W - -",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(0,2))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(2,2))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "- B B",
                "W - -",
                "W - -",
            ])

    def test_movePawn_blackMovingToSideIsInvalidMove(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - -",
                "- B -",
                "W - W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,1))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(1,0))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "- - -",
                "- B -",
                "W - W",
            ])

        # execute
        res = board.movePawn(pawn,Position(1,2))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "- - -",
                "- B -",
                "W - W",
            ])

    def test_movePawn_blackMovingBackwardIsInvalidMove(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - -",
                "- B -",
                "W - W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,1))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(0,1))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "- - -",
                "- B -",
                "W - W",
            ])
        
    def test_movePawn_blackMovingForwardToEmptyTileAndNoWinner(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B B B",
                "- - -",
                "W W W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(0,0))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(1,0))
        
        # assert
        self.assertEqual(res,MovePawnResult.NO_WINNER)
        self.assertBoard(
            board,
            [
                "- B B",
                "B - -",
                "W W W"
            ])

        # execute
        pawn = board._getPawnInPosition(Position(0,1))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(1,1))

        # assert
        self.assertEqual(res,MovePawnResult.NO_WINNER)
        self.assertBoard(
            board,
            [
                "- - B",
                "B B -",
                "W W W"
            ])

        # execute
        pawn = board._getPawnInPosition(Position(0,2))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(1,2))

        # assert
        self.assertEqual(res,MovePawnResult.NO_WINNER)
        self.assertBoard(
            board,
            [
                "- - -",
                "B B B",
                "W W W"
            ])

    def test_movePawn_blackMovingForwardToEmptyTileAndBlackWins(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B B",
                "B - -",
                "- W W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,0))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(2,0))

        # assert
        self.assertEqual(res,MovePawnResult.BLACK_WIN)
        self.assertBoard(
            board,
            [
                "- B B",
                "- - -",
                "B W W",
            ])

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - B",
                "- B -",
                "W - W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,1))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(2,1))

        # assert
        self.assertEqual(res,MovePawnResult.BLACK_WIN)
        self.assertBoard(
            board,
            [
                "B - B",
                "- - -",
                "W B W",
            ])

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B B -",
                "- - B",
                "W W -",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,2))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(2,2))

        # assert
        self.assertEqual(res,MovePawnResult.BLACK_WIN)
        self.assertBoard(
            board,
            [
                "B B -",
                "- - -",
                "W W B",
            ])

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B B B",
                "W - W",
                "- W -",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(0,1))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(1,1))

        # assert
        self.assertEqual(res,MovePawnResult.BLACK_WIN)
        self.assertBoard(
            board,
            [
                "B - B",
                "W B W",
                "- W -",
            ])
        
    def test_movePawn_blackMovingForwardToNonEmptyTileIsInvalidMove(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B B",
                "B - -",
                "W W W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,0))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(2,0))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "- B B",
                "B - -",
                "W W W",
            ])

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - B",
                "- B -",
                "W W W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,1))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(2,1))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "B - B",
                "- B -",
                "W W W",
            ])

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B B -",
                "- - B",
                "W W W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,2))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(2,2))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "B B -",
                "- - B",
                "W W W",
            ])

    def test_movePawn_blackMovingDiagonalRightToBlackPawnAndNoWinner(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - -",
                "- W B",
                "- W -",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(0,0))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(1,1))

        # assert
        self.assertEqual(res,MovePawnResult.NO_WINNER)
        self.assertBoard(
            board,
            [
                "- - -",
                "- B B",
                "- W -",
            ])
        
    def test_movePawn_blackMovingDiagonalRightToWhitePawnAndWinner(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - B",
                "B W -",
                "- W -",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,0))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(2,1))

        # assert
        self.assertEqual(res,MovePawnResult.BLACK_WIN)
        self.assertBoard(
            board,
            [
                "- - B",
                "- W -",
                "- B -",
            ])
        
    def test_movePawn_blackMovingDiagonalRightToEmptyTileIsInvalidMove(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - -",
                "- - B",
                "W - -",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(0,0))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(1,1))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "B - -",
                "- - B",
                "W - -",
            ])

    def test_movePawn_blackMovingDiagonalLeftToWhitePawnAndNoWinner(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - B",
                "B W W",
                "- - -"
            ])

        # execute
        pawn = board._getPawnInPosition(Position(0,2))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(1,1))

        # assert
        self.assertEqual(res,MovePawnResult.NO_WINNER)
        self.assertBoard(
            board,
            [
                "- - -",
                "B B W",
                "- - -"
            ])
        
    def test_movePawn_blackMovingDiagonalLeftToWhitePawnAndWinner(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B - -",
                "- W B",
                "- W -",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(1,2))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(2,1))

        # assert
        self.assertEqual(res,MovePawnResult.BLACK_WIN)
        self.assertBoard(
            board,
            [
                "B - -",
                "- W -",
                "- B -",
            ])
        
    def test_movePawn_blackMovingDiagonalLeftToEmptyTileIsInvalidMove(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- - B",
                "B - W",
                "- - W",
            ])

        # execute
        pawn = board._getPawnInPosition(Position(0,2))
        assert not pawn == None, "Test pawn not found."
        assert pawn.color == Color.BLACK, "Expecting black pawn."
        res = board.movePawn(pawn,Position(1,1))

        # assert
        self.assertEqual(res,MovePawnResult.INVALID)
        self.assertBoard(
            board,
            [
                "- - B",
                "B - W",
                "- - W",
            ])

    ### Board.arePawnPositionsSymmetric ###

    def test_arePawnPositionsSymmetric_asymmetric(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B B -",
                "- - -",
                "W W W"
            ])
        # execute
        res = board.arePawnPositionsSymmetric()
        # assert
        self.assertFalse(res)
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B B B",
                "- - W",
                "- W -"
            ])
        # execute
        res = board.arePawnPositionsSymmetric()
        # assert
        self.assertFalse(res)
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B B B",
                "- - -",
                "W W -"
            ])
        # execute
        res = board.arePawnPositionsSymmetric()
        # assert
        self.assertFalse(res)

    def test_arePawnPositionsSymmetric_symmetric(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "W B W",
                "- W -",
            ])
        # execute
        res = board.arePawnPositionsSymmetric()
        # assert
        self.assertTrue(res)
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B -",
                "- - -",
                "- W -",
            ])
        # execute
        res = board.arePawnPositionsSymmetric()
        # assert
        self.assertTrue(res)

    ### Board.resetPawns ###

    def test_resetPawns(self):
        board = Board()
        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- B B",
                "W B -",
                "- W W",
            ])
        # execute
        board.resetPawns()
        # assert
        self.assertBoard(
            board,
            [
                "B B B",
                "- - -",
                "W W W",
            ])
        
    ### areBoardsEqual ###

    def test_areBoardsEqual_matchReturnsTrue(self):
        boardA = Board()
        boardB = Board()
        # setup
        TestBoardUtil.setBoard(
            boardA,
            [
                "- B B",
                "W B -",
                "- W W",
            ])
        TestBoardUtil.setBoard(
            boardB,
            [
                "- B B",
                "W B -",
                "- W W",
            ])
        # execute
        res = areBoardsEqual(boardA,boardB)
        # assert
        self.assertTrue(res)

    def test_areBoardsEqual_mismatchReturnsFalse(self):
        boardA = Board()
        boardB = Board()
        ## row 0 mismacth
        # setup
        TestBoardUtil.setBoard(
            boardA,
            [
                "- B B",
                "W B -",
                "- W W",
            ])
        TestBoardUtil.setBoard(
            boardB,
            [
                "- B -",
                "W B -",
                "- W W",
            ])
        # execute
        res = areBoardsEqual(boardA,boardB)
        # assert
        self.assertFalse(res)
        # setup
        TestBoardUtil.setBoard(
            boardA,
            [
                "- B B",
                "W B -",
                "- W -",
            ])
        TestBoardUtil.setBoard(
            boardB,
            [
                "- B W",
                "W B -",
                "- W -",
            ])
        # execute
        res = areBoardsEqual(boardA,boardB)
        # assert
        self.assertFalse(res)
        ## row 1 mismacth
        TestBoardUtil.setBoard(
            boardA,
            [
                "- B B",
                "- B -",
                "- W W",
            ])
        TestBoardUtil.setBoard(
            boardB,
            [
                "- B B",
                "W B -",
                "- W W",
            ])
        # execute
        res = areBoardsEqual(boardA,boardB)
        # assert
        self.assertFalse(res)
        ## row 2 mismacth
        # setup
        TestBoardUtil.setBoard(
            boardA,
            [
                "- B B",
                "W B -",
                "W W -",
            ])
        TestBoardUtil.setBoard(
            boardB,
            [
                "- B B",
                "W B -",
                "- W W",
            ])
        # execute
        res = areBoardsEqual(boardA,boardB)
        # assert
        self.assertFalse(res)
        