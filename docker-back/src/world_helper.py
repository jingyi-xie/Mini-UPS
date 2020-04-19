import socket
from proto import *
from socket_helper import *
from command_helper import *
from db_update import *

def connectWorld(truck_num):
    #Send the UConnect command to world
    world_s = createWorldSocket()
    connectCommand = world_ups_pb2.UConnect()
    connectCommand = createInitialConnect(connectCommand, truck_num)
    sender(world_s, connectCommand)

    #TODO: add trucks to database
    initTrucks(truck_num)
    #Receive the UConnected response from world
    whole_message = receiver(world_s)
    connectResult = world_ups_pb2.UConnected()
    connectResult.ParseFromString(whole_message)
    print(connectResult)
    return world_s, connectResult.worldid

def initTrucks(truck_num):
    con = connectDB()
    csr = con.cursor()
    for i in range(truck_num):
        db_insertTruck(csr, i, 'idle')
    csr.close()
    con.commit()
    con.close()