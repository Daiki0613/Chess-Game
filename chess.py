import board
import copy

class Chess:
    """
    spos: start position in 0~63 int
    epos: end position
    """

    def __init__(self, position = "pos1"):
        # replace `pass` with the desired attributes and add any 
        # additional parameters to the function
        self.board = board.Board(position)
        self.turn = True #white turn, and flips every turn
        self.threat_map = set()
        self.threat_pieces = []
        self.threats() #gives initial values to threats
        self.game_log = [] #used to undo movement, stores data like [start_pos, end_pos, taken piece type]


    def trans(self, inpos):
        file = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        rank = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
        return file[inpos[0]] + rank[inpos[1]] * 8
    
    def rtrans(self, outpos):
        a, b = outpos % 8, outpos // 8
        file = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        rank = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
        return file[a] + rank[b]
    
    def generate_moves(self):
        moves = self._generate_moves()
        list = []
        for x in moves:
            if x[2] == "C": 
                list.append(x[0])
            else:
                move = x[2] if x[2] != None else ""
                list.append([self.rtrans(x[0]), self.rtrans(x[1]) + move])
        return list

    def move(self, loc):
        if loc == "O-O":
            if self.turn: self._move([60, 62, "C"])
            else: self._move([4, 6, "C"])
        elif loc == "O-O-O":
            if self.turn: self._move([60, 58, "C"])
            else: self._move([4, 2, "C"])
        else:
            spos = self.trans(loc[0])
            epos = self.trans(loc[1][:2])
            if len(loc[1][2:]) != 0:
                move = loc[1][2:]
            else: move = None
            self._move([spos, epos, move])
    
    def _move(self, loc):
        self.game_log.append(self.board.move(loc[0], loc[1], loc[2], self.turn))
        self.turn = not self.turn
        self.threats()
    
    def undo(self):
        self.board.undo(self.game_log.pop())
        self.turn = not self.turn
        self.threats()

    def find_color(self, color):
        return [x.pos for x in self.board.board if x != None and x.color == color]
    
    def find_king(self, color):
        for x in self.board.board:
            if x != None and x.color == color and x.name.upper() == "K":
                return x.pos

    def _generate_moves(self): #gives a list of all possible moves
        pieces = self.find_color(self.turn) #list of pieces player can move on turn
        list = [] #stores all possible moves
        board = self.board.board
        king_pos = self.find_king(self.turn)
        for spos in pieces:
            if spos == king_pos: #king moves
                list.extend(self.castle(king_pos))
                king_moves = [destination for destination in board[spos].possible_moves(board) if destination not in self.threat_map]
                for epos in king_moves:
                    list.append([spos, epos, None])
            else:
                for epos in board[spos].possible_moves(board):
                    if self.valid_move(spos, epos, None, king_pos):
                        if board[spos].name == "P" and epos // 8 == 0 or board[spos].name == "p" and epos //  8 == 7: #if move is promotion, give promotion options
                            list.extend([[spos, epos, "Q"], [spos, epos, "N"], [spos, epos, "R"], [spos, epos, "B"]])
                        else:
                            list.append([spos, epos, None])
                list.extend(self.en_passant(spos, king_pos))
        return list

    def valid_move(self, spos, epos, move, king_loc): #given a set of moves, this simulates the movement and determine whether valid or not
        valid_move = True
        if self.threat_pieces:
            dup_board = copy.deepcopy(self.board) #make a copy of the board to simulate movement to see whether a move is valid
            dup_board.move(spos, epos, move, self.turn)
            for threat_piece_loc in self.threat_pieces:
                for x in dup_board.board[threat_piece_loc].possible_moves(dup_board.board):
                    if x == king_loc:
                        valid_move = False
                        break
            del dup_board
        return valid_move
    
    def en_passant(self, spos, king_pos):
        list = []
        if self.game_log != []:
            log = self.game_log[-1]
            if log[0] == "pawn" and self.board.board[spos].name.upper() == "P":
                if spos % 8 != 0 and spos - 1 == log[1][1] or spos % 8 != 7 and spos + 1 == log[1][1]:
                    epos = (log[1][0] + log[1][1]) // 2
                    if self.valid_move(spos, epos, "ep", king_pos):
                        list.append([spos, epos, "ep"])
        return list

    def castle(self, king_pos):
        list = []
        if self.turn and self.board.board[king_pos].not_moved: #white
            if self.board.board[61] == None and self.board.board[62] == None and self.board.board[63] != None and \
                self.board.board[63].name == "R" and self.board.board[63].not_moved: #King side O-O (right) 
                if 60 not in self.threat_map and 61 not in self.threat_map and 62 not in self.threat_map:
                    list.append(["O-O", 62, "C"])
            if self.board.board[57] == None and self.board.board[58] == None and self.board.board[59] == None and self.board.board[56] != None and \
                self.board.board[56].name == "R" and self.board.board[56].not_moved:  #Queen side O-O-O(left)
                if 58 not in self.threat_map and 59 not in self.threat_map and 60 not in self.threat_map:
                    list.append(["O-O-O", 58, "C"])
        elif self.board.board[king_pos].not_moved: #black
            if self.board.board[5] == None and self.board.board[6] == None and self.board.board[7] != None and \
                self.board.board[7].name == "r" and self.board.board[7].not_moved: #King side O-O (right)
                if 4 not in self.threat_map and 5 not in self.threat_map and 6 not in self.threat_map:
                    list.append(["O-O", 6, "C"])
            if self.board.board[1] == None and self.board.board[2] == None and self.board.board[3] == None and self.board.board[0] != None and \
                self.board.board[0].name == "r" and self.board.board[0].not_moved:  #Queen side O-O-O (left)
                if 2 not in self.threat_map and 3 not in self.threat_map and 4 not in self.threat_map:
                    list.append(["O-O-O", 2, "C"])
        return list

    def threats(self): #list of all locations opponent pieces can move, and opponent piece locations that could be attacking King
        threat_pos, threat_king = set(), []
        king_pos = self.find_king(self.turn)
        for piece_pos in self.find_color(not self.turn):
            temp1, temp2 = self.board.board[piece_pos].threats(self.board.board, king_pos)
            threat_pos.update(temp1)
            if temp2: threat_king.append(piece_pos)
        self.threat_map = threat_pos
        self.threat_pieces = threat_king
    
    def end_game(self): #determine checkmate or stalemate when there is no possible moves left
        if self.board.board[self.find_king(self.turn)].detect_check(self.board.board, self.find_color(not self.turn)): #if in check
            winner = "White" if not self.turn else "Black" #person who made previous move wins
            return "Checkmate " + winner + " wins"
        else: return "Stalemate, Draw"