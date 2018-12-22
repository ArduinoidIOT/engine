import chess
from datetime import datetime

board = chess.Board()


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
    if depth == 0 or board.is_checkmate():
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


def minimaxRoot(depth, isWhite=False):
    mRmoves = getMoves()
    global betterEval
    betterEval = -99999
    global bestMoveFound
    bestMoveFound = mRmoves[0]
    for i in mRmoves:
        board.push(i)
        value = minimax(depth - 1, -10000, 10000, not isWhite)
        board.pop()
        if value > betterEval:
            betterEval = value
            bestMoveFound = i
    return bestMoveFound


while not board.is_game_over():
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

    if not board.is_game_over() and move.lower() != 'undo':
        moves = getMoves()
        move = getBestmove()
        print(move)
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
"""var
        minimaxRoot = function(depth, game, isMaximisingPlayer)
        {

            var
        newGameMoves = game.ugly_moves();
        var bestMove = -9999;
        var
        bestMoveFound;

        for (var i = 0; i < newGameMoves.length; i++) {
            var newGameMove = newGameMoves[i];
        game.ugly_move(newGameMove);
        var value = minimax(depth - 1, game, !isMaximisingPlayer);
        game.undo();
        if (value >= bestMove) {
        bestMove = value;
        bestMoveFound = newGameMove;
        }
        }
        return bestMoveFound;
        };"""
