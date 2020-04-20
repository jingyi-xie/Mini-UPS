import select
import threading
from proto import *
from command_helper import *
from socket_helper import *
from world_helper import *
from amazon_helper import *
from db_update import *

TRUCK_NUM = 2000
WORLD_ID = 0
WORLD_SEQ = 1
AMZ_SEQ = 1

def main():
    global WORLD_SEQ, AMZ_SEQ, TRUCK_NUM, WORLD_ID
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

    #clear database
    con = connectDB()
    clearDB(con)
    #add trucks to database
    initTrucks(con, TRUCK_NUM)

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
                world_t = threading.Thread(
                    target = process_wTask,
                    args = (con, world_response, world_socket, amz_socket, AMZ_SEQ))
                AMZ_SEQ += len(world_response.completions) + len(world_response.delivered)
                world_t.start()
            elif rs == amz_socket:
                amz_msg = IG1_pb2.AMsg()
                message = receiver(amz_socket)
                amz_msg.ParseFromString(message)
                process_aTask(con, amz_msg, world_socket, amz_socket)
        for es in error_sockets:
            print('Error from ', es.getpeername())

    #Close the sockets
    world_socket.close()
    amz_socket.close()
    
if __name__ == "__main__":
    main()
