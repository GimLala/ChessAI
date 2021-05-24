import random
zobTable = [[[random.randint(1,2**64 - 1) for i in range(12)]for j in range(8)]for k in range(8)]


'''for i in zobTable:
    for j in i:
        for k in j:
            print k,
        print 

'''

def indexing(piece):
    
    
    ''' mapping each piece to a particular number'''
    if (piece=='P'):
        return 0
    if (piece=='N'):
        return 1
    if (piece=='B'):
        return 2
    if (piece=='R'):
        return 3
    if (piece=='Q'):
        return 4
    if (piece=='K'):
        return 5
    if (piece=='p'):
        return 6
    if (piece=='n'):
        return 7
    if (piece=='b'):
        return 8
    if (piece=='r'):
        return 9
    if (piece=='q'):
        return 10
    if (piece=='k'):
        return 11
    else:
        return -1

def computeHash(board):
    h = 0
    for i in range(8):
        for j in range(8):
           # print board[i][j]
            if board[i][j] != '-':
                piece = indexing(board[i][j])
                h ^= zobTable[i][j][piece]
    return h

def main():
    # Upper Case are white pieces
    # Lower Case are black pieces

    # a [8][8] format board
    board = [
        ['-', '-', '-', 'K', '-', '-', '-', '-'],
        ['-', 'R', '-', '-', '-', '-', 'Q', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', 'P', '-', '-', '-', '-', 'p', '-'],
        ['-', '-', '-', '-', '-', 'p', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['p', '-', '-', '-', 'b', '-', '-', 'q'],
        ['-', '-', '-', '-', 'n', '-', '-', 'k']
    ]

    hashValue = computeHash(board)
    print("Current Board is :")
    for i in board:
        for j in i:
            print(j, end=" ")
        print()

    print("\nThe Current hash is : ",hashValue,"\n")

    # an exaple of channge in game state and how it affects the hashes

    # move white Rook to at a new postion in right
    piece = board[1][1]

    board[1][1] = '-'
    hashValue ^= zobTable[1][1][indexing(piece)]

    board[3][1] = piece
    hashValue ^= zobTable[3][1][indexing(piece)]
    print("The new board is :")
    for i in board:
        for j in i:
            print(j, end=" ")
        print()

    print("\nHash after the move is : ", hashValue, "\n")

if __name__ == "__main__":
    main()
