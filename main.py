import chess

if __name__ == "__main__":
    chess = chess.Chess()
    print("Type 'undo' to undo move, 'O-O' or 'O-O-O' for castle, 'a8:a6' (start_pos:end_pos) for movement")
    print("Add 'ep' for en passant and 'Q', 'B', 'R', 'N' for promotion")

    while True:
        #start = input("From: ")
        chess.board.print_board()
        valid_moves = chess.generate_moves()
        if not valid_moves:
            print(chess.end_game())
            break

        print("possible moves are: " , valid_moves)

        while True:
            print("Its White's Turn, type your move." if chess.turn else "Its Black's Turn, type your move.")
            move = input("Enter move: ")
            if move == "undo":
                chess.undo()
                break
            elif len(move) >= 5:
                loc = [move[:2], move[3:]]
                if move[2] == " " and loc in valid_moves:
                    chess.move(loc)
                    break
