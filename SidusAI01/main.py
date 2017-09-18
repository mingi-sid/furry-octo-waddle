#-*- encoding: utf-8 -*-
from ailib import *
from ainetwork import *
import aicode
import socket
import sys
import time
import random



    

def main():
    print("usage: ")
    print("%s <host> <port>"%sys.argv[0])
    print("%s <P1 or P2>"%sys.argv[0])
    print("%s"%sys.argv[0])
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
        print("host: %s, port: %d"%(host, port))
    elif len(sys.argv) == 2:
        if sys.argv[1] == 'P1':
            host = "127.0.0.1"
            port = 25252
            print ("Player 1, host: %s, port: %d"%(host, port))
        elif sys.argv[1] == 'P2':
            host = "127.0.0.1"
            port = 25253
            print ("Player 2, host: %s, port: %d"%(host, port))
        else:
            raise Exception("Invalid sys.argv[1] parameter")
            return
    else:
        host = input("Input host name(default: 127.0.0.1): ")
        if host == "": host = "127.0.0.1"
        port = input("Input port name(default: 25252): ")
        if port == "": port = "25252"
        port = int(port)
    aiNetworking = AINetworking(host, port, aicode.Init, aicode.AI)
    aiNetworking.runProgram()
    
if __name__ == "__main__":
    main()
