import socket
from proto import world_ups_pb2
from command_helper import *



def main():
    WORLD_HOST = '127.0.0.1' 
    WORLD_PORT = 12345
    TRUCK_NUM = 2000
    world_s = socket.socket()
    world_s.connect((WORLD_HOST, WORLD_PORT))
    connectCommand = world_ups_pb2.UConnect()
    createInitialConnect(connectCommand, TRUCK_NUM)
    



if __name__ == "__main__":
    main()