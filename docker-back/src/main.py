from proto import *
from command_helper import *
from socket_helper import *
from world_helper import *
from amazon_helper import *

TRUCK_NUM = 2000
WORLD_ID = 0
WORLD_SEQ = 0
AMZ_SEQ = 0

def main():
    #Connect the world
    world_socket, WORLD_ID = connectWorld(TRUCK_NUM)

    #Accept connection from the amazon
    amz_socket = createAmzSocket()
    
    #Send worldid to Amazon
    sendWorldID(amz_socket, WORLD_ID, AMZ_SEQ)
    AMZ_SEQ += 1

    #TODO: Select and handle the commands from world/amazon

    #Close the sockets
    world_socket.close()
    amz_socket.close()
    
if __name__ == "__main__":
    main()
