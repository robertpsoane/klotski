''' Klotski solver using recursion
    
    https://www.schoolarchimedes.com/klotski

    I initially tried using recursion and backtracking to solve this problem,
    however I came across a problem - Klotski can run forever so there is no
    natural stopping point.  I tried setting a maximum number of recursions
    after which I would force it to return, however this got very unweildy

    I also discovered problems with accidentally editing the grid as it is only
    in memory once.  For that reason, I implemented deep copy (not sure what
    the difference between deep and shallow copy is, but thats what I did)

    I decided to change approach, and instead of using backtracking, attempt
    to generate all possible permeatations the board can find itself in, using
    a dictionary to store each layer.  At each layer the function finds all
    new positions the board can be in after one further move, and stops when
    it finds a solution (or outputs the solution and continues searching for
    infinitely more solutions.

    I have copied the output of running this program once into a block
    comment at the bottom of this file.  The program takes a few minutes to 
    run, and there is surely some further optimisation which can be done.

    In a bid to optimise the program, each time I generate a board, I find
    a generic form of the board and add it to a list (eg without the numbers 
    of specific pieces).  All boards are checked against that list to ensure
    we aren't carrying forward any duplicate boards.  I am assuming that all
    boards which we have already seen can be reached in a fewer number of move
    - the number of moves used to find that board in the first instance.  If
    we wanted to find all possible solutions this optimisation could be 
    removed, however I'm not sure whether this is necessary.

    #### The Solution ####
    I believe the first solution calculated is optimal.  It is completed in 
    116 steps.  A quick google search says the optimal solution can be 
    found in 81 steps, however that counts moving a piece 2 spaces as one move
    For example, the move below would be counted as 1 move, where this program
    counts it as 2 moves. 

    B1 R1 R1 B3     B1 R1 R1 B3
    B1 R1 R1 B3     B1 R1 R1 B3
    B2 P1 P1 B4  -> B2 P1 P1 B4
    B2 W2 W3 B4     B2 W2 W3 B4
    W1 XX XX W4     XX XX W1 W4

    The solution is output in coordinates, however I could extend the code
    to show the board after each step.

    To solve this problem, I had to use some functions which were not yet 
    covered in the course:
        - I used a dictionary to store all the permeatations of the board 
        the program has found so far.
        - I used a deepcopy to copy the variables in each round
        - I used the .append function to append to lists
    I believe these are all the functions I have used which we haven't yet
    covered

    I based my solution on the following grids, by moving the piece occupying
    the given coordinates, you will get to the solution of the problem.

    Grid:
     0 1 2 3
    _________
    |X X X X| 0
    |X X X X| 1
    |X X X X| 2
    |X X X X| 3
    |X X X X| 4
    --     --


    Starting Grid:
     0  1  2  3
    ____________
    |B1 R1 R1 B3| 0
    |B1 R1 R1 B3| 1
    |B2 P1 P1 B4| 2
    |B2 W2 W3 B4| 3
    |W1 XX XX W4| 4
    ---       ---

@author = R Soane
@date = 27/10/2020

'''

#import sys
#sys.setrecursionlimit(3000)
import copy
import time

klotski_board = [
    ['B1', 'R1', 'R1', 'B3'],
    ['B1', 'R1', 'R1', 'B3'],
    ['B2', 'P1', 'P1', 'B4'],
    ['B2', 'W2', 'W3', 'B4'],
    ['W1', 'XX', 'XX', 'W4']
]
board_init = [
    ['B1', 'R1', 'R1', 'B3'],
    ['B1', 'R1', 'R1', 'B3'],
    ['B2', 'P1', 'P1', 'B4'],
    ['B2', 'W2', 'W3', 'B4'],
    ['W1', 'XX', 'XX', 'W4']
]





#klotski_board = [['B1', 'R1', 'R1', 'B3'], ['B1', 'R1', 'R1', 'XX'], ['B2', 'P1', 'P1', 'XX'], ['B2', 'W2', 'W3', 'B4'], ['W1', 'XX', 'W4', 'B4']]


tiles = ['B1','B2','B3','B4','R1','P1','W1','W2','W3','W4']
singles = ['W1','W2','W3','W4']
vertical = ['B1','B2','B3','B4']
horizontal = ['P1']
big = ['R1'] 


def findValidMoves(board):
    ''' findValidMoves
    Finds a list of all possible moves for a given board configuration, 
    outputs as a string
    '''
    valid_moves = []
    for i in range(5):
        for j in range(4):
            if board[i][j] == 'XX':
                # We are on an empty space
                # We have multiple possible moves:
                # i + 1 up, i - 1 down, j + 1 left, j - 1 right

                # Checking if space to given side exists
                if i + 1 < 5:
                    move = [i+1, j, i, j]
                    if checkMove(board, move):
                        valid_moves = valid_moves + [move]
                if i - 1 > -1:
                    move = [i-1, j, i, j]
                    if checkMove(board, move):
                        valid_moves = valid_moves + [move]
                if j + 1 < 4:
                    move = [i, j+1, i, j]
                    if checkMove(board, move):
                        valid_moves = valid_moves + [move]
                if j - 1 > -1:
                    move = [i, j-1, i, j]
                    if checkMove(board, move):
                        valid_moves = valid_moves + [move]
    return valid_moves

