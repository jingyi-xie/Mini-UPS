import socket
import config
from proto import IG1_pb2, world_ups_pb2
from socket_helper import createWorldSocket, sender, receiver
from command_helper import createInitialConnect
from db_update import connectDB, db_insertTruck, db_updateTruck, db_getTruck, db_insertPackage, db_updatePackage

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

# TODO: send/recv operations
def processWmsg(con, msg, amz_seq):
    csr = con.cursor()
    world_msg = world_ups_pb2.UCommands()
    amazon_msg = IG1_pb2.UMsg()

    for completion in msg.completions:
        status = db_getTruck(csr, completion.truckid)
        db_updateTruck(csr, completion.truckid, completion.status)
        #if arrive at warehouse
        if status == 'en route to a warehouse':
            print("truck " + str(completion.truckid) + "arrived at warehouse")
            #send UTruckArrived to amz
            arrivedMsg = amazon_msg.utruckarrived.add()
            arrivedMsg.truckid = completion.truckid
            arrivedMsg.seq = amz_seq
            amz_seq += 1
        #if finished delivering: update status + send ack to world
        elif status == "delivering":
            print("truck " + str(completion.truckid) + "finished delivering")
        #ack to world
        world_msg.acks.append(completion.seqnum)
    for delivered in msg.delivered:
        print("package " + str(delivered.packageid) + "is delivered")
        #change package status to delivered
        db_updatePackage(csr, delivered.packageid, 'delivered')
        #send UPkgDelivered to amz
        deliveredMsg = amazon_msg.upkgdelivered.add()
        deliveredMsg.pkgid = delivered.packageid
        deliveredMsg.seq = amz_seq
        amz_seq += 1
        #send ack to world
        world_msg.acks.append(delivered.seqnum)
    # for finished in msg.finished:
    for ack in msg.acks:
        print("received ack from world " + str(ack))
        config.world_recv_acks.add(ack)
    for status in msg.truckstatus:
        print("update truck " + str(status.truck_id) + "'s status to " + str(status.status))
        #update truck status
        db_updateTruck(csr, status.truck_id, status.status)
        #ack to world
        world_msg.acks.append(status.seqnum)
    for error in msg.error:
        print("Received error from world: " + error.err)
        #ack to world
        world_msg.acks.append(error.seqnum)
    csr.close()
    con.commit()
    return amazon_msg, world_msg

def process_wTask(con, world_response, world_socket, amz_socket, AMZ_SEQ):
    amazon_msg, world_msg = processWmsg(con, world_response, AMZ_SEQ)
    # send message to world and amazon
    sender(world_socket, world_msg)
    sender(amz_socket, amazon_msg)
