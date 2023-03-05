from enum import Enum, IntEnum, auto
import re
from PyQt5 import QtGui
from hexapawn.board import *

class MoveColor(Enum):
    """
    Move colors. Use for setting the style of button for move.
    """
    GREEN   =  QtGui.QColor(0, 128, 0)
    RED     =  QtGui.QColor(255, 0, 0)
    BLUE    =  QtGui.QColor(0, 0, 255)
    YELLOW  =  QtGui.QColor(255, 255, 0)

class Movement(IntEnum):
    """
    Movement types.
    """
    FORWARD         = auto()
    DIAGONAL_RIGHT  = auto()
    DIAGONAL_LEFT   = auto()

class Move():
    """
    Move.
    """

    position = None
    """Position of black pawn to move."""

    color = None
    """Movement color."""

    movement = None
    """Movement type : forward, diagonal left or diagonal right."""

    removed = False
    """Remove if resulted to lose."""

    def __init__(self,position:Position,color:MoveColor,movement:Movement) -> None:
        """
        Parameter
        ---------
        position : Position
            Position of black pawn to move.
        color : MoveColor
            Movement color.
        movement : Movement
            Movement type : forward, diagonal left or diagonal right.
        """
        assert type(position) == Position and not position == None
        assert type(color) == MoveColor and not color == None
        assert type(movement) == Movement and not movement == None
        self.position = position
        self.color = color
        self.movement = movement

    ######################################################################
    #                          public functions                          #
    ######################################################################

    def newPosition(self)->Position:
        """
        Calculates new position based on current position and movement type.

        Returns
        ---------
        Position : New position.
        """
        newRow = self.position.row
        newCol = self.position.col
        if self.movement == Movement.FORWARD:
            newRow+=1
        elif self.movement == Movement.DIAGONAL_LEFT:
            newRow+=1
            newCol-=1
        elif self.movement == Movement.DIAGONAL_RIGHT:
            newRow+=1
            newCol+=1
        return Position(newRow,newCol)
    
    def remove(self)->None:
        """
        Reset move.
        """
        self.removed = True

    def reset(self):
        """
        Reset move.
        """
        self.removed = False

class MoveRecord():
    """
    Move record.
    """

    turn = -1
    """Turn of move."""

    move = None
    """Move executed."""
    
    def __init__(self,turn:int,move:Move) -> None:
        """
        Parameter
        ---------
        turn : int
            Turn of move.
        move : Move
            Move executed.
        """
        assert type(turn) == int and turn >=1
        assert not move == None and type(move) == Move
        self.turn = turn
        self.move = move

