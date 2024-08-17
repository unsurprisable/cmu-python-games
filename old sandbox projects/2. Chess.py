# August 2023

from enum import Enum
import datetime
import time
import random



class Color(Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"

class Piece(Enum):
    EMPTY = 0
    PAWN = 1
    KING = 2
    QUEEN = 3
    BISHOP = 4
    KNIGHT = 5
    ROOK = 6

class Visual(Enum):
    EMPTY = ''
    W_PAWN = chr(0x2659)
    W_KING = chr(0x2654)
    W_QUEEN = chr(0x2655)
    W_BISHOP = chr(0x2657)
    W_KNIGHT = chr(0x2658)
    W_ROOK = chr(0x2656)
    
    B_PAWN = chr(0x265f)
    B_KING = chr(0x265a)
    B_QUEEN = chr(0x265b)
    B_BISHOP = chr(0x265d)
    B_KNIGHT = chr(0x265e)
    B_ROOK = chr(0x265c)
    
class Condition(Enum):
    CHECKMATE = "CHECKMATE"
    TIME = "TIME"



class SquareProperties():
    def __init__(self, parent, row, col, fillColor):
        self.parent = parent
        self.row = row
        self.col = col
        
        self.color = None
        self._piece = Piece.EMPTY
        
        self.fillColor = fillColor
        self.baseFillColor = fillColor
        
        self.hasMoved = False
        
        self.enPassant = False
        
    @property
    def piece(self):
        return self._piece
    @piece.setter
    def piece(self, newPiece):
        self._piece = newPiece
        if (self.piece == Piece.EMPTY):
            self.parent.visual.value = Visual.EMPTY.value
            
        elif (self.color == Color.WHITE):
            if (self.piece == Piece.PAWN): self.parent.visual.value = Visual.W_PAWN.value
            elif (self.piece == Piece.KNIGHT): self.parent.visual.value = Visual.W_KNIGHT.value
            elif (self.piece == Piece.BISHOP): self.parent.visual.value = Visual.W_BISHOP.value
            elif (self.piece == Piece.ROOK): self.parent.visual.value = Visual.W_ROOK.value
            elif (self.piece == Piece.QUEEN): self.parent.visual.value = Visual.W_QUEEN.value
            elif (self.piece == Piece.KING): self.parent.visual.value = Visual.W_KING.value
            
        elif (self.color == Color.BLACK):
            if (self.piece == Piece.PAWN): self.parent.visual.value = Visual.B_PAWN.value
            elif (self.piece == Piece.KNIGHT): self.parent.visual.value = Visual.B_KNIGHT.value
            elif (self.piece == Piece.BISHOP): self.parent.visual.value = Visual.B_BISHOP.value
            elif (self.piece == Piece.ROOK): self.parent.visual.value = Visual.B_ROOK.value
            elif (self.piece == Piece.QUEEN): self.parent.visual.value = Visual.B_QUEEN.value
            elif (self.piece == Piece.KING): self.parent.visual.value = Visual.B_KING.value

class Move:
    def __init__(self, newSquare, square):
        self.newSquare = newSquare
        self.square = square
        
        self.newProperties = newSquare.properties
        self.properties = square.properties
        
        self.newRow = newSquare.properties.row
        self.newCol = newSquare.properties.col
        self.row = square.properties.row
        self.col = square.properties.col
        
        self.color = square.properties.color
        
        self.newPiece = newSquare.properties.piece
        self.piece = square.properties.piece
        
        self.enPassant = False
        self.enPassantPerformed = False
        
        self.castling = False




    
def ChangeTurn(turnColor = None):
    if (board.gameOver): return
    
    if (not turnColor == None):
        app.turnColor = turnColor
    else:
        if (app.turnColor == Color.WHITE):
            app.turnColor = Color.BLACK
        else:
            app.turnColor = Color.WHITE
    
    if (app.turnColor == Color.WHITE):
        app.turnText.value = 'White To Move'
        app.turnText.fill = gradient('white', board.whiteColor, start='right')
    else:
        app.turnText.value = 'Black To Move'
        app.turnText.fill = gradient('maroon', 'saddleBrown', start='right')
        




def SelectPiece(square):
    if (square == board.selectedSquare):
        Deselect()
        
    elif (square.properties.color == app.turnColor):
        if (board.selectedSquare != None): board.selectedSquare.fill = board.selectedSquare.properties.fillColor
        
        square.fill = board.selectedSquareColor
        board.selectedSquare = square
    elif (board.selectedSquare != None):
        board.selectedSquare.fill = board.selectedSquare.properties.fillColor
        board.selectedSquare = None
        
    if (board.selectedSquare != None):
        FindLegalMoves(board.selectedSquare)
        
        
        
def Deselect():
    if (board.selectedSquare != None):
        board.selectedSquare.fill = board.selectedSquare.properties.fillColor
        board.selectedSquare = None
    if (len(board.legalMoves) != 0):
        for move in board.legalMoves:
            move.newSquare.fill = move.newSquare.properties.fillColor
        board.legalMoves.clear()



def DeletePiece(square):
    square.properties.color = None
    square.properties.piece = Piece.EMPTY



def ChangePiece(square, color, piece):
    properties = square.properties
    properties.color = color
    properties.piece = piece
    
    if (piece == Piece.KING and color == Color.WHITE):
        board.whiteKingSquare = square
    elif (piece == Piece.KING and color == Color.BLACK):
        board.blackKingSquare = square



def MovePiece(move):
    app.gameHasStarted = True
    
    piece = move.properties.piece
    color = move.properties.color
    
    DeletePiece(move.square)
    
    move.newProperties.color = color
    move.newProperties.piece = piece
    
    move.properties.hasMoved = True
    move.newProperties.hasMoved = True
    
    for square in board:
        square.properties.enPassant = False
    
    if (move.enPassant):
        move.newProperties.enPassant = True
    if (move.enPassantPerformed):
        DeletePiece(board.square[move.row][move.newCol])
        
    if (move.castling):
        print("Castled")
        if (move.col+2 == move.newCol):
            DeletePiece(board.square[move.row][move.col+3])
            ChangePiece(board.square[move.row][move.col+1], move.color, Piece.ROOK)
        elif (move.col-2 == move.newCol):
            DeletePiece(board.square[move.row][move.col-4])
            ChangePiece(board.square[move.row][move.col-1], move.color, Piece.ROOK)
        
    # Promotion
    if (move.piece == Piece.PAWN):
        if (move.color == Color.WHITE and move.newRow == 7):
            move.newProperties.piece = Piece.QUEEN
        elif (move.color == Color.BLACK and move.newRow == 0):
            move.newProperties.piece = Piece.QUEEN
            
    
    # Update King Caches
    if (move.piece == Piece.KING and move.properties.color == Color.WHITE):
        board.whiteKingSquare = move.newSquare
    elif (move.piece == Piece.KING and move.properties.color == Color.BLACK):
        board.blackKingSquare = move.newSquare
        
        
    Deselect()

    # Check
    if (app.turnColor == Color.WHITE and KingIsChecked()):
        board.blackKingSquare.properties.fillColor = board.checkedColor
        board.blackKingSquare.fill = board.checkedColor
    elif (app.turnColor == Color.BLACK and KingIsChecked()):
        board.whiteKingSquare.properties.fillColor = board.checkedColor
        board.whiteKingSquare.fill = board.checkedColor
        
    # Clear the check visual
    else: 
        board.blackKingSquare.properties.fillColor = board.blackKingSquare.properties.baseFillColor
        board.blackKingSquare.fill = board.blackKingSquare.properties.fillColor
        
        board.whiteKingSquare.properties.fillColor = board.whiteKingSquare.properties.baseFillColor
        board.whiteKingSquare.fill = board.whiteKingSquare.properties.fillColor
    
    
    ChangeTurn()

    # Checkmate
    if (app.turnColor == Color.WHITE and not FindAnyLegalMove(Color.WHITE)):
        board.whiteKingSquare.fill = board.checkmateColor
        GameOver(Color.BLACK, Condition.CHECKMATE)
        return
    elif (app.turnColor == Color.BLACK and not FindAnyLegalMove(Color.BLACK)):
        board.blackKingSquare.fill = board.checkmateColor
        GameOver(Color.WHITE, Condition.CHECKMATE)
        return
    
    board.triggerBotMove = True
    
    app.botMoveTime = 0
    
def BotMove():
    startTime = time.time()
    # Bot Move
    if (board.playingBot and app.turnColor == Color.BLACK):
        if (len(board.botLegalMoves) != 0):
            board.botLegalMoves.clear()
        
        for square in board:
            if (square.properties.color == Color.BLACK):
                FindLegalMoves(square, False)
                for move in board.legalMoves:
                    if (move.newSquare.properties.piece != Piece.EMPTY):
                        MovePiece(move)
                        return
                    else:
                        board.botLegalMoves.append(move)
        
        if (len(board.botLegalMoves) != 0):
            index = random.randint(0, len(board.botLegalMoves)-1)
            MovePiece(board.botLegalMoves[index])
            timeToMove = time.time() - startTime
            app.botMoveTime += timeToMove
            if (int(app.botMoveTime) > 0):
                app.blackTimer -= int(app.botMoveTime)
                app.blackTimerText.value = str(datetime.timedelta(seconds=app.blackTimer)).rsplit(':', 2)[1] + ':' + str(datetime.timedelta(seconds=app.blackTimer)).rsplit(':', 2)[2]
                app.botMoveTime -= int(app.botMoveTime)
            



# Checks if the OPPONENT is in check (call this after a move and before the turn switches)
def KingIsChecked(overrideColor = None):
    color = overrideColor if (overrideColor != None) else app.turnColor
    
    if (len(board.allLegalMoves) != 0):
        board.allLegalMoves.clear()
    
    for square in board:
        if (square.properties.color == color):
            FindLegalMoves(square, False, False)
            for legalMove in board.allLegalMoves:
                if (legalMove.newProperties.piece == Piece.KING and legalMove.newProperties.color != color):
                    print(f"\n{color.value} opposing king is checked by square {legalMove.row}, {legalMove.col}")
                    return True
                    
    return False



def KingIsCheckedAfterMove(move):
    oldPiece = move.properties.piece
    oldColor = move.properties.color
    
    oldNewPiece = move.newProperties.piece
    oldNewColor = move.newProperties.color
    
    move.properties._piece = Piece.EMPTY
    move.properties.color = None
    
    move.newProperties._piece = move.piece
    move.newProperties.color = move.color
    
    color = Color.WHITE if (app.turnColor == Color.BLACK) else Color.BLACK
    
    isKingChecked = KingIsChecked(color)
    
    move.properties._piece = oldPiece
    move.properties.color = oldColor
    
    move.newProperties._piece = oldNewPiece
    move.newProperties.color = oldNewColor
    
    print(f"My king is checked after move: {move.row}, {move.col} TO {move.newRow}, {move.newCol}... = {isKingChecked}")
    return isKingChecked
            


def FindAnyLegalMove(color):
    for square in board:
        if (square.properties.color == color):
            FindLegalMoves(square, False, True)
            if (len(board.legalMoves) == 0):
                print(f"Couldn't find a legal move for {square.properties.row}, {square.properties.col}, color {color.value}")
                continue
            else:
                print(f"Found a legal move for {square.properties.row}, {square.properties.col}, color {color.value}")
                return True
    # No legal moves at all
    print(f"Couldn't find any legal moves for {color.value}")
    return False



def FindLegalMoves(square, showGraphic = True, lookAhead = True):
    row = square.properties.row
    col = square.properties.col
    color = square.properties.color
    piece = square.properties.piece
    hasMoved = square.properties.hasMoved
    
    if (lookAhead and len(board.legalMoves) != 0):
        for move in board.legalMoves:
            move.newSquare.fill = move.newSquare.properties.fillColor
        board.legalMoves.clear()
    
    for newSquare in board:
        newRow = newSquare.properties.row
        newCol = newSquare.properties.col
        newColor = newSquare.properties.color
        newPiece = newSquare.properties.piece
        
        # PAWN
        if (piece == Piece.PAWN):
            if (color == Color.WHITE):
                if (row+1 == newRow and col == newCol and newPiece == Piece.EMPTY):
                    move = Move(newSquare, square)
                    if (lookAhead and not KingIsCheckedAfterMove(move)):
                        board.legalMoves.append(move)
                    elif (not lookAhead):
                        board.allLegalMoves.append(move)
                    continue
                elif (row+1 == newRow and (col+1 == newCol or col-1 == newCol) and newPiece != Piece.EMPTY and newColor != color):
                    move = Move(newSquare, square)
                    if (lookAhead and not KingIsCheckedAfterMove(move)):
                        board.legalMoves.append(move)
                    elif (not lookAhead):
                        board.allLegalMoves.append(move)
                    continue
                elif (not hasMoved and row+2 == newRow and col == newCol and newPiece == Piece.EMPTY and board.square[row+1][col].properties.piece == Piece.EMPTY):
                    move = Move(newSquare, square)
                    if (lookAhead and not KingIsCheckedAfterMove(move)):
                        move.enPassant = True
                        board.legalMoves.append(move)
                    elif (not lookAhead):
                        board.allLegalMoves.append(move)
                    continue
                elif (row+1 == newRow and col+1 == newCol and board.square[row][col+1].properties.enPassant):
                    move = Move(newSquare, square)
                    if (lookAhead and not KingIsCheckedAfterMove(move)):
                        move.enPassantPerformed = True
                        board.legalMoves.append(move)
                    elif (not lookAhead):
                        board.allLegalMoves.append(move)
                    continue
                elif (row+1 == newRow and col-1 == newCol and board.square[row][col-1].properties.enPassant):
                    move = Move(newSquare, square)
                    if (lookAhead and not KingIsCheckedAfterMove(move)):
                        move.enPassantPerformed = True
                        board.legalMoves.append(move)
                    elif (not lookAhead):
                        board.allLegalMoves.append(move)
                    continue
                
            elif (color == Color.BLACK):
                if (row-1 == newRow and col == newCol and newPiece == Piece.EMPTY):
                    move = Move(newSquare, square)
                    if (lookAhead and not KingIsCheckedAfterMove(move)):
                        board.legalMoves.append(move)
                    elif (not lookAhead):
                        board.allLegalMoves.append(move)
                    continue
                elif (row-1 == newRow and (col+1 == newCol or col-1 == newCol) and newPiece != Piece.EMPTY and newColor != color):
                    move = Move(newSquare, square)
                    if (lookAhead and not KingIsCheckedAfterMove(move)):
                        board.legalMoves.append(move)
                    elif (not lookAhead):
                        board.allLegalMoves.append(move)
                    continue
                elif (not hasMoved and row-2 == newRow and col == newCol and newPiece == Piece.EMPTY and board.square[row-1][col].properties.piece == Piece.EMPTY):
                    move = Move(newSquare, square)
                    if (lookAhead and not KingIsCheckedAfterMove(move)):
                        move.enPassant = True
                        board.legalMoves.append(move)
                    elif (not lookAhead):
                        board.allLegalMoves.append(move)
                    continue
                elif (row-1 == newRow and col+1 == newCol and board.square[row][col+1].properties.enPassant):
                    move = Move(newSquare, square)
                    if (lookAhead and not KingIsCheckedAfterMove(move)):
                        move.enPassantPerformed = True
                        board.legalMoves.append(move)
                    elif (not lookAhead):
                        board.allLegalMoves.append(move)
                    continue
                elif (row-1 == newRow and col-1 == newCol and board.square[row][col-1].properties.enPassant):
                    move = Move(newSquare, square)
                    if (lookAhead and not KingIsCheckedAfterMove(move)):
                        move.enPassantPerformed
                        board.legalMoves.append(move)
                    elif (not lookAhead):
                        board.allLegalMoves.append(move)
                    continue
                
        # KNIGHT
        elif (piece == Piece.KNIGHT):
            if  (
                (row+2 == newRow and col+1 == newCol) or
                (row+1 == newRow and col+2 == newCol) or
                (row-1 == newRow and col+2 == newCol) or
                (row-2 == newRow and col+1 == newCol) or
                (row-2 == newRow and col-1 == newCol) or
                (row-1 == newRow and col-2 == newCol) or
                (row+1 == newRow and col-2 == newCol) or
                (row+2 == newRow and col-1 == newCol)
                ):
                if (newColor != color):
                    move = Move(newSquare, square)
                    if (lookAhead and not KingIsCheckedAfterMove(move)):
                        board.legalMoves.append(move)
                    elif (not lookAhead):
                        board.allLegalMoves.append(move)
                    continue
                
        # BISHOP
        elif (piece == Piece.BISHOP):
            vertDir = newRow - row
            horzDir = newCol - col
            
            if (abs(vertDir) == abs(horzDir)):
                isObstructed = False
                for i in range(abs(vertDir)-1):
                    vertAdd = i+1
                    horzAdd = i+1
                    
                    if (vertDir < 0): vertAdd = -vertAdd
                    if (horzDir < 0): horzAdd = -horzAdd
                    
                    # if there is a piece found along the path from the selected square 'square' to the new square 'newSquare'
                    if (board.square[row+vertAdd][col+horzAdd].properties.piece != Piece.EMPTY):
                        isObstructed = True
                        break
                    
                if (not isObstructed and newColor != color):
                    move = Move(newSquare, square)
                    if (lookAhead and not KingIsCheckedAfterMove(move)):
                        board.legalMoves.append(move)
                    elif (not lookAhead):
                        board.allLegalMoves.append(move)
                    
                continue
              
        # ROOK  
        elif (piece == Piece.ROOK):
            
            isObstructed = False
            if (row == newRow and col != newCol):
                # horizontal
                horzDir = newCol - col
                
                for i in range(abs(horzDir)-1):
                    horzAdd = i+1
                    
                    if (horzDir < 0): horzAdd = -horzAdd
                    
                    # if there is a piece found along the path from the selected square 'square' to the new square 'newSquare'
                    if (board.square[row][col+horzAdd].properties.piece != Piece.EMPTY):
                        isObstructed = True
                        break
                    
            elif (row != newRow and col == newCol):
                # vertical
                vertDir = newRow - row
                
                for i in range(abs(vertDir)-1):
                    vertAdd = i+1
                    
                    if (vertDir < 0): vertAdd = -vertAdd
                    
                    # if there is a piece found along the path from the selected square 'square' to the new square 'newSquare'
                    if (board.square[row+vertAdd][col].properties.piece != Piece.EMPTY):
                        isObstructed = True
                        break
            
            else:
                isObstructed = True
                
            if (not isObstructed and newColor != color):
                move = Move(newSquare, square)
                if (lookAhead and not KingIsCheckedAfterMove(move)):
                    board.legalMoves.append(move)
                elif (not lookAhead):
                    board.allLegalMoves.append(move)
                    
            continue
            
        # QUEEN
        elif (piece == Piece.QUEEN):
            vertDir = newRow - row
            horzDir = newCol - col
            
            if (abs(vertDir) == abs(horzDir)):
                isObstructed = False
                for i in range(abs(vertDir)-1):
                    vertAdd = i+1
                    horzAdd = i+1
                    
                    if (vertDir < 0): vertAdd = -vertAdd
                    if (horzDir < 0): horzAdd = -horzAdd
                    
                    # if there is a piece found along the path from the selected square 'square' to the new square 'newSquare'
                    if (board.square[row+vertAdd][col+horzAdd].properties.piece != Piece.EMPTY):
                        isObstructed = True
                        break
                    
                if (not isObstructed and newColor != color):
                    move = Move(newSquare, square)
                    if (lookAhead and not KingIsCheckedAfterMove(move)):
                        board.legalMoves.append(move)
                    elif (not lookAhead):
                        board.allLegalMoves.append(move)
                    
                continue
            
            isObstructed = False
            if (row == newRow and col != newCol):
                # horizontal
                horzDir = newCol - col
                
                for i in range(abs(horzDir)-1):
                    horzAdd = i+1
                    
                    if (horzDir < 0): horzAdd = -horzAdd
                    
                    # if there is a piece found along the path from the selected square 'square' to the new square 'newSquare'
                    if (board.square[row][col+horzAdd].properties.piece != Piece.EMPTY):
                        isObstructed = True
                        break
                    
            elif (row != newRow and col == newCol):
                # vertical
                vertDir = newRow - row
                
                for i in range(abs(vertDir)-1):
                    vertAdd = i+1
                    
                    if (vertDir < 0): vertAdd = -vertAdd
                    
                    # if there is a piece found along the path from the selected square 'square' to the new square 'newSquare'
                    if (board.square[row+vertAdd][col].properties.piece != Piece.EMPTY):
                        isObstructed = True
                        break
            
            else:
                isObstructed = True
                
            if (not isObstructed and newColor != color):
                move = Move(newSquare, square)
                if (lookAhead and not KingIsCheckedAfterMove(move)):
                    board.legalMoves.append(move)
                elif (not lookAhead):
                    board.allLegalMoves.append(move)
                    
            continue
        
        # KING
        elif (piece == Piece.KING):
            if ((
                (row+1 == newRow and col == newCol) or
                (row+1 == newRow and col+1 == newCol) or
                (row == newRow and col+1 == newCol) or
                (row-1 == newRow and col+1 == newCol) or
                (row-1 == newRow and col == newCol) or
                (row-1 == newRow and col-1 == newCol) or
                (row == newRow and col-1 == newCol) or
                (row+1 == newRow and col-1 == newCol))
                and (newColor != color)
                ):
                move = Move(newSquare, square)
                if (lookAhead and not KingIsCheckedAfterMove(move)):
                    board.legalMoves.append(move)
                elif (not lookAhead):
                    board.allLegalMoves.append(move)
                continue
            elif (row == newRow and col+2 == newCol and not hasMoved and (not board.square[row][col+3].properties.hasMoved and board.square[row][col+3].properties.piece == Piece.ROOK) and board.square[row][col+1].properties.piece == Piece.EMPTY):
                move = Move(newSquare, square)
                secMove = Move(board.square[row][col+1], square)
                if (lookAhead and not KingIsCheckedAfterMove(move) and not KingIsCheckedAfterMove(secMove)):
                    move.castling = True
                    board.legalMoves.append(move)
                elif (not lookAhead):
                    board.allLegalMoves.append(move)
            elif (row == newRow and col-2 == newCol and not hasMoved and (not board.square[row][col-4].properties.hasMoved and board.square[row][col-4].properties.piece == Piece.ROOK) and board.square[row][col-1].properties.piece == Piece.EMPTY and board.square[row][col-3].properties.piece == Piece.EMPTY):
                move = Move(newSquare, square)
                secMove = Move(board.square[row][col-2], square)
                thrMove = Move(board.square[row][col-1], square)
                if (lookAhead and not KingIsCheckedAfterMove(move) and not KingIsCheckedAfterMove(secMove) and not KingIsCheckedAfterMove(thrMove)):
                    move.castling = True
                    board.legalMoves.append(move)
                elif (not lookAhead):
                    board.allLegalMoves.append(move)
    
    if (showGraphic):
        for move in board.legalMoves:
            move.newSquare.fill = board.legalMoveColor


def MoveIsLegal(move):
    for legalMove in board.legalMoves:
        if (legalMove.newSquare == move.newSquare and legalMove.square == move.square):
            if (legalMove.enPassant): move.enPassant = True
            if (legalMove.enPassantPerformed): move.enPassantPerformed = True
            if (legalMove.castling): move.castling = True
            return True
    # else:
    Deselect()
    return False
        
        

def GameOver(winningColor, winCondition):
    board.gameOver = True
    app.gameHasStarted = False
    
    
    if (winCondition == Condition.CHECKMATE):
        if (winningColor == Color.WHITE):
            textBackground = Rect(0, 275, 400, 125, fill='white')
            Label("WHITE WINS BY CHECKMATE!", textBackground.centerX, textBackground.centerY, size=24, font='monospace', bold=True)
        elif (winningColor == Color.BLACK):
            textBackground = Rect(0, 75, 400, 125, fill='white')
            Label("BLACK WINS BY CHECKMATE!", textBackground.centerX, textBackground.centerY, size=24, font='monospace', bold=True)
    elif (winCondition == Condition.TIME):
        if (winningColor == Color.WHITE):
            textBackground = Rect(0, 275, 400, 125, fill='white')
            Label("WHITE WINS ON TIME!", textBackground.centerX, textBackground.centerY, size=24, font='monospace', bold=True)
        elif (winningColor == Color.BLACK):
            textBackground = Rect(0, 75, 400, 125, fill='white')
            Label("BLACK WINS ON TIME!", textBackground.centerX, textBackground.centerY, size=24, font='monospace', bold=True)
            
    app.stop()
            
    
    
    
    
    

##### AWAKE #####

app.background = gradient('peru', 'sienna', 'chocolate', 'darkGoldenrod', start='top-left')

board = Group()

board.square = makeList(8, 8)
board.horizontalGap = 64
board.verticalGap = 64

board.squareSize = (400-board.horizontalGap)/8
board.pieceSize = 40

board.whiteColor = 'antiqueWhite'
board.blackColor = rgb(240, 169, 120)

board.notationSize = 22
board.notationColor = 'wheat'

board.selectedSquare = None
board.selectedSquareColor = 'limeGreen'

board.legalMoves = []
board.legalMoveColor = 'gold'

board.allLegalMoves = []

board.whiteKingSquare = None
board.blackKingSquare = None

board.checkedColor = 'salmon'
board.checkmateColor = 'crimson'
board.checkmateMoveCheck = []

board.gameOver = False

board.playingBot = False
board.triggerBotMove = False
board.botLegalMoves = []

# Generate board using sizes & colors
for row in range(len(board.square)):
    for col in range(len(board.square[row])):
        square = Rect(board.horizontalGap/2 + (board.squareSize*col), board.verticalGap/2 + (board.squareSize*row), board.squareSize, board.squareSize)

        square.visual = Label('', square.centerX, square.centerY, size=board.pieceSize, font='symbols')
        
        if (row%2 == 0):
            if (col%2 == 0):
                square.fill = board.whiteColor
                square.properties = SquareProperties(square, 7-row, col, board.whiteColor)
            else:
                square.fill = board.blackColor
                square.properties = SquareProperties(square, 7-row, col, board.blackColor)
        else:
            if (col%2 == 1):
                square.fill = board.whiteColor
                square.properties = SquareProperties(square, 7-row, col, board.whiteColor)
            else:
                square.fill = board.blackColor
                square.properties = SquareProperties(square, 7-row, col, board.blackColor)
                
        print(f"\nPlaced:")
        print(square.properties.row)
        print(square.properties.col)
        
        board.add(square)
        board.square[7-row][col] = square
        
##### AWAKE #####





        

##### START #####

### Notation
horizontalPos = board.square[0][0].left - (board.horizontalGap/5)
Label('8', horizontalPos, board.square[7][0].centerY, size=board.notationSize, fill=board.notationColor, bold=True)
Label('7', horizontalPos, board.square[6][0].centerY, size=board.notationSize, fill=board.notationColor, bold=True)
Label('6', horizontalPos, board.square[5][0].centerY, size=board.notationSize, fill=board.notationColor, bold=True)
Label('5', horizontalPos, board.square[4][0].centerY, size=board.notationSize, fill=board.notationColor, bold=True)
Label('4', horizontalPos, board.square[3][0].centerY, size=board.notationSize, fill=board.notationColor, bold=True)
Label('3', horizontalPos, board.square[2][0].centerY, size=board.notationSize, fill=board.notationColor, bold=True)
Label('2', horizontalPos, board.square[1][0].centerY, size=board.notationSize, fill=board.notationColor, bold=True)
Label('1', horizontalPos, board.square[0][0].centerY, size=board.notationSize, fill=board.notationColor, bold=True)

verticalPos = board.square[0][0].bottom + (board.verticalGap/5)
Label('a', board.square[0][0].centerX, verticalPos, size=board.notationSize, fill=board.notationColor, bold=True)
Label('b', board.square[0][1].centerX, verticalPos, size=board.notationSize, fill=board.notationColor, bold=True)
Label('c', board.square[0][2].centerX, verticalPos, size=board.notationSize, fill=board.notationColor, bold=True)
Label('d', board.square[0][3].centerX, verticalPos, size=board.notationSize, fill=board.notationColor, bold=True)
Label('e', board.square[0][4].centerX, verticalPos, size=board.notationSize, fill=board.notationColor, bold=True)
Label('f', board.square[0][5].centerX, verticalPos, size=board.notationSize, fill=board.notationColor, bold=True)
Label('g', board.square[0][6].centerX, verticalPos, size=board.notationSize, fill=board.notationColor, bold=True)
Label('h', board.square[0][7].centerX, verticalPos, size=board.notationSize, fill=board.notationColor, bold=True)


### Piece Setup

# White
ChangePiece(board.square[1][0], Color.WHITE, Piece.PAWN)
ChangePiece(board.square[1][1], Color.WHITE, Piece.PAWN)
ChangePiece(board.square[1][2], Color.WHITE, Piece.PAWN)
ChangePiece(board.square[1][3], Color.WHITE, Piece.PAWN)
ChangePiece(board.square[1][4], Color.WHITE, Piece.PAWN)
ChangePiece(board.square[1][5], Color.WHITE, Piece.PAWN)
ChangePiece(board.square[1][6], Color.WHITE, Piece.PAWN)
ChangePiece(board.square[1][7], Color.WHITE, Piece.PAWN)

ChangePiece(board.square[0][0], Color.WHITE, Piece.ROOK)
ChangePiece(board.square[0][1], Color.WHITE, Piece.KNIGHT)
ChangePiece(board.square[0][2], Color.WHITE, Piece.BISHOP)
ChangePiece(board.square[0][3], Color.WHITE, Piece.QUEEN)
ChangePiece(board.square[0][4], Color.WHITE, Piece.KING)
ChangePiece(board.square[0][5], Color.WHITE, Piece.BISHOP)
ChangePiece(board.square[0][6], Color.WHITE, Piece.KNIGHT)
ChangePiece(board.square[0][7], Color.WHITE, Piece.ROOK)


# Black
ChangePiece(board.square[6][0], Color.BLACK, Piece.PAWN)
ChangePiece(board.square[6][1], Color.BLACK, Piece.PAWN)
ChangePiece(board.square[6][2], Color.BLACK, Piece.PAWN)
ChangePiece(board.square[6][3], Color.BLACK, Piece.PAWN)
ChangePiece(board.square[6][4], Color.BLACK, Piece.PAWN)
ChangePiece(board.square[6][5], Color.BLACK, Piece.PAWN)
ChangePiece(board.square[6][6], Color.BLACK, Piece.PAWN)
ChangePiece(board.square[6][7], Color.BLACK, Piece.PAWN)

ChangePiece(board.square[7][0], Color.BLACK, Piece.ROOK)
ChangePiece(board.square[7][1], Color.BLACK, Piece.KNIGHT)
ChangePiece(board.square[7][2], Color.BLACK, Piece.BISHOP)
ChangePiece(board.square[7][3], Color.BLACK, Piece.QUEEN)
ChangePiece(board.square[7][4], Color.BLACK, Piece.KING)
ChangePiece(board.square[7][5], Color.BLACK, Piece.BISHOP)
ChangePiece(board.square[7][6], Color.BLACK, Piece.KNIGHT)
ChangePiece(board.square[7][7], Color.BLACK, Piece.ROOK)



app.turnText = Label('', 200, board.square[7][0].top - board.verticalGap/4, size=28, font='monospace', bold=True)
ChangeTurn(Color.WHITE)

app.gameHasStarted = False

app.whiteTimer = 600
app.whiteTimerText = Label(str(datetime.timedelta(seconds=app.whiteTimer)).rsplit(':', 2)[1] + ':' + str(datetime.timedelta(seconds=app.whiteTimer)).rsplit(':', 2)[2], 40, 16, size=20, fill='black', bold=True, font='monospace')
app.whiteTimerButton = Rect(app.whiteTimerText.left-5, app.whiteTimerText.top-5, app.whiteTimerText.width+10, app.whiteTimerText.height+10, fill='white')
app.whiteTimerButton.toBack()

app.blackTimer = 600
app.blackTimerText = Label(str(datetime.timedelta(seconds=app.blackTimer)).rsplit(':', 2)[1] + ':' + str(datetime.timedelta(seconds=app.whiteTimer)).rsplit(':', 2)[2], 360, 16, size=20, fill='white', bold=True, font='monospace')
app.blackTimerButton = Rect(app.blackTimerText.left-5, app.blackTimerText.top-5, app.blackTimerText.width+10, app.blackTimerText.height+10, fill='black')
app.blackTimerButton.toBack()



app.introBackground = Rect(0,0,400,400,opacity=75)
app.introLabel = Label("(You can left/right click on the times to change them)", 200, 40, size=14, fill='white', bold=True)
app.botButton = Label("PLAY AGAINST BOT", 200, 170, size=32, fill='white', font='monospace', bold=True)
app.playerButton = Label("PLAY AGAINST PLAYER", 200, 230, size=30, fill='white', font='monospace', bold=True)

##### START #####
        
        
        
        
def OnBotButtonPress():
    app.introBackground.visible = False
    app.introLabel.visible = False
    app.botButton.visible = False
    app.playerButton.visible = False
    
    board.playingBot = True
    
def OnPlayerButtonPress():
    app.introBackground.visible = False
    app.introLabel.visible = False
    app.botButton.visible = False
    app.playerButton.visible = False
    
def OnWhiteTimerPress(button):
    if (app.gameHasStarted): return

    if (button == 0):
        if (app.whiteTimer < 10):
            app.whiteTimer += 1
        elif (app.whiteTimer < 30):
            app.whiteTimer += 2
        elif (app.whiteTimer < 180):
            app.whiteTimer += 30
        elif (app.whiteTimer < 600):
            app.whiteTimer += 60
        elif (app.whiteTimer < 1500):
            app.whiteTimer += 150
        elif (app.whiteTimer < 3000):
            app.whiteTimer += 300
    elif (button == 2):
        if (app.whiteTimer > 1500):
            app.whiteTimer -= 300
        elif (app.whiteTimer > 600):
            app.whiteTimer -= 150
        elif (app.whiteTimer > 180):
            app.whiteTimer -= 60
        elif (app.whiteTimer > 30):
            app.whiteTimer -= 30
        elif (app.whiteTimer > 10):
            app.whiteTimer -= 2
        elif (app.whiteTimer > 1):
            app.whiteTimer -= 1
    app.whiteTimerText.value = str(datetime.timedelta(seconds=app.whiteTimer)).rsplit(':', 2)[1] + ':' + str(datetime.timedelta(seconds=app.whiteTimer)).rsplit(':', 2)[2]

def OnBlackTimerPress(button):
    if (app.gameHasStarted): return
    
    if (button == 0):
        if (app.blackTimer < 10):
            app.blackTimer += 1
        elif (app.blackTimer < 30):
            app.blackTimer += 2
        elif (app.blackTimer < 180):
            app.blackTimer += 30
        elif (app.blackTimer < 600):
            app.blackTimer += 60
        elif (app.blackTimer < 1500):
            app.blackTimer += 150
        elif (app.blackTimer < 3000):
            app.blackTimer += 300
    elif (button == 2):
        if (app.blackTimer > 1500):
            app.blackTimer -= 300
        elif (app.blackTimer > 600):
            app.blackTimer -= 150
        elif (app.blackTimer > 180):
            app.blackTimer -= 60
        elif (app.blackTimer > 30):
            app.blackTimer -= 30
        elif (app.blackTimer > 10):
            app.blackTimer -= 2
        elif (app.blackTimer > 1):
            app.blackTimer -= 1
    app.blackTimerText.value = str(datetime.timedelta(seconds=app.blackTimer)).rsplit(':', 2)[1] + ':' + str(datetime.timedelta(seconds=app.blackTimer)).rsplit(':', 2)[2]
        
        

def onKeyPress(keys):
    if ('s' in keys):
        ChangeTurn()
        
def onMousePress(msX, msY, button):
    if (not app.gameHasStarted and app.botButton.contains(msX, msY)):
        OnBotButtonPress()
        return
    elif (not app.gameHasStarted and app.playerButton.contains(msX, msY)):
        OnPlayerButtonPress()
        return
    
    
    
    if (not board.playingBot or (board.playingBot and app.turnColor == Color.WHITE)):
        for square in board:
            if square.contains(msX, msY):
                if (board.selectedSquare != None and board.selectedSquare != square and board.selectedSquare.properties.color != square.properties.color):
                    move = Move(square, board.selectedSquare)
                    if (MoveIsLegal(move)): MovePiece(move)
                    return
                else:
                    SelectPiece(square)
                    return
            
    if (app.whiteTimerButton.contains(msX, msY)):
        OnWhiteTimerPress(button)
    elif (app.blackTimerButton.contains(msX, msY)):
        OnBlackTimerPress(button)
    
    Deselect()      
    
def onMouseRelease(msX, msY):
    for square in board:
        if square.contains(msX, msY):
            if (board.selectedSquare != None and board.selectedSquare != square and board.selectedSquare.properties.color != square.properties.color):
                move = Move(square, board.selectedSquare)
                if (MoveIsLegal(move)): MovePiece(move)
                return
           
app.stepsPerSecond = 1            
def onStep():
    if (not app.gameHasStarted): return

    if (board.triggerBotMove):
        BotMove()
        board.triggerBotMove = False

    if (app.turnColor == Color.WHITE):
        app.whiteTimer -= 1
        app.whiteTimerText.value = str(datetime.timedelta(seconds=app.whiteTimer)).rsplit(':', 2)[1] + ':' + str(datetime.timedelta(seconds=app.whiteTimer)).rsplit(':', 2)[2]
    elif (app.turnColor == Color.BLACK):
        app.blackTimer -= 1
        app.blackTimerText.value = str(datetime.timedelta(seconds=app.blackTimer)).rsplit(':', 2)[1] + ':' + str(datetime.timedelta(seconds=app.blackTimer)).rsplit(':', 2)[2]
        
    if (app.whiteTimer <= 0):
        print("yo white lost")
        GameOver(Color.BLACK, Condition.TIME)
    if (app.blackTimer <= 0):
        GameOver(Color.WHITE, Condition.TIME)
        
        
        
        
