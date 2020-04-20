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
    print('Successfully connected to world with id ' + str(WORLD_ID))
    #Accept connection from the amazon
    amz_socket = createAmzSocket()
    print('Created amazon socket')
    
    #Send worldid to Amazon
    sendWorldID(amz_socket, WORLD_ID, AMZ_SEQ)
    print('Sent world id to amazon')
    AMZ_SEQ += 1

    #Select and read the messages from world/amazon
    while True:
        socket_list = [world_socket, amz_socket]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for rs in read_sockets:
            if not read_sockets:
                print("Timed out, retry...")
                continue
            if rs == world_socket:
                world_response = world_ups_pb2.UResponses()
                message = receiver(world_socket)
                world_response.ParseFromString(message)
                process_wTask(world_response, world_socket, amz_socket)
            elif rs == amz_socket:
                amz_msg = IG1_pb2.AMsg()
                message = receiver(amz_socket)
                amz_msg.ParseFromString(message)
                process_aTask(amz_msg, world_socket, amz_socket)
        for es in error_sockets:
            print('Error from ', es.getpeername())

    #Close the sockets
    world_socket.close()
    amz_socket.close()
    
if __name__ == "__main__":
    main()