class Box(Board):
    """
    Consist of possible moves specified by color.
    """

    BOARD_ROW_SETTING_REGEX = "^(B|W|-) (B|W|-) (B|W|-)$"
    """Regex to verify row for setting up board."""

    id = ""
    """ID  of box. Use to map with target button icon file."""

    turn = -1
    """Turn number."""

    moves = []
    """Moves for black player."""

    def __init__(self,id:str,turn:int,setup:list,moves:list) -> None:
        """
        Parameter
        ---------
        id : str
            ID  of box. Use to map with target button icon file.
        turn : int
            Turn number. Must be event.
        setup : list
            3-element string array to indicate setup. Each element specify pawn placement for row.\n
            "W" - indicates white pawn in tile.\n
            "B" - indicates black pawn in tile.\n
            "-" - indicates empty tile.\n
            Separated by space.
            Sample:\n
            [ "B B B", "- - -", "W W W" ] indicates first row of black pawns; second row of empty tiles, and third row of white pawns.\n
            The setup list must be in correct format.
        moves : list
            Moves for black player.
        """
        super().__init__()
        assert len(id) > 0
        assert type(turn) == int and turn > 0 and turn%2 == 0
        assert all(type(move)==Move for move in moves)
        Box._setPawnsFromStringSetup(self,setup)
        self.id = id
        self.turn = turn
        for move in moves:
            self._assertMove(move)
        self.moves = moves
        
    @staticmethod
    def _setPawnsFromStringSetup(board:Board,setup:list)->None:
        """
        Setups pawns in board based on specified setup list.

        Parameter
        ---------
        board : Board
            Board to setup.
        setup : list
            3-element string array to indicate setup. Each element specify pawn placement for row.\n
            "W" - indicates white pawn in tile.\n
            "B" - indicates black pawn in tile.\n
            "-" - indicates empty tile.\n
            Separated by space.
            Sample:\n
            [ "B B B", "- - -", "W W W" ] indicates first row of black pawns; second row of empty tiles, and third row of white pawns.\n
            The setup list must be in correct format.
        """
        assert type(setup) == list
        assert len(setup) == SIZE
        assert all(type(s) == str and re.match(Box.BOARD_ROW_SETTING_REGEX,s) for s in setup)
        board._blackPawns = []
        board._whitePawns = []
        for row in range(SIZE):
            tokens = setup[row].split(' ')
            for col in range(len(tokens)):
                char = tokens[col]
                if char == "B":
                    board._blackPawns.append(Pawn(Color.BLACK,Position(row,col)))
                elif char == "W":
                    board._whitePawns.append(Pawn(Color.WHITE,Position(row,col)))
        assert len(board._blackPawns) <= SIZE
        assert len(board._whitePawns) <= SIZE

    @staticmethod
    def _createAssertMoveError(description:str,turn:int,move:Move)->str:
        """
        Creates assertion error message for move.

        Parameter
        ---------
        description : str
            Description of error.
        turn : int
            Turn.
        move : Move
            Move causing assertion error.
        """
        assert type(description) == str
        assert type(turn) == int
        return "{} : [{},{}] {} : {}".format(
            turn,
            move.position.row,
            move.position.col,
            move.movement.name,
            description)

    def _assertMove(self,move:Move)->None:
        """
        Checks if move is valid.\n
        - The front of black pawns moving forward is empty tile.

        Parameter
        ---------
        move : Move
            Move to check.
        """
        position = move.position
        movement = move.movement
        blackPawn = self._getPawnInPosition(position)
        assert not blackPawn == None,\
            Box._createAssertMoveError("Move position must have black pawn.",self.turn,move)
        assert blackPawn.position.row < (SIZE-1),\
            Box._createAssertMoveError("Results to outside board.",self.turn,move)
        if movement == Movement.FORWARD:
            pawnInFront = self._getPawnInPosition(Position(position.row+1,position.col))
            assert pawnInFront == None,\
            Box._createAssertMoveError("Expecting empty tile in front.",self.turn,move)
        elif movement == Movement.DIAGONAL_LEFT:
            assert position.col > 0,\
            Box._createAssertMoveError("Results to outside board.",self.turn,move)
            pawnInLowerLeft = self._getPawnInPosition(Position(position.row+1,position.col-1))
            assert not pawnInLowerLeft == None and pawnInLowerLeft.color == Color.WHITE,\
                Box._createAssertMoveError("Expecting to take white pawn.",self.turn,move)
        elif movement == Movement.DIAGONAL_RIGHT:
            assert position.col < (SIZE-1),\
            Box._createAssertMoveError("Results to outside board.",self.turn,move)
            pawnInLowerRight = self._getPawnInPosition(Position(position.row+1,position.col+1))
            assert not pawnInLowerRight == None and pawnInLowerRight.color == Color.WHITE,\
                Box._createAssertMoveError("Expecting to take white pawn.",self.turn,move)

    ######################################################################
    #                          public functions                          #
    ######################################################################

    def reset(self):
        """
        Resets box.
        """
        for move in self.moves:
            move.reset()
        pass