def checkMove(board, move):
    i0, j0 = move[0], move[1]
    i1, j1 = move[2], move[3]
    piece = board[i0][j0]

    try:
        if piece in singles:
            return True
        elif piece in vertical:
            if j0 == j1:
                # Moving up/down
                return True
            elif (board[i0+1][j0] == piece) and (board[i1+1][j1] == 'XX'):
                # moving Right/Left One
                return True
            elif (board[i0-1][j0] == piece) and (board[i1-1][j1] == 'XX'):
                # moving Right/Left One
                return True
        elif piece in horizontal:
            if i0 == i1:
                # Moving Right/Left
                return True
            elif (board[i0][j0+1] == piece) and (board[i1][j1+1] == 'XX'):
                # moving Up/Down One
                return True
            elif (board[i0][j0-1] == piece) and (board[i1][j1-1] == 'XX'):
                # moving Up/Down One
                return True
        elif piece == 'R1':
            if i0 == i1:
                # Moving Horizontally
                if (board[i0+1][j0] == piece) and (board[i1+1][j1] == 'XX'):
                    # moving Right/Left One
                    return True
                elif (board[i0-1][j0] == piece) and (board[i1-1][j1] == 'XX'):
                    # moving Right/Left One
                    return True
            else:
                # Moving Vertically
                if (board[i0][j0+1] == piece) and (board[i1][j1+1] == 'XX'):
                    # moving Up/Down One
                    return True
                elif (board[i0][j0-1] == piece) and (board[i1][j1-1] == 'XX'):
                    # moving Up/Down One
                    return True
        else:
            return False
    except:
        return False

def dispBoard(board):
    for i in range(5):
        for j in range(4):
            print(board[i][j], end = ' ')
        print()

def board2String(board):
    string = ''
    for i in range(5):
        for j in range(4):
            string = string + board[i][j] + ' '
        string += '\n'
    return string

def moveBoard(board, move):
    
    i0, j0 = move[0], move[1]
    i1, j1 = move[2], move[3]
    piece = board[i0][j0]

    if piece in singles:
        board[i0][j0] = 'XX'
        board[i1][j1] = piece
    elif piece in vertical:
        if j0 == j1:
            # Moving up/down
            if i1 > i0:
                # Moving Down
                board[i0-1][j0] = 'XX'
                board[i1][j1] = piece
            else:
                # Moving Up
                #dispBoard(board)
                board[i0+1][j0] = 'XX'
                board[i1][j1] = piece
        else:
            # Moving left/right
            if j1 > j0:
                # Moving Right
                board[i0][j0] = 'XX'
                board[i1][j1] = piece
                if piece == board[i0+1][j0]:
                    board[i0+1][j0] = 'XX'
                    board[i1+1][j1] = piece
                else:
                    board[i0-1][j0] = 'XX'
                    board[i1-1][j1] = piece
            
            ################################################################
            else:
            # Moving Left
                board[i0][j0] = 'XX'
                board[i1][j1] = piece
                if piece == board[i0+1][j0]:
                    board[i0+1][j0] = 'XX'
                    board[i1+1][j1] = piece
                else:
                    board[i0-1][j0] = 'XX'
                    board[i1-1][j1] = piece
    elif piece in horizontal:
        if i0 == i1:
            # Moving left/right
            if j1 > j0:
                # Moving left
                board[i0][j0-1] = 'XX'
                board[i1][j1] = piece
            else:
                # Moving right
                board[i0][j0+1] = 'XX'
                board[i1][j1] = piece
        else:
            # Moving up/down
            if i1 > i0:
                # Moving down
                board[i0][j0] = 'XX'
                board[i1][j1] = piece
                if piece == board[i0][j0+1]:
                    board[i0][j0+1] = 'XX'
                    board[i1][j1+1] = piece
                else:
                    board[i0][j0-1] = 'XX'
                    board[i1][j1-1] = piece
            else:
                # Moving Up
                board[i0][j0] = 'XX'
                board[i1][j1] = piece
                if piece == board[i0][j0+1]:
                    board[i0][j0+1] = 'XX'
                    board[i1][j1+1] = piece
                else:
                    board[i0][j0-1] = 'XX'
                    board[i1][j1-1] = piece
    elif piece == 'R1':
        if i0 == i1:
            # Moving left/right
            if j1 > j0:
                # Moving left
                board[i0][j0-1] = 'XX'
                board[i1][j1] = piece
                if piece == board[i0+1][j0]:
                    board[i0+1][j0-1] = 'XX'
                    board[i1+1][j1] = piece
                else:
                    board[i0-1][j0-1] = 'XX'
                    board[i1-1][j1] = piece
            else:
                # Moving right
                board[i0][j0+1] = 'XX'
                board[i1][j1] = piece
                if piece == board[i0+1][j0]:
                    board[i0+1][j0+1] = 'XX'
                    board[i1+1][j1] = piece
                else:
                    board[i0-1][j0+1] = 'XX'
                    board[i1-1][j1] = piece
        else:
            # Moving up/down
            if i1 > i0:
                # Moving Down
                board[i0-1][j0] = 'XX'
                board[i1][j1] = piece
                if piece == board[i0][j0+1]:
                    board[i0-1][j0+1] = 'XX'
                    board[i1][j1+1] = piece
                else:
                    board[i0-1][j0-1] = 'XX'
                    board[i1][j1-1] = piece
            else:
                # Moving Up
                board[i0-1][j0] = 'XX'
                board[i1][j1] = piece
                if piece == board[i0][j0+1]:
                    board[i0-1][j0+1] = 'XX'
                    board[i1][j1+1] = piece
                else:
                    board[i0-1][j0-1] = 'XX'
                    board[i1][j1-1] = piece
    return board

