from proto import *
from socket_helper import *
from command_helper import *
from world_helper import *
from db_update import *
import time
import config

def sendWorldID(amz_socket, worldID, seqNum):
    #Create the Umsg that contains worldid
    worldIdMsg = IG1_pb2.UMsg()
    worldIdMsg = insertInitialWorld(worldIdMsg, worldID, seqNum)

    #Send UMsg to amazon
    sender(amz_socket, worldIdMsg)
    
    #Receive the response
    sendIDResult = IG1_pb2.AMsg()
    ack_message = receiver(amz_socket)
    sendIDResult.ParseFromString(ack_message)
    ack = sendIDResult.ack
    print('Ack received after sending world id to amazon' + str(ack))


def findIdleTruck(csr):
    csr.execute('SELECT truck_id FROM upsapp_ups_truck WHERE status = \'idle\'')
    return csr.fetchone()[0]

def findPkgX(csr, pkgid):
    csr.execute('SELECT x, y FROM upsapp_ups_package WHERE package_id = (%d)' % pkgid)
    return csr.fetchone()


def processAmsg(con, msg, ASEQ, WSEQ):
    csr = con.cursor()

    # lists of messages to send
    world_list = {}
    amz_list = []

    for item in msg.asendtruck:
        # 1. update truck
        truck_id = findIdleTruck(csr)
        db_updateTruck(csr, truck_id, 'loading')
        
        # 2. insert pkg
        package_id = item.pkgid
        x = item.x
        y = item.y
        owner = ''
        if item.upsid:
            owner = item.upsid
        status = 'loading'
        product_name = getProductName(item.products)
        db_insertPackage(csr, package_id, x, y, owner,
                         status, product_name, truck_id)
        
        # 3. world go pick up
        world_msg = world_ups_pb2.UCommands() # world msg 1
        pickup = world_msg.pickups.add()
        pickup.truckid = truck_id
        pickup.whid = item.whinfo.whid
        WSEQ += 1
        pickup.seqnum = WSEQ
        # world_list.append(world_msg)
        world_list[WSEQ] = world_msg # add to map

        # 4. reply amazon
        # orderplaced
        amazon_msg = IG1_pb2.UMsg() # amz msg1
        placed = amazon_msg.uorderplaced.add()
        placed.pkgid = package_id
        placed.truckid = truck_id
        ASEQ += 1
        placed.seq = ASEQ
        # ack
        amazon_msg.ack.append(item.seq)
        amz_list.append(amazon_msg)
        

    for item in msg.afinishloading:
        # 1. update truck and pkg
        db_updateTruck(csr, item.truckid, 'shipping')
        db_updatePackage(csr, item.pkgid, 'shipping')

        # 2. world go deliver
        world_msg = world_ups_pb2.UCommands()  # world msg 2
        deliver = world_msg.deliveries.add()
        deliver.truckid = item.truckid
        location = deliver.packages.add()
        location.packageid = item.pkgid
        xy = findPkgX(csr, item.pkgid)
        location.x = xy[0]
        location.y = xy[1]
        WSEQ += 1
        deliver.seqnum = WSEQ
        # world_list.append(world_msg)
        world_list[WSEQ] = world_msg  # add to map

        # 3. reply amazon
        amazon_msg = IG1_pb2.UMsg()  # amz msg2
        amazon_msg.ack.append(item.seq)
        amz_list.append(amazon_msg)

    csr.close()
    con.commit()
    return amz_list, world_list


def getProductName(products):
    names = ''
    for item in products:
        names += item.description + ', '
    return names


def process_aTask(con, msg, wSocket, aSocket, ASEQ, WSEQ):
    global WORLD_RECV_ACKS
    amz_list, world_list = processAmsg(con, msg, ASEQ, WSEQ)

    # send message to amazon
    for item in amz_list:
        sender(wSocket, item)
    
    # repeatedly messages to world
    while len(world_list):
        for key in world_list:
            if key in WORLD_RECV_ACKS:
                del world_list[key]
            else:
                sender(wSocket, world_list[key])
        time.sleep(5)
    

# # TEST ========== processAmsg
# msg = IG1_pb2.AMsg()
# # ASendTruck
# sendTruck = msg.asendtruck.add()
# wh_info = sendTruck.whinfo
# wh_info.whid = 1
# wh_info.x = 2
# wh_info.y = 3
# sendTruck.x = 5
# sendTruck.y = 10
# sendTruck.pkgid = 12
# product = sendTruck.products.add()
# product.id = 1
# product.description = 'test product'
# product.count = 5
# sendTruck.upsid = 'upsid'
# sendTruck.seq = 12345
# # AFinishLoading
# fl = msg.afinishloading.add()
# fl.pkgid = 12
# fl.truckid = 0
# fl.seq = 56789

# con = connectDB()
# clearDB(con)
# initTrucks(con, 10)
# amsg, wmsg = processAmsg(con, msg, 0, 0)

# disconnectDB(con)
# print("Amazon message ==========")
# print(amsg)
# print("World message ==========")
# print(wmsg)


# # TEST ========== findIdleTruck
# con = connectDB()
# csr = con.cursor()
# print(findIdleTruck(csr))
# csr.close()
# con.close()

# # TEST ========== findpkgXY
# con = connectDB()
# csr = con.cursor()
# print(findPkgX(csr, 12))
# csr.close()
# con.close()