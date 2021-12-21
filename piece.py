#representation of the chess pieces and the possible moves

def direction(pos, board, color): #iterates through a list of move destinations in one direction and see if its valid
    list = []
    for x in pos:
        if board[x] == None:
            list.append(x)
            continue
        elif board[x].color != color:
            list.append(x)
            break
        else:
            break
    return list

def _threat_direction(board, pos_list, king_pos): #given a set of positions in one direction, returns threat map and determines whether king is threatened
    tpos = set() #stores a set of values that the piece threatens (iterates through pos_list until it hits a piece (non-opp-king))
    tpos_bool = True #when this turns false, no more adding to tpos
    tking = False #when true, the piece threats king
    counter = 0 #when 3 or more pieces are between the piece and king, that piece is not threatening king, so tking stays false
    for x in pos_list:
        if x == king_pos:
            if tpos_bool: tpos.add(x)
            if counter <= 2: tking = True
        elif board[x] != None:
            counter += 1
            if tpos_bool:
                tpos.add(x)
                tpos_bool = False
        elif board[x] == None:
            if tpos_bool: tpos.add(x)
        else: raise "ERROR"
    return tpos, tking

def gen_diagonal(pos):
    a, b = pos % 8, pos // 8
    return [[pos - (i + 1) * 9 for i in range(min(a, b))],
    [pos - (i + 1) * 7 for i in range(min(7 - a, b))],
    [pos + (i + 1) * 7 for i in range(7 - max(7 - a, b))],
    [pos + (i + 1) * 9 for i in range(7 - max(a, b))]]

def gen_orthogonal(pos):
    a , b = pos % 8, pos // 8
    return [[pos - (i + 1) * 8 for i in range(b)],
    [pos - (i + 1) for i in range(a)],
    [pos + (i + 1) for i in range(7 - a)],
    [pos + (i + 1) * 8 for i in range(7 - b)]]

class Piece:
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.name = None #default, set in child class
    
    def move(self, new_pos): #changes position of pawn
        self.pos = new_pos
    
    def undo(self, new_pos): #changes position of pawn
        self.pos = new_pos

class Pawn(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        if color: self.name = "P"
        else: self.name = "p"
        self.not_moved = True
    
    def threats(self, board, king_pos):
        list, bool = set(), False
        if self.color: #white
            if self.pos % 8 != 0: 
                list.add(self.pos-9)
                if self.pos - 9 == king_pos:
                    bool = True
            if self.pos % 8 != 7: 
                list.add(self.pos-7)
                if self.pos - 7 == king_pos:
                    bool = True
        if not self.color: #Black
            if self.pos % 8 != 0:
                list.add(self.pos + 7)
                if self.pos + 7 == king_pos:
                    bool = True
            if self.pos % 8 != 7:
                list.add(self.pos + 9)
                if self.pos + 9 == king_pos:
                    bool = True
        return list, bool

    def possible_moves(self, board):
        x = self.pos
        list = []
        if self.color: #white
            if board[x-8] == None: #forward
                list.append(x-8)
                if self.pos // 8 == 6 and board[x-16] == None: list.append(x-16)
            if x % 8 != 0 and board[x-9] != None and not board[x-9].color: #take diagonal left
                list.append(x-9)
            if x % 8 != 7 and board[x-7] != None and not board[x-7].color: #take diagonal right
                list.append(x-7)
                
        else: #black
            if board[x+8] == None:
                list.append(x+8)
                if self.pos // 8 == 1 and board[x+16] == None: list.append(x+16)
            if x % 8 != 0 and board[x+7] != None and board[x+7].color: #take diagonal left
                list.append(x+7)
            if x % 8 != 7 and board[x+9] != None and board[x+9].color: #take diagonal right
                list.append(x+9)
        return list

class Knight(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        if color: self.name = "N"
        else: self.name = "n"
        self.not_moved = False
    
    def threats(self, board, king_pos):
        list, bool = set(), False
        a, b = self.pos % 8, self.pos // 8
        positions = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]
        for x in positions:
            if 0 <= a + x[0] < 8 and 0 <= b + x[1] < 8:
                new_pos = self.pos + x[0] + x[1] * 8
                list.add(new_pos)
        if king_pos in list:
            bool = True
        return list, bool

    def possible_moves(self, board):
        list1, list2 = [], []
        a, b = self.pos % 8, self.pos // 8
        positions = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]
        for x in positions:
            if 0 <= a + x[0] < 8 and 0 <= b + x[1] < 8:
                list1.append(self.pos + x[0] + x[1] * 8)
        for x in list1:
            if board[x] == None or board[x].color != self.color:
                list2.append(x)
        return list2
    
