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
from hexapawn.pawn import *
from hexapawn.board import *

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
        targetPositions = TestBoardUtil.getTargetPositions(setting)
        whitePawns = []
        blackPawns = []
        for row in range(SIZE):
            for col in range(SIZE):
                char = targetPositions[row][col]
                if char == "W":
                    whitePawns.append(Pawn(Color.WHITE,Position(row,col)))
                elif char == "B":
                    blackPawns.append(Pawn(Color.BLACK,Position(row,col)))

        board._whitePawns = whitePawns
        board._blackPawns = blackPawns
                    
class TestBoard(unittest.TestCase):

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

    def test_isMoveValid_whiteMovingForwardMoreThanOneTileAway(self):
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

    def test_isMoveValid_whiteMovingToSide(self):
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

    def test_isMoveValid_whiteMovingBackward(self):
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
        
    def test_isMoveValid_whiteMovingForwardToEmptySlotAndNoWinner(self):
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

    def test_isMoveValid_whiteMovingForwardToEmptySlotAndWhiteWins(self):
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
        
    def test_isMoveValid_whiteMovingForwardToNonEmptySlot(self):
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

    def test_isMoveValid_whiteMovingDiagonalRightToBlackPawnAndNoWinner(self):
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
        
    def test_isMoveValid_whiteMovingDiagonalRightToBlackPawnAndWinner(self):
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
        
    def test_isMoveValid_whiteMovingDiagonalRightToEmptySlot(self):
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

    def test_isMoveValid_whiteMovingDiagonalLeftToBlackPawnAndNoWinner(self):
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
        
    def test_isMoveValid_whiteMovingDiagonalLeftToBlackPawnAndWinner(self):
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
        
    def test_isMoveValid_whiteMovingDiagonalLeftToEmptySlot(self):
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

    def test_isMoveValid_blackMovingForwardMoreThanOneTileAway(self):
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

    def test_isMoveValid_blackMovingToSide(self):
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

    def test_isMoveValid_blackMovingBackward(self):
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
        
    def test_isMoveValid_blackMovingForwardToEmptySlotAndNoWinner(self):
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

    def test_isMoveValid_blackMovingForwardToEmptySlotAndWhiteWins(self):
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
        
    def test_isMoveValid_blackMovingForwardToNonEmptySlot(self):
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

    def test_isMoveValid_blackMovingDiagonalRightToBlackPawnAndNoWinner(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "B W -",
                "- W B",
                "- - -",
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
                "- W -",
                "- B B",
                "- - -",
            ])
        
    def test_isMoveValid_blackMovingDiagonalRightToWhitePawnAndWinner(self):
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
        
    def test_isMoveValid_blackMovingDiagonalRightToEmptySlot(self):
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

    def test_isMoveValid_blackMovingDiagonalLeftToWhitePawnAndNoWinner(self):
        board = Board()

        # setup
        TestBoardUtil.setBoard(
            board,
            [
                "- W B",
                "B W -",
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
                "- W -",
                "B B -",
                "- - -"
            ])
        
    def test_isMoveValid_blackMovingDiagonalLeftToWhitePawnAndWinner(self):
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
        
    def test_isMoveValid_blackMovingDiagonalLeftToEmptySlot(self):
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
