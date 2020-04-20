import socket
from proto import *
from socket_helper import *
from command_helper import *
from db_update import *

def connectWorld(truck_num):
    world_s = createWorldSocket()
    wid = -1
    #Keep trying until world is connected successfully
    while True:
        #Send the UConnect command to world
        connectCommand = world_ups_pb2.UConnect()
        connectCommand = createInitialConnect(connectCommand, truck_num)
        sender(world_s, connectCommand)
        #Receive the UConnected response from world
        whole_message = receiver(world_s)
        connectResult = world_ups_pb2.UConnected()
        connectResult.ParseFromString(whole_message)
        print('Connect world result is ' + connectResult.result)
        if connectResult.result == 'connected!':
            wid = connectResult.worldid
            break
    return world_s, wid

def initTrucks(con, truck_num):
    csr = con.cursor()
    for i in range(truck_num):
        db_insertTruck(csr, i, 'idle')
    csr.close()
    con.commit()
    con.close()

# TODO: send/recv operations
def process_wTask(con, msg, world_socket, amz_socket, seq):
    # csr = con.cursor()
    # for item in msg.completions:
    #     db_updateTruck(csr, item.truckid, item.status)
    # for item in msg.delivered:
    #     db_updatePackage(csr, item.packageid, 'delivered')
    # for item in msg.finished:
    #     print ''
    # for item in msg.
    # for item in msg.truckstatus:
    #     db_updateTruck(csr, item.truck_id, item.status)
    # for item in msg.

    # csr.close()
    # con.commit()
