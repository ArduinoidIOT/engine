from chess import variant as chess

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
def minimax(depth,alpha,beta, isWhite):
    if depth == 0 or board.is_checkmate():
        return evalPos()
    
    global goodevalm
    goodevalm = None
    if isWhite:
        goodevalm = 99999
        for i in mover:
            board.push(i)
            goodevalm = min(goodevalm, minimax(depth - 1,alpha,beta,not isWhite))
            board.pop()
            alpha = min(alpha,goodevalm)
            if alpha >= beta:
                return goodevalm
    else:
        goodevalm = -99999
        for i in mover:
            board.push(i)
            goodevalm = max(goodevalm, minimax(depth - 1, alpha,beta, not isWhite))
            board.pop()
            beta = min(beta, goodevalm)
            if alpha >= beta:
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
        value = minimax(depth - 1,-100000,100000, not isWhite)
        board.pop()
        if value > betterEval:
            betterEval = value
            bestMoveFound = i
    return bestMoveFound
def getBestmove():
    ans = minimaxRoot(4)
    return ans
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
        board.push(move)

        print()
        print(board)
if board.is_stalemate():
    print("1/2-1/2 draw")
else:
    if len(board.stack) % 2 == 1:
        print('0-1')
    else:
        print('1-0')
