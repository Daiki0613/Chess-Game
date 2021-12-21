import piece

def init_pos():
    board = [None for i in range(64)]
    board[0] = piece.Rook(False, 0)
    board[1] = piece.Knight(False, 1)
    board[2] = piece.Bishop(False, 2)
    board[3] = piece.Queen(False, 3)
    board[4] = piece.King(False, 4)
    board[5] = piece.Bishop(False, 5)
    board[6] = piece.Knight(False, 6)
    board[7] = piece.Rook(False, 7)

    for i in range(8):
        board[8 + i] = piece.Pawn(False, 8 + i)
        board[48 + i] = piece.Pawn(True, 48 + i)

    board[56] = piece.Rook(True, 56)
    board[57] = piece.Knight(True, 57)
    board[58] = piece.Bishop(True, 58)
    board[59] = piece.Queen(True, 59)
    board[60] = piece.King(True, 60)
    board[61] = piece.Bishop(True, 61)
    board[62] = piece.Knight(True, 62)
    board[63] = piece.Rook(True, 63)
    return board

def position2():
    board = [None for i in range(64)]
    board[0] = piece.Rook(False, 0)
    board[17] = piece.Knight(False, 17)
    board[14] = piece.Bishop(False, 14)
    board[12] = piece.Queen(False, 12)
    board[4] = piece.King(False, 4)
    board[16] = piece.Bishop(False, 16)
    board[21] = piece.Knight(False, 21)
    board[7] = piece.Rook(False, 7)

    board[8] = piece.Pawn(False, 8)
    board[10] = piece.Pawn(False, 10)
    board[11] = piece.Pawn(False, 11)
    board[13] = piece.Pawn(False, 13)
    board[20] = piece.Pawn(False, 20)
    board[22] = piece.Pawn(False, 22)
    board[33] = piece.Pawn(False, 33)
    board[47] = piece.Pawn(False, 47)

    board[27] = piece.Pawn(True, 27)
    board[36] = piece.Pawn(True, 36)
    board[48] = piece.Pawn(True, 48)
    board[49] = piece.Pawn(True, 49)
    board[50] = piece.Pawn(True, 50)
    board[53] = piece.Pawn(True, 53)
    board[54] = piece.Pawn(True, 54)
    board[55] = piece.Pawn(True, 55)

    board[56] = piece.Rook(True, 56)
    board[28] = piece.Knight(True, 28)
    board[51] = piece.Bishop(True, 51)
    board[45] = piece.Queen(True, 45)
    board[60] = piece.King(True, 60)
    board[52] = piece.Bishop(True, 52)
    board[42] = piece.Knight(True, 42)
    board[63] = piece.Rook(True, 63)
    return board

def position3():
    board = [None for i in range(64)]
    board[10] = piece.Pawn(False, 10)
    board[19] = piece.Pawn(False, 19)
    board[37] = piece.Pawn(False, 37)
    board[39] = piece.King(False, 39)
    board[31] = piece.Rook(False, 31)

    board[25] = piece.Pawn(True, 25)
    board[52] = piece.Pawn(True, 52)
    board[54] = piece.Pawn(True, 54)
    board[24] = piece.King(True, 24)
    board[33] = piece.Rook(True, 33)
    return board

def position4():
    board = [None for i in range(64)]
    board[0] = piece.Rook(False, 0)
    board[4] = piece.King(False, 4)
    board[7] = piece.Rook(False, 7)
    board[17] = piece.Bishop(False, 17)
    board[21] = piece.Knight(False, 21)
    board[22] = piece.Bishop(False, 22)
    board[24] = piece.Knight(False, 24)
    board[40] = piece.Queen(False, 40)

    board[9] = piece.Pawn(False, 9)
    board[10] = piece.Pawn(False, 10)
    board[11] = piece.Pawn(False, 11)
    board[13] = piece.Pawn(False, 13)
    board[14] = piece.Pawn(False, 14)
    board[15] = piece.Pawn(False, 15)
    board[49] = piece.Pawn(False, 49)

    board[8] = piece.Pawn(True, 8)
    board[25] = piece.Pawn(True, 25)
    board[34] = piece.Pawn(True, 34)
    board[36] = piece.Pawn(True, 36)
    board[48] = piece.Pawn(True, 48)
    board[51] = piece.Pawn(True, 51)
    board[54] = piece.Pawn(True, 54)
    board[55] = piece.Pawn(True, 55)

    board[23] = piece.Knight(True, 23)
    board[32] = piece.Bishop(True, 32)
    board[33] = piece.Bishop(True, 33)
    board[45] = piece.Knight(True, 45)
    board[56] = piece.Rook(True, 56)
    board[59] = piece.Queen(True, 59)
    board[61] = piece.Rook(True, 61)
    board[62] = piece.King(True, 62)
    return board




