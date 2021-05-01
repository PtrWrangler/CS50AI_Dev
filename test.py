EMPTY = None
X = "X"
O = "O"

board = [[O, O, X],
         [O, X, EMPTY],
         [X, O, O]]

# board = [[EMPTY, EMPTY, EMPTY],
#          [EMPTY, EMPTY, EMPTY],
#          [EMPTY, EMPTY, EMPTY]]

winningPlayer = None
boardLength = len(board)
# Check Diagonals
if board[0][0] is not None:
    winningPlayer = board[0][0]
for diag in range(1, boardLength):
    if board[diag][diag] is not winningPlayer:
        winningPlayer = None
        break
if winningPlayer is not None:
    print("Left diag wins: ", winningPlayer)

   
boardLengthIndex = boardLength - 1
if board[0][boardLengthIndex] is not None:
    winningPlayer = board[0][boardLengthIndex]
for diag in range(1, boardLength):
    if board[diag][boardLengthIndex - diag] is not winningPlayer:
        winningPlayer = None
        break
if winningPlayer is not None:
    print("Right diag wins: ", winningPlayer)



# action = (1,2)
# print(board[action[0]][action[1]])