class Bishop(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        if color: self.name = "B"
        else: self.name = "b"
        self.not_moved = False

    def threats(self, board, king_pos):
        threat_pos, threat_king = set(), False
        for x in gen_diagonal(self.pos):
            tpos, tking = _threat_direction(board, x, king_pos)
            threat_pos.update(tpos)
            threat_king = threat_king or tking
        return threat_pos, threat_king

    def possible_moves(self, board):
        list = []
        x = gen_diagonal(self.pos)
        for i in x:
            list.extend(direction(i, board, self.color))
        return list

class Rook(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        if color: self.name = "R"
        else: self.name = "r"
        self.not_moved = True
        self.move_count = 0
    
    def move(self, new_pos): #changes position of rook
        self.pos = new_pos
        self.not_moved = False
        self.move_count += 1
    
    def undo(self, new_pos): #changes position of rook
        self.pos = new_pos
        self.move_count -= 1
        if self.move_count == 0:
            self.not_moved = True

    def threats(self, board, king_pos):
        threat_pos, threat_king = set(), False
        for x in gen_orthogonal(self.pos):
            tpos, tking = _threat_direction(board, x, king_pos)
            threat_pos.update(tpos)
            threat_king = threat_king or tking
        return threat_pos, threat_king

    def possible_moves(self, board):
        list = []
        x = gen_orthogonal(self.pos)
        for i in x:
            list.extend(direction(i, board, self.color))
        return list

class Queen(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        if color: self.name = "Q"
        else: self.name = "q"
        self.not_moved = False
    
    def threats(self, board, king_pos):
        threat_pos, threat_king = set(), False
        for x in gen_diagonal(self.pos) + gen_orthogonal(self.pos):
            tpos, tking = _threat_direction(board, x, king_pos)
            threat_pos.update(tpos)
            threat_king = threat_king or tking
        return threat_pos, threat_king

    def possible_moves(self, board):
        list = []
        x = gen_orthogonal(self.pos) + gen_diagonal(self.pos)
        for i in x:
            list.extend(direction(i, board, self.color))
        return list

class King(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        if color: self.name = "K"
        else: self.name = "k"
        self.not_moved = True
        self.move_count = 0
    
    def move(self, new_pos): #changes position of king
        self.pos = new_pos
        self.move_count += 1
        self.not_moved = False
    
    def threats(self, board, king_pos):
        list, bool = set(), False
        a, b = self.pos % 8, self.pos // 8
        positions = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        for x in positions:
            if 0 <= a + x[0] < 8 and 0 <= b + x[1] < 8:
                new_pos = self.pos + x[0] + x[1] * 8
                list.add(new_pos)
        if king_pos in list:
            bool = True
        return list, bool

    def undo(self, new_pos): #changes position of pawn
        self.pos = new_pos
        self.move_count -= 1
        if self.move_count == 0:
            self.not_moved = True

    def possible_moves(self, board): #generate list of locations that king could move (without considering checks)
        list1, list2= [], []
        a, b = self.pos % 8, self.pos // 8
        positions = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        for x in positions:
            if 0 <= a + x[0] < 8 and 0 <= b + x[1] < 8:
                list1.append(self.pos + x[0] + x[1] * 8)
        #for x in self.move_locations():
        for x in list1:
            if board[x] == None or board[x].color != self.color:
                list2.append(x)
        return list2

    def detect_check(self, board, opp_pieces_pos):
        bool = False
        for x in opp_pieces_pos:
            for destination in board[x].possible_moves(board):
                if self.pos == destination:
                    bool = True
                    break
        return bool