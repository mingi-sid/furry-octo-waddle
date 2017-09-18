from ailib import *
from ainetwork import *
import random

verbose = 1
game_data = {}

def move_random(board, P1robots, P2robots):
    ret = []
    for i in P1robots:
        posAction = [ACTION.MOVE,
        ACTION.PLACEMIRROR1, ACTION.PLACEMIRROR2, ACTION.SHOT, ACTION.NOTHING]
        dirAction = [DIRECTION.LEFT, DIRECTION.RIGHT, DIRECTION.UP, DIRECTION.DOWN]
        ret.append(RobotMove(random.choice(posAction),random.choice(dirAction)))
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
    move = move_random(board, P1robots, P2robots)
    game_data['turn'] -= 1
    if verbose:
        pass
    return move
