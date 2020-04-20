from proto import *
from socket_helper import *
from command_helper import *
from world_helper import *
from db_update import *

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

def findPkgXY(csr, pkgid):
    csr.execute('SELECT x, y FROM upsapp_ups_package WHERE package_id = (%d)' % pkgid)
    return csr.fetchone()


def processAmsg(con, msg, ASEQ, WSEQ):
    csr = con.cursor()
    world_msg = world_ups_pb2.UCommands()
    amazon_msg = IG1_pb2.UMsg()

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
        pickup = world_msg.pickups.add()
        pickup.truckid = truck_id
        pickup.whid = item.whinfo.whid
        WSEQ += 1
        pickup.seqnum = WSEQ

        # 4. reply amazon
        # orderplaced
        placed = amazon_msg.uorderplaced.add()
        placed.pkgid = package_id
        placed.truckid = truck_id
        ASEQ += 1
        placed.seq = ASEQ
        # ack
        amazon_msg.ack.append(item.seq)
        

    for item in msg.afinishloading:
        # 1. update truck and pkg
        db_updateTruck(csr, item.truckid, 'shipping')
        db_updatePackage(csr, item.pkgid, 'shipping')

        # 2. world go deliver
        deliver = world_msg.deliveries.add()
        deliver.truckid = item.truck_id
        location = deliver.packages.add()
        location.packageid = item.pkgid
        location.x = findPkgXY(item.pkgid)[0]
        location.y = findPkgXY(item.pkgid)[1]
        WSEQ += 1
        deliver.seqnum = WSEQ

        # 3. reply amazon
        amazon_msg.ack.append(item.seq)

    #  # TODO
    # for item in msg.ack:
    #     # 1. compare with seq
    #     # 2. resend message

    csr.close()
    con.commit()
    return amazon_msg, world_msg


def getProductName(products):
    names = ''
    for item in products:
        names += item.description + ', '
    return names


def process_aTask(con, msg, wSocket, aSocket, ASEQ, WSEQ):
    amazon_msg, world_msg = processAmsg(con, msg, ASEQ, WSEQ)
    # send message to world and amazon
    sender(wSocket, world_msg)
    sender(aSocket, amazon_msg)

# # TEST ========== processAmsg
# msg = IG1_pb2.AMsg()
# sendTruck = msg.asendtruck.add()
# wh_info = sendTruck.whinfo
# wh_info.whid = 1
# wh_info.x = 2
# wh_info.y = 3
# sendTruck.x = 10
# sendTruck.y = 20
# sendTruck.pkgid = 12
# product = sendTruck.products.add()
# product.id = 1
# product.description = 'description info'
# product.count = 5
# sendTruck.upsid = 'upsid'
# sendTruck.seq = 12345

# con = connectDB()
# clearDB(con)
# initTrucks(con, 10)
# con = connectDB()
# processAmsg(con, msg, 0, 0)


# # TEST ========== findIdleTruck
# con = connectDB()
# csr = con.cursor()
# print(findIdleTruck(csr))
# csr.close()
# con.close()

# # # TEST ========== findpkgXY
# con = connectDB()
# csr = con.cursor()
# x = findPkgXY(csr, 12)
# print(x[0])
# print(x[1])
# csr.close()
# con.close()
