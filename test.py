import chess
"""
This script counts the total number of possible boards after n moves
According to this website, https://www.chessprogramming.org/Perft_Results
After the first move there are 20 possible positions, and 400 positions after the second.
(depth : positions)
pos1, (init_pos): (0: 1), (1: 20), (2:400), (3: 8902), (4:197281), (5:4865609) yes, (6:119060324)
pos2: (0: 1), (1: 48), (2: 2039), (3: 97862) yes, (4: 4085603), (5: 193690690), (6: 8031647685)
pos3: (0: 1), (1: 14), (2: 191), (3: 2812), (4: 43238) yes, (5: 674624), (6: 11030083), (7: 179633661)
pos4: (0: 1), (1: 6), (2: 264), (3: 9467) yes, (4: 422333), (5: 15833292), (6: 706045033)
"""

n = 3
position = "pos4"
chess = chess.Chess(position)

def perft(chess, n):
    nodes = 0
    valid_moves = chess._generate_moves()
    if n == 1:
        nodes = len(valid_moves)
        return nodes
    else:
        for x in valid_moves:
            chess._move(x)
            nodes += perft(chess, n-1)
            chess.undo()
        return nodes

sum = 0
list = chess._generate_moves()
print(len(list))
for i in range(len(list)):
#for i in [10]:
    print(i+1, end = ": ")
    chess._move(list[i])
    nodes = perft(chess, n-1)
    print(nodes)
    sum += nodes
    chess.undo()
print("total:",sum)
#print(perft(chess, n))
