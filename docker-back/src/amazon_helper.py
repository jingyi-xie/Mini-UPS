from proto import *
from socket_helper import *
from command_helper import *

def sendWorldID(amz_socket, worldID, seqNum):
    #Create the Umsg that contains worldid
    worldIdMsg = IG1.pb2.UMsg()
    worldIdMsg = insertInitialWorld(worldIdMsg, worldID, seqNum)

    #Send UMsg to amazon
    sender(amz_socket, worldIdMsg)
    
    #Receive the response
    sendIDResult = IG1.pb2.AMsg()
    ack_message = receiver(amz_socket)
    sendIDResult.ParseFromString(ack_message)
    ack = sendIDResult.ack
    print(ack)