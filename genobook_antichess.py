from chess import variant as chess
import multiprocessing as mp
from datetime import datetime

board= chess.SuicideBoard()
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
            score += 49
        elif i == "B":
            score += 32
        elif i == "N":
            score += 28
        elif i == "Q":
            score += 90
        elif i == 'K':
            score += 100
        elif i == 'P':
            score += 10
        if i == "r":
            score -= 49
        elif i == "b":
            score -= 32
        elif i == "n":
            score -= 28
        elif i == "q":
            score -= 90
        elif i == 'k':
            score -= 100
        elif i == 'p':
            score -= 10
    return score


def minimax(depth, alpha, beta, isWhite):
    if depth == 0 or board.is_checkmate():
        return evalPos()
    global goodevalm
    goodevalm = None
    if isWhite:
        goodevalm = 99999
        for i in getMoves():
            board.push(i)
            goodevalm = min(goodevalm, minimax(depth - 1, alpha, beta, not isWhite))
            board.pop()
            print (i,goodevalm)
            alpha = min(alpha, goodevalm)
            if alpha >= beta:
                return goodevalm
    else:
        goodevalm = -99999
        for i in getMoves():
            board.push(i)
            goodevalm = max(goodevalm, minimax(depth - 1, alpha, beta, not isWhite))
            board.pop()
            beta = min(beta, goodevalm)
            if alpha >= beta:
                return goodevalm
    return goodevalm


def minimaxRoot(depth, isWhite=False):
    mRmoves = getMoves()
    global betterEval
    betterEval = -99999
    if isWhite:
        betterEval = -betterEval
    global bestMoveFound
    bestMoveFound = mRmoves[0]
    for i in mRmoves:
        board.push(i)
        value = minimax(depth - 1, -100000, 100000, not isWhite)
        board.pop()
        if value > betterEval:
            betterEval = value
            bestMoveFound = i
    return (bestMoveFound,betterEval)
def getBestmove():

    ans = minimaxRoot(6)
    return ans
def process(initmove):
    myboard = chess.SuicideBoard()
    myboard.push(initmove)
    retu = getBestmove()
    myboard.pop()
    print ("{0} {1} {2}".format(retu[1], initmove, str(retu[0])))
    return (retu[1],initmove,retu[2])

pool = mp.Pool(processes=4)
results = [pool.apply_async(process, args=(initmove,)) for initmove in board.generate_legal_moves()]
outputs = [p.get() for p in results]
with open("opbook-antichess-depth6","w") as opbook:
    for j in outputs:
        opbook.write("{0} {1} {2}\n".format(j[0], str(j[1]), str(j[2])))