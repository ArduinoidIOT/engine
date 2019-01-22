import chess
import multiprocessing as mp
board = chess.Board(fen="7r/p3ppk1/3p4/2p1P1Kp/2Pb4/3P1QPq/PP5P/R6R b - - 0 1")
print (board)

def getMoves():
    movelist = []
    for i in board.generate_legal_moves():
        movelist.append(i)
    return movelist


def evalPos():
    score = 0
    if board.is_checkmate():
        if len(board.stack)%2 == 0:
            return 1000000
        else:
            return -1000000
    for i in board.fen():
        if i == " ":
            break
        if i == "R":
            score -= 49
        elif i == "B":
            score -= 32
        elif i == "N":
            score -= 28
        elif i == "Q":
            score -= 90
        elif i == 'K':
            score -= 10000
        elif i == 'P':
            score -= 10
        if i == "r":
            score += 49
        elif i == "b":
            score += 32
        elif i == "n":
            score += 28
        elif i == "q":
            score += 90
        elif i == 'k':
            score += 10000
        elif i == 'p':
            score += 10
    return score


def getBestmove():
    ans = minimaxRoot(3)
    return ans


def minimax(depth, alpha, beta, isWhite):
    if board.is_checkmate():
        return evalPos()*10000/(depth+1)
    if depth == 0 :
        return evalPos()
    mover = getMoves()
    global goodevalm
    goodevalm = None
    if isWhite:
        goodevalm = 99999
        for i in mover:
            board.push(i)
            goodevalm = min(goodevalm, minimax(depth - 1, alpha, beta, not isWhite))
            board.pop()
            alpha = min(alpha, goodevalm)
            if beta <= alpha:
                return goodevalm

    else:
        goodevalm = -99999
        for i in mover:
            board.push(i)
            goodevalm = max(goodevalm, minimax(depth - 1, alpha, beta, not isWhite))
            board.pop()
            beta = max(beta,goodevalm)
            if beta <= alpha:
                return goodevalm
    return goodevalm
def dowork(move,depth,isWhite):
    board.push(move)
    value = minimax(depth - 1, -10000, 10000, not isWhite)
    board.pop()
    return move,value
#pool = mp.Pool(processes=2)

def minimaxRoot(depth, isWhite=False):
    mRmoves = getMoves()
    global betterEval
    betterEval = -99999
    global bestMoveFound
    bestMoveFound = mRmoves[0]
    for i in mRmoves:
        temp=dowork(i,depth,isWhite)
        value = temp[1]
        move=temp[0]
        if value > betterEval:
            betterEval = value
            bestMoveFound = move
    return bestMoveFound

global move
move = '0000'
while not board.is_game_over():
    if len(board.stack) % 2:
        move = str(input("Your move:"))
        moves = getMoves()
        if move.lower() != 'undo':
            try:
                board.parse_san(move)
            except:
                print("Invalid move")
                while True:
                    move = str(input("Your move:"))
                    if move.lower() != 'undo':
                        try:
                            board.parse_san(move)
                            break
                        except:
                            print("Invalid move")
                    else:
                        break
        print()
        if move.lower() != 'undo':
            board.push_san(move)
        else:
            board.pop()
            board.pop()

    print(board)
    if len(board.stack) % 2  == 0:
        if not board.is_game_over() and move.lower() != 'undo':
            moves = getMoves()
            move = getBestmove()
            board.push(move)

            print()
            print(board)
if board.is_stalemate():
    print("1/2-1/2 draw")
else:
    if len(board.stack) % 2 == 1:
        print('1-0')
    else:
        print('0-1')
