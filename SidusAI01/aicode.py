from ailib import *
from ainetwork import *
import random

verbose = 1
game_data = {}

#Returns all possible list of (P1move, P2move)
def generate_all_moves(board, P1robots, P2robots):
    allRobotMove = [[tuple(action, direction),] for action in ACTION\
                   for direction in DIRECTION]
    allP1move = []
    allP1move3 = [[move1, move2, move3] for move1 in allRobotMove for move2 in allRobotMove\
                 for move3 in allRobotMove]
    allP1move2 = [[move1, move2] for move1 in allRobotMove for move2 in allRobotMove]

    if len(P1robots) == 3:
        allP1move = allP1move3[:]
    elif len(P1robots) == 2:
        allP1move = allP1move2[:]
    elif len(P1robots) == 1:
        allP1move = allRobotMove[:]
    else:
        allP1move = []

    allP2move = []
    if len(P2robots) == 3:
        allP2move = allP1move3[:]
    elif len(P2robots) == 2:
        allP2move = allP1move2[:]
    elif len(P2robots) == 1:
        allP2move = allRobotMove[:]
    else:
        allP2move = []

    #removing redundant moves
    for i in range(len(P1robots)):
        pass

    allMove = [tuple(p1, p2) for p1 in allP1move for p2 in allP2move]
    return allMove

#Simulate the next board state
def simulate_board(board, P1robots, P2robots, P1move, P2move):
    newBoard = [x[:] for x in board]
    newP1robots = P1robots[:]
    newP2robots = P2robots[:]
    directionMap = {DIRECTION.UP : (-1, 0),\
            DIRECTION.DOWN : (1, 0),\
            DIRECTION.LEFT : (0, -1),\
            DIRECTION.RIGHT : (0, 1)}
    #Moving stage
    for i in range(len(P1robots)):
        if P1move[i][0] == ACTION.MOVE:
            newP1robots[i].X += directionMap[P1move[i][1]][0]
            newP1robots[i].X = min(game_data['W']-1, max(0, newP1robots[i].X))
            newP1robots[i].Y += directionMap[P1move[i][1]][1]
            newP1robots[i].Y = min(game_data['H']-1, max(0, newP1robots[i].Y))
            #Ignore movement if robot tries to enter enemy area or mirror
            #Ignore both movement if there is a robot tries to move to the same position
    for i in range(len(P2robots)):
        if P2move[i][0] == ACTION.MOVE:
            newP2robots[i].X += directionMap[P2move[i][1]][0]
            newP2robots[i].X = min(game_data['W']-1, max(0, newP2robots[i].X))
            newP2robots[i].Y += directionMap[P2move[i][1]][1]
            newP2robots[i].Y = min(game_data['H']-1, max(0, newP2robots[i].Y))
            #Ignore movement if robot tries to enter enemy area or mirror
            #Ignore both movement if there is a robot tries to move to the same position
    #Mirror setting stage
    for i in range(len(P1robots)):
        if P1move[i][0] == ACTION.PLACEMIRROR1:
            mirrorX = P1robots[i].X + directionMap[P1move[i][1]][0]
            mirrorY = P1robots[i].Y + directionMap[P1move[i][1]][1]
            if mirrorX < 0 or mirrorX >= game_data['W'] or \
                     mirrorY < 0 or mirrorY >= game_data['H']:
                continue
            #Ignore both setting if there is a robot tries to set a mirror at the same position
            newBoard[mirrorX][mirrorY] = PAWN.P1MIRROR1
        elif P1move[i][0] == ACTION.PLACEMIRROR2:
            mirrorX = P1robots[i].X + directionMap[P1move[i][1]][0]
            mirrorY = P1robots[i].Y + directionMap[P1move[i][1]][1]
            if mirrorX < 0 or mirrorX >= game_data['W'] or \
                     mirrorY < 0 or mirrorY >= game_data['H']:
                continue
            #Ignore both setting if there is a robot tries to set a mirror at the same position
            newBoard[mirrorX][mirrorY] = PAWN.P1MIRROR2
    for i in range(len(P2robots)):
        if P2move[i][0] == ACTION.PLACEMIRROR1:
            mirrorX = P2robots[i].X + directionMap[P2move[i][1]][0]
            mirrorY = P2robots[i].Y + directionMap[P2move[i][1]][1]
            if mirrorX < 0 or mirrorX >= game_data['W'] or \
                     mirrorY < 0 or mirrorY >= game_data['H']:
                continue
            #Ignore both setting if there is a robot tries to set a mirror at the same position
            newBoard[mirrorX][mirrorY] = PAWN.P2MIRROR1
        elif P2move[i][0] == ACTION.PLACEMIRROR2:
            mirrorX = P2robots[i].X + directionMap[P2move[i][1]][0]
            mirrorY = P2robots[i].Y + directionMap[P2move[i][1]][1]
            if mirrorX < 0 or mirrorX >= game_data['W'] or \
                     mirrorY < 0 or mirrorY >= game_data['H']:
                continue
            #Ignore both setting if there is a robot tries to set a mirror at the same position
            newBoard[mirrorX][mirrorY] = PAWN.P2MIRROR2
    #Beam shooting stage
    #TODO:kill myself

    return (newBoard, newP1robots, newP2robots)

