from enum import Enum

class DIRECTION(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class ACTION(Enum):
    NOTHING = 0
    MOVE = 1
    PLACEMIRROR1 = 2
    PLACEMIRROR2 = 3
    SHOT = 4

class PAWN(Enum):
    BLANK = 0
    P1 = 1
    P2 = 2
    P1MIRROR1 = 3
    P2MIRROR1 = 4
    P1MIRROR2 = 5
    P2MIRROR2 = 6

class RobotMove:
    def __init__(self, action, direction):
        self.direction = direction 
        self.action = action
    
    def __str__(self):
        return "(" + str(self.action) + ", " + str(self.direction) + ")"
    
    def __repr__(self):
        return str(self)
    
class Robot:
    def __init__(self, X, Y, CooldownMirror, CooldownLaser):
        self.X = X
        self.Y = Y
        self.CooldownMirror = CooldownMirror
        self.CooldownLaser = CooldownLaser
        
    def __str__(self):
        return "(" + str(self.X) + ", " + str(self.Y) + ", " + str(self.CooldownMirror) + ", " + str(self.CooldownLaser) + ")"

    def __repr__(self):
        return str(self)
        
def parseBoard(str):
    ret = []
    now = []
    for i in str:
        if i == '/':
            ret.append(now)
            now = []
        elif i == '_':
            now.append(PAWN.BLANK)
        elif i == 'O':
            now.append(PAWN.P1)
        elif i == 'o':
            now.append(PAWN.P2)
        elif i == 'N':
            now.append(PAWN.P1MIRROR1)
        elif i == 'n':
            now.append(PAWN.P2MIRROR1)
        elif i == 'Z':
            now.append(PAWN.P1MIRROR2)
        elif i == 'z':
            now.append(PAWN.P2MIRROR2)
    return ret

def parseRobot(str):
    divsplit = str.split('/')
    ret = []
    for i in divsplit[:-1]:
        rdata = i.split(',')
        ret.append(Robot(int(rdata[0]), int(rdata[1]), int(rdata[2]), int(rdata[3])))
    return ret

def parsePacket(str, Init, AI):
    try:
        str = str.strip()
        semsplit = str.split(';') #Init;<NUM>;<NUM>;<NUM>;<NUM>;<NUM>;
        if semsplit[0] == 'Init':
            Init(
                int(semsplit[1]),
                int(semsplit[2]), 
                int(semsplit[3]), 
                int(semsplit[4]),
                int(semsplit[5])
            )
            return "Return;Init;\n"
        elif semsplit[0] == 'AI':
            board = parseBoard(semsplit[1])
            p1robot = parseRobot(semsplit[2])
            p2robot = parseRobot(semsplit[3])
            retdata = AI(board, p1robot, p2robot)
            ret = "Return;AI;"
            for i in retdata:
                ret = ret + "UDLR"[i.direction.value] + "NM12S"[i.action.value] + "/"
            
            ret += ";\n"
            return ret
            
        else:
            raise Exception("Invalid packet.")
    except:
        raise Exception("Error parsing or calling Functions")

def main():
    def Init_t(a, b, c, d, e):
        print(a, b, c, d, e)
    
    def AI_t(a, b, c):
        print(a, b, c)
        ret = []
        for i in b:
            ret.append(RobotMove(DIRECTION.UP, ACTION.NOTHING))
        return ret
        
    print ( parsePacket("Init;1;2;3;4;5;\n", Init_t, AI_t) )
    print ( parsePacket("AI;OO/oo/;0,0,42,42,/;1,1,42,42,/;\n", Init_t, AI_t ) )
        
        
if __name__ == '__main__':
    main()
