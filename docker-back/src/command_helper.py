from proto import world_ups_pb2
from proto import IG1_pb2

# interaction with world
def createInitialConnect(uconnect, truckNum):
    for i in range(0, truckNum):
        truck = uconnect.trucks.add()
        truck.id = i
        truck.x = 0
        truck.y = 0
    uconnect.isAmazon = False
    return uconnect

def insertInitialWorld(umsg, worldid, seq):
    # initWorld = umsg.initworld
    umsg.initworld.worldid = worldid
    umsg.initworld.seq = seq
    return umsg