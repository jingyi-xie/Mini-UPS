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

def insertDeliveries(ucommands, truckid, pkgMap, seqnum):
    delivery =  ucommands.deliveries.add()
    delivery.truckid = truckid
    for k, v in pkgMap.items():
        package = delivery.packages.add()
        package.packageid = k
        (package.x, package.y) = v
    delivery.seqnum = seqnum
    return ucommands

def insertPickup(ucommands, truckid, whid, seqnum):
    pickup = ucommands.pickups.add()
    pickup.truckid = truckid
    pickup.whid = whid
    pickup.seqnum = seqnum
    return ucommands

def insertQuery(ucommands, truckid, seqnum):
    query = ucommands.queries.add()
    query.truckid = truckid
    query.seqnum = seqnum
    return ucommands

# interaction with amazon
def createUmsg()
    return IG1.pb2.UMsg()
    
def insertAck(umsg, ack):
    umsg.ack.add(ack)
    return umsg

def insertOrderPlaced(umsg, pkgid, truckid, seq):
    orderPlaced = umsg.uorderplaced.add()
    orderPlaced.pkgid = pkgid
    orderPlaced.truckid = truckid
    orderPlaced.seq = seq
    return umsg

def insertTruckArrived(umsg, truckid, seq):
    truckArrived = umsg.utruckarrived.add()
    truckArrived.truckid = truckid
    truckArrived.seq = seq
    return umsg

def insertPkgDelivered(umsg, pkgid, seq):
    pkgDelivered = umsg.upkgdelivered.add()
    pkgDelivered.pkgid = pkgid
    pkgDelivered.seq = seq
    return umsg

def insertInitialWorld(umsg, worldid, seq):
    initWorld = umsg.initworld.add()
    initWorld.worldid = worldid
    initWorld.seq = seq
    return umsg