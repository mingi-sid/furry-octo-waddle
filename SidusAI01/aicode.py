from ailib import *
from ainetwork import *
import random



def Init(height, width, cooldownMirror, cooldownLaser, gameTurn):
    print(height, width, cooldownMirror, cooldownLaser, gameTurn)

def AI(board, P1robots, P2robots):
    
    ret = []
    
    for i in P1robots:
        posAction = [ACTION.MOVE,
		ACTION.PLACEMIRROR1, ACTION.PLACEMIRROR2, ACTION.SHOT, ACTION.NOTHING]
        dirAction = [DIRECTION.LEFT, DIRECTION.RIGHT, DIRECTION.UP, DIRECTION.DOWN]
        ret.append(RobotMove(random.choice(posAction),random.choice(dirAction)))
    return ret