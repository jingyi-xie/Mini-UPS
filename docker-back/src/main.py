import select
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

    #Select and handle the commands from world/amazon
    while True:
        socket_list = [world_socket, amz_socket]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for s in read_sockets:
            if s == world_socket:
                world_response = world_ups_pb2.UResponses()
                message = receiver(world_socket)
                world_response.ParseFromString(message)
                handle_UResponse(world_response, world_socket, amz_socket)
            elif s == amz_socket:
                amz_msg = IG1_pb2.AMsg()
                message = receiver(amz_socket)
                amz_msg.ParseFromString(message)
                handle_AMsg(amz_msg, world_socket, amz_socket)

    #Close the sockets
    world_socket.close()
    amz_socket.close()
    
if __name__ == "__main__":
    main()
