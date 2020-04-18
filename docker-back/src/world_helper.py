import socket
from proto import *
from socket_helper import *
from command_helper import *

def connectWorld(truck_num):
    #Send the UConnect command to world
    world_s = createWorldSocket()
    connectCommand = world_ups_pb2.UConnect()
    connectCommand = createInitialConnect(connectCommand, truck_num)
    sender(world_s, connectCommand)

    #TODO: add trucks to database

    #Receive the UConnected response from world
    whole_message = receiver(world_s)
    connectResult = world_ups_pb2.UConnected()
    connectResult.ParseFromString(whole_message)
    print(connectResult)
    return world_s, connectResult.worldid
