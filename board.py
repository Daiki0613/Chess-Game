import piece
import positions

#representation of the chess board
#make the board represented as a list of 64 elements

class Board:
    """
    Board creates the chess game and stores the state of the board
    Put description of the Board class here
    
    First digit: used to distinguish black and white
    1: white
    2: black

    Second digit: used to determine piece type
    1: Pawn
    2: Knight
    3: Bishop
    4: Rook
    5: Queen
    6: King

    For example, 11 is black pawn

    """
    def __init__(self, position = "pos1"):
        if position == "pos1": self.board = positions.init_pos()
        elif position == "pos2": self.board = positions.position2()
        elif position == "pos3": self.board = positions.position3()
        elif position == "pos4": self.board = positions.position4()
        else: raise "ERROR"

    def print_board(self):
        list = self.tolist()
        print("   a  b  c  d  e  f  g  h")
        print("  _______________________")
        for i in range(8):
            print(8 - i, end = "| ")
            for j in range(8):
                print(list[8 * i + j], end = "  ")
            print()
    
    def tolist(self):
        list = []
        for i in range(64):
            if self.board[i] == None: list.append(0)
            else: list.append(self.board[i].name)
        return list

    def move(self, spos, epos, move_type, turn):
        if move_type == None: #normal movement
            if self.board[spos].name.upper() == "P" and abs(spos - epos) == 16: #used for en passant
                move_type = "pawn"
            self.board[spos].move(epos) #change coordinates of piece moved
            end_pos_piece = self.board[epos] #storing piece taken
            self.board[epos] = self.board[spos] #move piece to new location
            self.board[spos] = None #empty original location
            return [move_type, [spos, epos, end_pos_piece]]

        elif move_type == "ep": #en passant
            self.board[spos].move(epos) #change coordinates of piece moved
            if turn: pawn_pos = epos + 8 #white, coordinates of pawn taken
            else: pawn_pos = epos - 8 #black
            pawn_taken = self.board[pawn_pos] #storing pawn taken
            self.board[pawn_pos] = None
            self.board[epos] = self.board[spos] #move piece to new location
            self.board[spos] = None
            return ["ep", [spos, epos, pawn_pos, pawn_taken]]

        elif move_type == "C": #castle
            if epos == 2: list = [4, 2, 0, 3]
            elif epos == 6: list = [4, 6, 7, 5]
            elif epos == 58: list = [60, 58, 56, 59]
            elif epos == 62: list = [60, 62, 63, 61]
            else: raise "ERROR"
            self.board[list[0]].move(list[1])
            self.board[list[2]].move(list[3])
            self.board[list[1]], self.board[list[0]] = self.board[list[0]], None
            self.board[list[3]], self.board[list[2]] = self.board[list[2]], None
            return ["c", list]

        elif move_type in ["Q", "N", "R", "B"]: #promotion
            piece_taken = self.board[epos] #store piece taken
            piece_moved = self.board[spos] #store original pawn
            self.board[spos] = None
            if move_type == "Q": #creating new piece
                self.board[epos] = piece.Queen(turn, epos)
            if move_type == "N":
                self.board[epos] = piece.Knight(turn, epos)
            if move_type == "R":
                self.board[epos] = piece.Rook(turn, epos)
            if move_type == "B":
                self.board[epos] = piece.Bishop(turn, epos)
            return ["p", [spos, epos, piece_moved, piece_taken]]
        else: 
            raise "ERROR"

    def undo(self, previous_move):
        if previous_move[0] == "p":
            promoted_piece = self.board[previous_move[1][1]]
            self.board[previous_move[1][1]] = previous_move[1][3] #place back piece which was in end_pos
            self.board[previous_move[1][0]] = previous_move[1][2] #place back piece which was in start_pos
            del promoted_piece
        elif previous_move[0] == "ep":
            self.board[previous_move[1][1]].undo(previous_move[1][0]) #change moved piece coordinates to initial coord
            self.board[previous_move[1][0]] = self.board[previous_move[1][1]] #move end_pos back to start_pos
            self.board[previous_move[1][1]] = None
            self.board[previous_move[1][2]] = previous_move[1][3] #put taken piece back
        elif previous_move[0] == "c":
            self.board[previous_move[1][1]].undo(previous_move[1][0])
            self.board[previous_move[1][3]].undo(previous_move[1][2])
            self.board[previous_move[1][0]], self.board[previous_move[1][1]] = self.board[previous_move[1][1]], None
            self.board[previous_move[1][2]], self.board[previous_move[1][3]] = self.board[previous_move[1][3]], None
        else:
            self.board[previous_move[1][1]].undo(previous_move[1][0]) #change moved piece coordinates to initial coord
            self.board[previous_move[1][0]] = self.board[previous_move[1][1]] #move end_pos back to start_pos
            self.board[previous_move[1][1]] = previous_move[1][2] #put taken piece back