class Computer():
    """
    Contains the boxes for possible moves for black player based on current
    pawn positions in board.
    """
    
    _boxes = [
        Box(
            "2A", 2,
            [
                "B B B",
                "W - -",
                "- W W"
            ],
            [
                Move(Position(0,1),MoveColor.GREEN,Movement.DIAGONAL_LEFT),
                Move(Position(0,1),MoveColor.RED,Movement.FORWARD),
                Move(Position(0,2),MoveColor.BLUE,Movement.FORWARD)
            ]
        ),
        Box(
            "2B", 2,
            [
                "B B B",
                "- W -",
                "W - W"
            ],
            [
                Move(Position(0,0),MoveColor.GREEN,Movement.FORWARD),
                Move(Position(0,0),MoveColor.RED,Movement.DIAGONAL_RIGHT)
            ]
        ),
        Box(
            "4A", 4,
            [
                "B - B",
                "B W -",
                "- - W"
            ],
            [
                Move(Position(0,0),MoveColor.RED,Movement.DIAGONAL_RIGHT),
                Move(Position(0,2),MoveColor.BLUE,Movement.DIAGONAL_LEFT),
                Move(Position(0,2),MoveColor.YELLOW,Movement.FORWARD),
                Move(Position(1,0),MoveColor.GREEN,Movement.FORWARD)
            ]
        ),
        Box(
            "4B", 4,
            [
                "- B B",
                "W B -",
                "- - W"
            ],
            [
                Move(Position(0,1),MoveColor.GREEN,Movement.DIAGONAL_LEFT),
                Move(Position(0,2),MoveColor.BLUE,Movement.FORWARD),
                Move(Position(1,1),MoveColor.RED,Movement.FORWARD)
            ]
        ),
        Box(
            "4C", 4,
            [
                "B - B",
                "W W -",
                "- W -"
            ],
            [
                Move(Position(0,0),MoveColor.GREEN,Movement.DIAGONAL_RIGHT),
                Move(Position(0,2),MoveColor.RED,Movement.DIAGONAL_LEFT),
                Move(Position(0,2),MoveColor.BLUE,Movement.FORWARD)
            ]
        ),
        Box(
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
        ),
        Box(
            "4E", 4,
            [
                "- B B",
                "- B W",
                "W - -"
            ],
            [
                Move(Position(0,1),MoveColor.RED,Movement.DIAGONAL_RIGHT),
                Move(Position(1,1),MoveColor.GREEN,Movement.DIAGONAL_LEFT),
                Move(Position(1,1),MoveColor.BLUE,Movement.FORWARD)
            ]
        ),
        Box(
            "4F", 4,
            [
                "- B B",
                "B W W",
                "W - -"
            ],
            [
                Move(Position(0,1),MoveColor.RED,Movement.DIAGONAL_RIGHT),
                Move(Position(0,2),MoveColor.GREEN,Movement.DIAGONAL_LEFT)
            ]
        ),
        Box(
            "4G", 4,
            [
                "B - B",
                "B - W",
                "- W -"
            ],
            [
                Move(Position(1,0),MoveColor.GREEN,Movement.FORWARD),
                Move(Position(1,0),MoveColor.RED,Movement.DIAGONAL_RIGHT)
            ]
        ),
        Box(
            "4H", 4,
            [
                "B B -",
                "W W B",
                "- - W"
            ],
            [
                Move(Position(0,0),MoveColor.RED,Movement.DIAGONAL_RIGHT),
                Move(Position(0,1),MoveColor.GREEN,Movement.DIAGONAL_LEFT)
            ]
        ),
        Box(
            "4I", 4,
            [
                "- B B",
                "- W -",
                "- - W"
            ],
            [
                Move(Position(0,2),MoveColor.GREEN,Movement.DIAGONAL_LEFT),
                Move(Position(0,2),MoveColor.RED,Movement.FORWARD)
            ]
        ),
        Box(
            "4J", 4,
            [
                "- B B",
                "- W -",
                "W - -"
            ],
            [
                Move(Position(0,2),MoveColor.GREEN,Movement.DIAGONAL_LEFT),
                Move(Position(0,2),MoveColor.RED,Movement.FORWARD)
            ]
        ),
        Box(
            "4K", 4,
            [
                "B - B",
                "W - -",
                "- - W"
            ],
            [
                Move(Position(0,2),MoveColor.GREEN,Movement.FORWARD)
            ]
        ),
        Box(
            "6A", 6,
            [
                "- - B",
                "B B W",
                "- - -"
            ],
            [
                Move(Position(1,0),MoveColor.GREEN,Movement.FORWARD),
                Move(Position(1,1),MoveColor.RED,Movement.FORWARD)
            ]
        ),
        Box(
            "6B", 6,
            [
                "B - -",
                "W W W",
                "- - -"
            ],
            [
                Move(Position(0,0),MoveColor.GREEN,Movement.DIAGONAL_RIGHT)
            ]
        ),
        Box(
            "6C", 6,
            [
                "- B -",
                "B W W",
                "- - -"
            ],
            [
                Move(Position(0,1),MoveColor.RED,Movement.DIAGONAL_RIGHT),
                Move(Position(1,0),MoveColor.GREEN,Movement.FORWARD)
            ]
        ),
        Box(
            "6D", 6,
            [
                "- B -",
                "W W B",
                "- - -"
            ],
            [
                Move(Position(0,1),MoveColor.GREEN,Movement.DIAGONAL_LEFT),
                Move(Position(1,2),MoveColor.RED,Movement.FORWARD)
            ]
        ),
        Box(
            "6E", 6,
            [
                "B - -",
                "B B W",
                "- - -"
            ],
            [
                Move(Position(1,0),MoveColor.GREEN,Movement.FORWARD),
                Move(Position(1,1),MoveColor.RED,Movement.FORWARD)
            ]
        ),
        Box(
            "6F", 6,
            [
                "- - B",
                "W B B",
                "- - -"
            ],
            [
                Move(Position(1,1),MoveColor.GREEN,Movement.FORWARD),
                Move(Position(1,2),MoveColor.RED,Movement.FORWARD)
            ]
        ),
        Box(
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
        ),
        Box(
            "6H", 6,
            [
                "- B -",
                "W B -",
                "- - -"
            ],
            [
                Move(Position(0,1),MoveColor.GREEN,Movement.DIAGONAL_LEFT),
                Move(Position(1,1),MoveColor.RED ,Movement.FORWARD)
            ]
        ),
        Box(
            "6I", 6,
            [
                "- B -",
                "- B W",
                "- - -"
            ],
            [
                Move(Position(0,1),MoveColor.RED,Movement.DIAGONAL_RIGHT),
                Move(Position(1,1),MoveColor.GREEN ,Movement.FORWARD)
            ]
        ),
        Box(
            "6J", 6,
            [
                "B - -",
                "B W -",
                "- - -"
            ],
            [
                Move(Position(0,0),MoveColor.RED,Movement.DIAGONAL_RIGHT),
                Move(Position(1,0),MoveColor.GREEN ,Movement.FORWARD)
            ]
        ),
        Box(
            "6K", 6,
            [
                "- - B",
                "- W B",
                "- - -"
            ],
            [
                Move(Position(0,2),MoveColor.GREEN,Movement.DIAGONAL_LEFT),
                Move(Position(1,2),MoveColor.RED ,Movement.FORWARD)
            ]
        ),
    ]
    """Boxes for black player moves."""

    def __init__(self) -> None:
        self._addMirrorsOfAsymmetricBoxes()
    
    def _addMirrorsOfAsymmetricBoxes(self)->None:
        """
        Adds mirrors of asymmetric boxexs.
        """
        mirroedBoxes = []
        # add symetric moves
        for box in self._boxes:
            if box.arePawnPositionsSymmetric() == False:
                # creat mirrored box
                mirroredBox = Computer._createMirroredBox(box)
                existingBox = next((b for b in self._boxes if areBoardsEqual(b,mirroredBox)),None)
                if existingBox == None:
                    print("Adding mirrored {}".format(mirroredBox.id))
                    mirroedBoxes.append(mirroredBox)
                else:
                    print("{} is mirror of {}.".format(box.id,existingBox.id))
        if len(mirroedBoxes)>0:
            # add mirrored boxes
            for box in mirroedBoxes:
                self._boxes.append(box)
                
    @staticmethod
    def _createMirroredBox(box:Box)->Box:
        """
        Creates mirror for box.

        Parameter
        ---------
        box : Box
            Box to create mirror from.

        Returns
        ---------
        Box : Mirrored box.
        """
        assert not box == None
        newSetting = []
        tilePositions = box.getTilePositions()
        for row in range(SIZE):
            rowStr = []
            for col in reversed(range(SIZE)):
                pawn = tilePositions[row][col]
                if pawn == None:
                    rowStr.append("-")
                elif pawn.color == Color.BLACK:
                    rowStr.append("B")
                elif pawn.color == Color.WHITE:
                    rowStr.append("W")
            newSetting.append(" ".join(rowStr))
        newMoves = []
        reversedCol = list(reversed(range(SIZE)))
        for move in box.moves:
            newPosition = Position(move.position.row,reversedCol[move.position.col])
            newMovement = Movement.FORWARD
            if move.movement == Movement.DIAGONAL_LEFT:
                newMovement = Movement.DIAGONAL_RIGHT
            elif move.movement == Movement.DIAGONAL_RIGHT:
                newMovement = Movement.DIAGONAL_LEFT
            newMoves.append(Move(newPosition,move.color,newMovement))
        box = Box( "{}r".format(box.id), box.turn, newSetting, newMoves )
        return box

    ######################################################################
    #                          public functions                          #
    ######################################################################

    def getBoxForCurrentBlackTurn(self,turn:int,currentBoard:Board)->Box:
        """
        Checks if move is valid.\n
        - The front of black pawns moving forward is empty tile.

        Parameter
        ---------
        turn : int
            Turn. Must be even number.
        currentBoard : Board
            Board.

        Returns
        ---------
        Box : Box for current turn based on board pawn positions. None if box is not found.
        """
        assert turn >= 2 and (turn%2) == 0
        assert not currentBoard == None
        boxForTurn = None
        boxesWithTurn = list(filter(lambda x : x.turn == turn, self._boxes))
        for box in boxesWithTurn:
            if areBoardsEqual(box,currentBoard):
                boxForTurn = box
                break  
        return boxForTurn
    
    def resetIntelligence(self)->None:
        """
        Resets intelligence of computer.
        """
        for box in self._boxes:
            box.reset()
