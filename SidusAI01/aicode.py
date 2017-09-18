from ailib import *
from ainetwork import *
import random

verbose = 1
game_data = {}

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