def move2String(board, move):
    i0, j0 = move[0], move[1]
    i1, j1 = move[2], move[3]
    piece = board[i0][j0]

    if i0 == i1:
        if j1 > j0:
            direction = 'right'
        else:
            direction = 'left'
    else:
        if i1 > i0:
            direction = 'down'
        else:
            direction = 'up'
    
    string = 'Move {}, {}'.format(piece,direction)
    return string

def isSolved(board):
    if (board[4][1] == 'R1') and (board[4][2] == 'R1'):
        return True
    else:
        return False

def printMoves(move_list):
    for move in move_list:
        i0, j0, i1, j1 = move[0], move[1], move[2], move[3]   
        print(f'({i0},{j0}) > ({i1},{j1})')

def printBoards(move_list):
    board = [
        ['B1', 'R1', 'R1', 'B3'],
        ['B1', 'R1', 'R1', 'B3'],
        ['B2', 'P1', 'P1', 'B4'],
        ['B2', 'W2', 'W3', 'B4'],
        ['W1', 'XX', 'XX', 'W4']
    ]
    dispBoard(board)
    k = 1
    for move in move_list:
        print('\nMove {}'.format(k))
        board = moveBoard(board, move)
        dispBoard(board)
        k += 1

def makeGeneral(board):
    replacementBoard = [
        ['X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 'X']
    ]
    for i in range(5):
        for j in range(4):
            replacementBoard[i][j] = board[i][j][0]
    return replacementBoard

def solve(board_dictionary):
    # Extracting relevant variables from dictionary
    layer = board_dictionary['n']
    layer_key = 'n'+str(layer)

    boards = board_dictionary[layer_key]['boards']
    history = board_dictionary[layer_key]['history']

    print('Starting Layer {}, checked {} board layouts'.format(
                                                        layer + 1,
                                                        len(board_dictionary['allboards'])))

    # Setting up variables for next layer
    new_boards = []
    histories = []
    next_layer_key = 'n'+str(layer + 1)

    # For each board, find all moves.
    for index_1 in range(len(boards)):
        board = copy.deepcopy(boards[index_1])
        ith_history = copy.deepcopy(history[index_1])
        
        # Check all potential moves
        potential_moves = findValidMoves(boards[index_1])
        # For each move
        for index_2 in range(len(potential_moves)):
            move = potential_moves[index_2]
            ith_new_board = copy.deepcopy(board)

            new_board = moveBoard(ith_new_board, move)
            new_history = ith_history + [move]

            # Checking uniqueness of board
            if makeGeneral(new_board) in board_dictionary['allboards']:
                pass
            # Check whether board provides a solution, if it does - output the 
            # board
            elif isSolved(new_board):
                print('solved!\n')
                dispBoard(new_board)
                print()
                printBoards(new_history)
                end_time = time.time()
                
                ### Timing Search
                total_time = end_time - start_time
                secs = total_time % 60
                mins = total_time // 60
                hours = mins // 60
                print('Time to solve and output solution: {}:{}:{}'.format(hours, mins, secs))

                input('more?')
            else:
                new_boards.append(new_board)
                histories.append(new_history)
                board_dictionary['allboards'].append(makeGeneral(new_board))

    # Adding layer to dictionary and running next layer
    next_dictionary_layer = {
        'boards': new_boards,
        'history': histories
    }
    board_dictionary[next_layer_key] = next_dictionary_layer
    board_dictionary['n'] += 1
    solve(board_dictionary)

klotski_dict = {
    'n': 0,
    'allboards': [],
    'n0': {
        'boards': [klotski_board],
        'history': [[]]
    }
}

start_time = time.time()

solve(klotski_dict)

end_time = time.time()
total_time = end_time - start_time
secs = total_time % 60
mins = total_time // 60
hours = mins // 60
print('Time to solve and output solution: {}:{}:{}'.format(hours, mins, secs))


'''
Output from running code:

Starting Layer 1, checked 0 board layouts
Starting Layer 2, checked 4 board layouts
Starting Layer 3, checked 15 board layouts
Starting Layer 4, checked 28 board layouts
Starting Layer 5, checked 46 board layouts
Starting Layer 6, checked 63 board layouts
Starting Layer 7, checked 82 board layouts
Starting Layer 8, checked 102 board layouts
Starting Layer 9, checked 124 board layouts
Starting Layer 10, checked 156 board layouts
Starting Layer 11, checked 194 board layouts
Starting Layer 12, checked 236 board layouts
Starting Layer 13, checked 272 board layouts
Starting Layer 14, checked 306 board layouts
Starting Layer 15, checked 350 board layouts
Starting Layer 16, checked 390 board layouts
Starting Layer 17, checked 424 board layouts
Starting Layer 18, checked 454 board layouts
Starting Layer 19, checked 483 board layouts
Starting Layer 20, checked 519 board layouts
Starting Layer 21, checked 566 board layouts
Starting Layer 22, checked 628 board layouts
Starting Layer 23, checked 684 board layouts
Starting Layer 24, checked 732 board layouts
Starting Layer 25, checked 780 board layouts
Starting Layer 26, checked 819 board layouts
Starting Layer 27, checked 854 board layouts
Starting Layer 28, checked 900 board layouts
Starting Layer 29, checked 952 board layouts
Starting Layer 30, checked 1020 board layouts
Starting Layer 31, checked 1096 board layouts
Starting Layer 32, checked 1165 board layouts
Starting Layer 33, checked 1216 board layouts
Starting Layer 34, checked 1266 board layouts
Starting Layer 35, checked 1331 board layouts
Starting Layer 36, checked 1408 board layouts
Starting Layer 37, checked 1509 board layouts
Starting Layer 38, checked 1641 board layouts
Starting Layer 39, checked 1786 board layouts
Starting Layer 40, checked 1960 board layouts
Starting Layer 41, checked 2163 board layouts
Starting Layer 42, checked 2403 board layouts
Starting Layer 43, checked 2687 board layouts
Starting Layer 44, checked 3029 board layouts
Starting Layer 45, checked 3409 board layouts
Starting Layer 46, checked 3809 board layouts
Starting Layer 47, checked 4241 board layouts
Starting Layer 48, checked 4659 board layouts
Starting Layer 49, checked 5067 board layouts
Starting Layer 50, checked 5513 board layouts
Starting Layer 51, checked 5991 board layouts
Starting Layer 52, checked 6529 board layouts
Starting Layer 53, checked 7105 board layouts
Starting Layer 54, checked 7681 board layouts
Starting Layer 55, checked 8297 board layouts
Starting Layer 56, checked 8991 board layouts
Starting Layer 57, checked 9739 board layouts
Starting Layer 58, checked 10499 board layouts
Starting Layer 59, checked 11231 board layouts
Starting Layer 60, checked 11943 board layouts
Starting Layer 61, checked 12599 board layouts
Starting Layer 62, checked 13147 board layouts
Starting Layer 63, checked 13657 board layouts
Starting Layer 64, checked 14155 board layouts
Starting Layer 65, checked 14639 board layouts
Starting Layer 66, checked 15127 board layouts
Starting Layer 67, checked 15547 board layouts
Starting Layer 68, checked 15869 board layouts
Starting Layer 69, checked 16171 board layouts
Starting Layer 70, checked 16451 board layouts
Starting Layer 71, checked 16691 board layouts
Starting Layer 72, checked 16893 board layouts
Starting Layer 73, checked 17067 board layouts
Starting Layer 74, checked 17225 board layouts
Starting Layer 75, checked 17355 board layouts
Starting Layer 76, checked 17451 board layouts
Starting Layer 77, checked 17525 board layouts
Starting Layer 78, checked 17585 board layouts
Starting Layer 79, checked 17633 board layouts
Starting Layer 80, checked 17679 board layouts
Starting Layer 81, checked 17729 board layouts
Starting Layer 82, checked 17773 board layouts
Starting Layer 83, checked 17831 board layouts
Starting Layer 84, checked 17901 board layouts
Starting Layer 85, checked 17987 board layouts
Starting Layer 86, checked 18089 board layouts
Starting Layer 87, checked 18195 board layouts
Starting Layer 88, checked 18299 board layouts
Starting Layer 89, checked 18419 board layouts
Starting Layer 90, checked 18553 board layouts
Starting Layer 91, checked 18705 board layouts
Starting Layer 92, checked 18883 board layouts
Starting Layer 93, checked 19075 board layouts
Starting Layer 94, checked 19291 board layouts
Starting Layer 95, checked 19521 board layouts
Starting Layer 96, checked 19775 board layouts
Starting Layer 97, checked 20025 board layouts
Starting Layer 98, checked 20297 board layouts
Starting Layer 99, checked 20593 board layouts
Starting Layer 100, checked 20889 board layouts
Starting Layer 101, checked 21197 board layouts
Starting Layer 102, checked 21481 board layouts
Starting Layer 103, checked 21711 board layouts
Starting Layer 104, checked 21897 board layouts
Starting Layer 105, checked 22057 board layouts
Starting Layer 106, checked 22198 board layouts
Starting Layer 107, checked 22320 board layouts
Starting Layer 108, checked 22444 board layouts
Starting Layer 109, checked 22556 board layouts
Starting Layer 110, checked 22666 board layouts
Starting Layer 111, checked 22776 board layouts
Starting Layer 112, checked 22862 board layouts
Starting Layer 113, checked 22930 board layouts
Starting Layer 114, checked 22984 board layouts
Starting Layer 115, checked 23044 board layouts
Starting Layer 116, checked 23118 board layouts
solved!

B4 B2 B3 B1
B4 B2 B3 B1
W4 W2 P1 P1
XX R1 R1 W1
XX R1 R1 W3

B1 R1 R1 B3
B1 R1 R1 B3
B2 P1 P1 B4
B2 W2 W3 B4
W1 XX XX W4

Move 1
B1 R1 R1 B3
B1 R1 R1 B3
B2 P1 P1 B4
B2 W2 W3 B4
XX W1 XX W4

Move 2
B1 R1 R1 B3
B1 R1 R1 B3
XX P1 P1 B4
B2 W2 W3 B4
B2 W1 XX W4 

Move 3
B1 R1 R1 B3
B1 R1 R1 B3
P1 P1 XX B4
B2 W2 W3 B4
B2 W1 XX W4

Move 4
B1 R1 R1 B3
B1 R1 R1 B3
P1 P1 W3 B4
B2 W2 XX B4
B2 W1 XX W4

Move 5
B1 R1 R1 B3
B1 R1 R1 B3
P1 P1 W3 B4
B2 W2 XX B4
B2 W1 W4 XX

Move 6
B1 R1 R1 B3
B1 R1 R1 B3
P1 P1 W3 XX
B2 W2 XX B4
B2 W1 W4 B4

Move 7
B1 R1 R1 B3
B1 R1 R1 B3
P1 P1 XX W3
B2 W2 XX B4
B2 W1 W4 B4

Move 8
B1 R1 R1 B3
B1 R1 R1 B3 
XX P1 P1 W3
B2 W2 XX B4
B2 W1 W4 B4

Move 9
B1 R1 R1 B3
B1 R1 R1 B3
B2 P1 P1 W3
B2 W2 XX B4
XX W1 W4 B4

Move 10
B1 R1 R1 B3
B1 R1 R1 B3
B2 P1 P1 W3
B2 W2 XX B4
W1 XX W4 B4

Move 11
B1 R1 R1 B3
B1 R1 R1 B3
B2 P1 P1 W3
B2 W2 XX B4
W1 W4 XX B4

Move 12
B1 R1 R1 B3
B1 R1 R1 B3
B2 P1 P1 W3
B2 W2 B4 XX
W1 W4 B4 XX

Move 13
B1 R1 R1 B3
B1 R1 R1 B3
B2 P1 P1 XX
B2 W2 B4 W3
W1 W4 B4 XX 

Move 14
B1 R1 R1 B3
B1 R1 R1 B3
B2 XX P1 P1
B2 W2 B4 W3
W1 W4 B4 XX

Move 15
B1 R1 R1 B3
B1 R1 R1 B3
B2 W2 P1 P1
B2 XX B4 W3
W1 W4 B4 XX

Move 16
B1 R1 R1 B3
B1 R1 R1 B3 
B2 W2 P1 P1
B2 W4 B4 W3
W1 XX B4 XX

Move 17
B1 R1 R1 B3
B1 R1 R1 B3
B2 W2 P1 P1
B2 W4 B4 W3
XX W1 B4 XX

Move 18
B1 R1 R1 B3
B1 R1 R1 B3
XX W2 P1 P1
B2 W4 B4 W3
B2 W1 B4 XX

Move 19
B1 R1 R1 B3
B1 R1 R1 B3
W2 XX P1 P1
B2 W4 B4 W3
B2 W1 B4 XX

Move 20
B1 R1 R1 B3
B1 R1 R1 B3
W2 P1 P1 XX
B2 W4 B4 W3
B2 W1 B4 XX

Move 21
B1 R1 R1 XX
B1 R1 R1 B3
W2 P1 P1 B3
B2 W4 B4 W3 
B2 W1 B4 XX

Move 22
B1 R1 R1 XX
B1 R1 R1 B3
W2 P1 P1 B3
B2 W4 B4 XX
B2 W1 B4 W3

Move 23
B1 R1 R1 XX
B1 R1 R1 XX
W2 P1 P1 B3
B2 W4 B4 B3
B2 W1 B4 W3

Move 24
B1 XX R1 R1 
B1 XX R1 R1
W2 P1 P1 B3
B2 W4 B4 B3
B2 W1 B4 W3

Move 25
XX B1 R1 R1
XX B1 R1 R1
W2 P1 P1 B3
B2 W4 B4 B3
B2 W1 B4 W3

Move 26
XX B1 R1 R1
W2 B1 R1 R1
XX P1 P1 B3
B2 W4 B4 B3
B2 W1 B4 W3

Move 27
W2 B1 R1 R1
XX B1 R1 R1
XX P1 P1 B3
B2 W4 B4 B3
B2 W1 B4 W3

Move 28
W2 B1 R1 R1
XX B1 R1 R1
B2 P1 P1 B3
B2 W4 B4 B3
XX W1 B4 W3

Move 29
W2 B1 R1 R1
B2 B1 R1 R1
B2 P1 P1 B3
XX W4 B4 B3
XX W1 B4 W3

Move 30
W2 B1 R1 R1 
B2 B1 R1 R1
B2 P1 P1 B3
W4 XX B4 B3
XX W1 B4 W3

Move 31
W2 B1 R1 R1
B2 B1 R1 R1
B2 P1 P1 B3
W4 XX B4 B3
W1 XX B4 W3

Move 32
W2 B1 R1 R1
B2 B1 R1 R1
B2 P1 P1 B3
W4 B4 XX B3
W1 B4 XX W3

Move 33
W2 B1 R1 R1
B2 B1 R1 R1
B2 P1 P1 B3
W4 B4 XX B3
W1 B4 W3 XX

Move 34
W2 B1 R1 R1
B2 B1 R1 R1
B2 P1 P1 B3
W4 B4 W3 B3
W1 B4 XX XX

Move 35
W2 B1 R1 R1
B2 B1 R1 R1
B2 P1 P1 XX
W4 B4 W3 B3
W1 B4 XX B3

Move 36
W2 B1 R1 R1
B2 B1 R1 R1
B2 XX P1 P1
W4 B4 W3 B3
W1 B4 XX B3

Move 37
W2 B1 R1 R1
B2 B1 R1 R1
B2 B4 P1 P1
W4 B4 W3 B3
W1 XX XX B3

Move 38
W2 B1 R1 R1
B2 B1 R1 R1
B2 B4 P1 P1
W4 B4 W3 B3 
XX W1 XX B3

Move 39
W2 B1 R1 R1
B2 B1 R1 R1
B2 B4 P1 P1
W4 B4 W3 B3
XX XX W1 B3

Move 40
W2 B1 R1 R1
B2 B1 R1 R1
B2 XX P1 P1
W4 B4 W3 B3
XX B4 W1 B3

Move 41
W2 XX R1 R1
B2 B1 R1 R1
B2 B1 P1 P1
W4 B4 W3 B3
XX B4 W1 B3

Move 42
XX W2 R1 R1
B2 B1 R1 R1
B2 B1 P1 P1
W4 B4 W3 B3
XX B4 W1 B3

Move 43
B2 W2 R1 R1
B2 B1 R1 R1
XX B1 P1 P1
W4 B4 W3 B3
XX B4 W1 B3

Move 44
B2 W2 R1 R1 
B2 B1 R1 R1
W4 B1 P1 P1
XX B4 W3 B3
XX B4 W1 B3

Move 45
B2 W2 R1 R1
B2 B1 R1 R1
W4 B1 P1 P1
B4 XX W3 B3
B4 XX W1 B3

Move 46
B2 W2 R1 R1
B2 XX R1 R1
W4 B1 P1 P1
B4 B1 W3 B3
B4 XX W1 B3

Move 47
B2 W2 R1 R1
B2 XX R1 R1 
W4 XX P1 P1
B4 B1 W3 B3
B4 B1 W1 B3

Move 48
B2 W2 R1 R1
B2 XX R1 R1
XX W4 P1 P1
B4 B1 W3 B3
B4 B1 W1 B3

Move 49
B2 W2 R1 R1
B2 W4 R1 R1
XX XX P1 P1
B4 B1 W3 B3
B4 B1 W1 B3

Move 50
B2 W2 R1 R1
B2 W4 R1 R1
XX P1 P1 XX
B4 B1 W3 B3
B4 B1 W1 B3

Move 51
B2 W2 R1 R1
B2 W4 R1 R1
P1 P1 XX XX
B4 B1 W3 B3
B4 B1 W1 B3

Move 52
B2 W2 R1 R1
B2 W4 R1 R1
P1 P1 XX B3
B4 B1 W3 B3
B4 B1 W1 XX

Move 53
B2 W2 R1 R1
B2 W4 R1 R1
P1 P1 XX B3
B4 B1 W3 B3
B4 B1 XX W1

Move 54
B2 W2 R1 R1
B2 W4 R1 R1
P1 P1 XX B3
B4 B1 XX B3
B4 B1 W3 W1

Move 55
B2 W2 R1 R1
B2 W4 R1 R1
P1 P1 B3 XX
B4 B1 B3 XX
B4 B1 W3 W1

Move 56
B2 W2 R1 R1
B2 W4 R1 R1
P1 P1 B3 XX
B4 B1 B3 W1
B4 B1 W3 XX

Move 57
B2 W2 R1 R1
B2 W4 R1 R1
P1 P1 B3 XX
B4 B1 B3 W1
B4 B1 XX W3

Move 58
B2 W2 R1 R1
B2 W4 R1 R1
P1 P1 XX XX
B4 B1 B3 W1
B4 B1 B3 W3

Move 59
B2 W2 R1 R1
B2 W4 R1 R1
XX P1 P1 XX
B4 B1 B3 W1
B4 B1 B3 W3

Move 60
XX W2 R1 R1
B2 W4 R1 R1
B2 P1 P1 XX
B4 B1 B3 W1
B4 B1 B3 W3

Move 61
W2 XX R1 R1
B2 W4 R1 R1
B2 P1 P1 XX
B4 B1 B3 W1
B4 B1 B3 W3

Move 62
W2 W4 R1 R1
B2 XX R1 R1
B2 P1 P1 XX
B4 B1 B3 W1
B4 B1 B3 W3

Move 63
W2 W4 R1 R1
B2 XX R1 R1
B2 XX P1 P1
B4 B1 B3 W1
B4 B1 B3 W3 

Move 64
W2 W4 R1 R1
B2 XX R1 R1
B2 B1 P1 P1
B4 B1 B3 W1
B4 XX B3 W3

Move 65
W2 W4 R1 R1
B2 B1 R1 R1
B2 B1 P1 P1 
B4 XX B3 W1
B4 XX B3 W3

Move 66
W2 W4 R1 R1
B2 B1 R1 R1
B2 B1 P1 P1
B4 B3 XX W1
B4 B3 XX W3

Move 67
W2 W4 R1 R1
B2 B1 R1 R1
B2 B1 P1 P1
B4 B3 W1 XX
B4 B3 XX W3

Move 68
W2 W4 R1 R1
B2 B1 R1 R1
B2 B1 P1 P1
B4 B3 XX XX
B4 B3 W1 W3

Move 69
W2 W4 R1 R1
B2 B1 R1 R1
B2 B1 XX XX
B4 B3 P1 P1
B4 B3 W1 W3

Move 70
W2 W4 XX XX
B2 B1 R1 R1 
B2 B1 R1 R1
B4 B3 P1 P1
B4 B3 W1 W3

Move 71
W2 XX W4 XX
B2 B1 R1 R1
B2 B1 R1 R1
B4 B3 P1 P1
B4 B3 W1 W3

Move 72
XX W2 W4 XX
B2 B1 R1 R1
B2 B1 R1 R1
B4 B3 P1 P1
B4 B3 W1 W3

Move 73
B2 W2 W4 XX
B2 B1 R1 R1
XX B1 R1 R1
B4 B3 P1 P1
B4 B3 W1 W3

Move 74
B2 W2 XX W4
B2 B1 R1 R1
XX B1 R1 R1
B4 B3 P1 P1
B4 B3 W1 W3

Move 75
B2 XX W2 W4
B2 B1 R1 R1
XX B1 R1 R1
B4 B3 P1 P1
B4 B3 W1 W3

Move 76
B2 B1 W2 W4
B2 B1 R1 R1 
XX XX R1 R1
B4 B3 P1 P1
B4 B3 W1 W3

Move 77
B2 B1 W2 W4
B2 B1 R1 R1
B4 XX R1 R1
B4 B3 P1 P1
XX B3 W1 W3

Move 78
B2 B1 W2 W4
B2 B1 R1 R1
B4 B3 R1 R1
B4 B3 P1 P1
XX XX W1 W3

Move 79
B2 B1 W2 W4
B2 B1 R1 R1
B4 B3 R1 R1 
B4 B3 P1 P1
XX W1 XX W3

Move 80
B2 B1 W2 W4
B2 B1 R1 R1
B4 B3 R1 R1
B4 B3 P1 P1
W1 XX XX W3

Move 81
B2 B1 W2 W4
B2 B1 R1 R1
B4 B3 R1 R1
B4 B3 P1 P1
W1 XX W3 XX

Move 82
B2 B1 W2 W4
B2 B1 R1 R1
B4 B3 R1 R1
B4 B3 P1 P1
W1 W3 XX XX

Move 83
B2 B1 W2 W4
B2 B1 R1 R1
B4 B3 R1 R1
B4 B3 XX XX
W1 W3 P1 P1

Move 84
B2 B1 W2 W4
B2 B1 XX XX
B4 B3 R1 R1
B4 B3 R1 R1
W1 W3 P1 P1

Move 85
B2 B1 XX W4
B2 B1 W2 XX
B4 B3 R1 R1
B4 B3 R1 R1
W1 W3 P1 P1

Move 86
B2 B1 XX W4
B2 B1 XX W2
B4 B3 R1 R1
B4 B3 R1 R1
W1 W3 P1 P1

Move 87
B2 XX B1 W4
B2 XX B1 W2
B4 B3 R1 R1
B4 B3 R1 R1
W1 W3 P1 P1

Move 88
B2 XX B1 W4
B2 B3 B1 W2
B4 B3 R1 R1
B4 XX R1 R1
W1 W3 P1 P1

Move 89
B2 B3 B1 W4
B2 B3 B1 W2
B4 XX R1 R1 
B4 XX R1 R1
W1 W3 P1 P1

Move 90
B2 B3 B1 W4
B2 B3 B1 W2
B4 R1 R1 XX
B4 R1 R1 XX
W1 W3 P1 P1

Move 91
B2 B3 B1 W4
B2 B3 B1 XX
B4 R1 R1 W2
B4 R1 R1 XX
W1 W3 P1 P1

Move 92
B2 B3 B1 XX
B2 B3 B1 W4
B4 R1 R1 W2
B4 R1 R1 XX
W1 W3 P1 P1

Move 93
B2 B3 B1 XX
B2 B3 B1 W4
B4 R1 R1 XX
B4 R1 R1 W2
W1 W3 P1 P1

Move 94
B2 B3 B1 XX
B2 B3 B1 XX
B4 R1 R1 W4
B4 R1 R1 W2
W1 W3 P1 P1

Move 95
B2 B3 XX B1
B2 B3 XX B1
B4 R1 R1 W4
B4 R1 R1 W2
W1 W3 P1 P1

Move 96
B2 XX B3 B1
B2 XX B3 B1 
B4 R1 R1 W4
B4 R1 R1 W2
W1 W3 P1 P1

Move 97
XX B2 B3 B1
XX B2 B3 B1
B4 R1 R1 W4
B4 R1 R1 W2
W1 W3 P1 P1

Move 98
XX B2 B3 B1
B4 B2 B3 B1
B4 R1 R1 W4
XX R1 R1 W2
W1 W3 P1 P1

Move 99
B4 B2 B3 B1
B4 B2 B3 B1
XX R1 R1 W4
XX R1 R1 W2
W1 W3 P1 P1

Move 100
B4 B2 B3 B1
B4 B2 B3 B1
R1 R1 XX W4
R1 R1 XX W2
W1 W3 P1 P1

Move 101
B4 B2 B3 B1
B4 B2 B3 B1
R1 R1 W4 XX
R1 R1 XX W2
W1 W3 P1 P1

Move 102
B4 B2 B3 B1
B4 B2 B3 B1
R1 R1 W4 W2
R1 R1 XX XX
W1 W3 P1 P1

Move 103
B4 B2 B3 B1
B4 B2 B3 B1
R1 R1 W4 W2
R1 R1 P1 P1
W1 W3 XX XX

Move 104
B4 B2 B3 B1
B4 B2 B3 B1
R1 R1 W4 W2
R1 R1 P1 P1
W1 XX W3 XX

Move 105
B4 B2 B3 B1 
B4 B2 B3 B1
R1 R1 W4 W2
R1 R1 P1 P1
XX W1 W3 XX

Move 106
B4 B2 B3 B1
B4 B2 B3 B1
R1 R1 W4 W2
R1 R1 P1 P1
XX W1 XX W3

Move 107
B4 B2 B3 B1
B4 B2 B3 B1
R1 R1 W4 W2
R1 R1 P1 P1
XX XX W1 W3

Move 108
B4 B2 B3 B1
B4 B2 B3 B1
XX XX W4 W2
R1 R1 P1 P1
R1 R1 W1 W3

Move 109
B4 B2 B3 B1
B4 B2 B3 B1
XX W4 XX W2
R1 R1 P1 P1
R1 R1 W1 W3

Move 110
B4 B2 B3 B1
B4 B2 B3 B1
W4 XX XX W2
R1 R1 P1 P1
R1 R1 W1 W3

Move 111
B4 B2 B3 B1
B4 B2 B3 B1
W4 XX W2 XX
R1 R1 P1 P1
R1 R1 W1 W3

Move 112
B4 B2 B3 B1
B4 B2 B3 B1
W4 W2 XX XX
R1 R1 P1 P1
R1 R1 W1 W3

Move 113
B4 B2 B3 B1
B4 B2 B3 B1
W4 W2 P1 P1
R1 R1 XX XX
R1 R1 W1 W3

Move 114
B4 B2 B3 B1
B4 B2 B3 B1
W4 W2 P1 P1
R1 R1 W1 XX
R1 R1 XX W3

Move 115
B4 B2 B3 B1
B4 B2 B3 B1
W4 W2 P1 P1
R1 R1 XX W1
R1 R1 XX W3

Move 116
B4 B2 B3 B1
B4 B2 B3 B1
W4 W2 P1 P1
XX R1 R1 W1
XX R1 R1 W3
more?

'''
