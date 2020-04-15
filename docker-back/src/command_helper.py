from proto import world_ups_pb2

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

