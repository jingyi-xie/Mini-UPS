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
    #add trucks to database
    initTrucks(truck_num)
    return world_s, wid

def initTrucks(truck_num):
    con = connectDB()
    csr = con.cursor()
    for i in range(truck_num):
        db_insertTruck(csr, i, 'idle')
    csr.close()
    con.commit()
    con.close()