#Find a dangerous cell in the 1st column
def find_hazard_1st_column(board, P1robots, P2robots):
    hazardCell = []
    directionMap = {DIRECTION.UP : (-1, 0),\
            DIRECTION.DOWN : (1, 0),\
            DIRECTION.LEFT : (0, -1),\
            DIRECTION.RIGHT : (0, 1)}
    mirror1Map = {DIRECTION.UP : DIRECTION.LEFT,\
            DIRECTION.LEFT : DIRECTION.UP,\
            DIRECTION.DOWN : DIRECTION.RIGHT,\
            DIRECTION.RIGHT : DIRECTION.UP}
    mirror2Map = {DIRECTION.UP : DIRECTION.RIGHT,\
            DIRECTION.RIGHT : DIRECTION.UP,\
            DIRECTION.DOWN : DIRECTION.LEFT,\
            DIRECTION.LEFT : DIRECTION.UP}
    for robot in P2robots:
        posX = P2robots.X
        posY = P2robots.Y
        for direction in DIRECTION: 
            beamDir = direction
            for i in range(91):
                posX += directionMap[beamDir][0]
                posY += directionMap[beamDir][1]
                if posX < 0 or posX >= game_data['W'] or \
                       posY < 0 or posY >= game_data['H']:
                    break
                if board[posX][posY] in [PAWN.P1MIRROR1, PAWN.P2MIRROR1]:
                    beamDir = mirror1Map[beamDir]
                elif board[posX][posY] in [PAWN.P1MIRROR2, PAWN.P2MIRROR2]:
                    beamDir = mirror2Map[beamDir]
                if posX == 0:
                    hazardCell.append((posX, posY))
    return hazardCell

def eval_default(board, P1robots, P2robots):
    return eval_summation(board, P1robots, P2robots)

def eval_summation(board, P1robots, P2robots):
    evaluation = 0.0
    for i in board:
        for j in i:
            if j in [PAWN.P1, PAWN.P1MIRROR1, PAWN.P1MIRROR2]:
                evaluation += 1.0
            elif j in [PAWN.P2, PAWN.P2MIRROR1, PAWN.P2MIRROR2]:
                evaluation -= 1.0
    evaluation += float(game_data['turn'] * len(P1robots))
    evaluation -= float(game_data['turn'] * len(P2robots))
    return evaluation

def move_default(board, P1robots, P2robots):
    return move_line_fire(board, P1robots, P2robots)

def move_random(board, P1robots, P2robots):
    ret = []
    for i in P1robots:
        posAction = [ACTION.MOVE,
        ACTION.PLACEMIRROR1, ACTION.PLACEMIRROR2, ACTION.SHOT, ACTION.NOTHING]
        dirAction = [DIRECTION.LEFT, DIRECTION.RIGHT, DIRECTION.UP, DIRECTION.DOWN]
        ret.append(RobotMove(random.choice(posAction),random.choice(dirAction)))
    return ret

def move_line_fire(board, P1robots, P2robots):
    ret = []
    for i in P1robots:
        if i.CooldownLaser == 0:
            ret.append(RobotMove(ACTION.SHOT, DIRECTION.RIGHT))
        else:
            ret.append(RobotMove(ACTION.MOVE, random.choice([DIRECTION.UP, DIRECTION.DOWN])))
    return ret

def Init(height, width, cooldownMirror, cooldownLaser, gameTurn):
    print(height, width, cooldownMirror, cooldownLaser, gameTurn)
    game_data['H'] = height
    game_data['W'] = width
    game_data['CoolM'] = cooldownMirror
    game_data['CoolL'] = cooldownLaser
    game_data['Turn'] = gameTurn
    game_data['turn'] = game_data['Turn']

def AI(board, P1robots, P2robots):
    move = []
    move = move_default(board, P1robots, P2robots)
    game_data['turn'] -= 1
    if game_data['turn'] >= 95:
        print(P1robots)
        print(move)
    if verbose:
        pass
    return move
