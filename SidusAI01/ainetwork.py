from ailib import *
import socket
class AINetworking:  
    def InitPack(self, height, width, cdM, cdL, gameTurn):
        self.gameTurn = gameTurn
        return self.InitFunc(height, width, cdM, cdL, gameTurn)
    
    def __init__(self, host, port, InitFunc, AIFunc):
        self.s = socket.socket()
        self.s.connect((host, port))
        self.InitFunc = InitFunc
        self.AIFunc = AIFunc

    def Interaction(self):
        packetStr = self.s.recv(1024).decode('utf-8')
        res = parsePacket(packetStr, self.InitPack, self.AIFunc)
        self.s.send((res).encode("utf-8"))
        
    def runProgram(self):
        self.Interaction()
        for _ in range(self.gameTurn):
            self.Interaction()