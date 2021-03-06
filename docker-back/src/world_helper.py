import socket
import config
from email_helper import mailMan
from proto import IG1_pb2, world_ups_pb2
from socket_helper import createWorldSocket, sender, receiver
from command_helper import createInitialConnect
from db_update import clearDB, disconnectDB, connectDB, db_insertTruck, db_updateTruck, db_getTruck, db_insertPackage, db_updatePackage

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

def processWmsg(con, msg, amz_seq):
    csr = con.cursor()
    world_msg = world_ups_pb2.UCommands()
    amazon_msg = IG1_pb2.UMsg()

    for completion in msg.completions:
        # 1. detect duplication
        if completion.seqnum in config.WORLD_RECV_SEQS:
            continue

        # 2. get truck's current status
        status = db_getTruck(csr, completion.truckid)

        # 3. update truck status
        db_updateTruck(csr, completion.truckid, completion.status)

        # 4.1 if arrive at warehouse
        if status == 'en route to a warehouse':
            print("truck " + str(completion.truckid) + " arrived at warehouse")
            #send UTruckArrived to amz
            arrivedMsg = amazon_msg.utruckarrived.add()
            arrivedMsg.truckid = completion.truckid
            amz_seq += 1
            arrivedMsg.seq = amz_seq

        # 4.2 if finished delivering: update status + send ack to world
        elif status == "delivering":
            print("truck " + str(completion.truckid) + " finished delivering")

        # 5. send ack to world
        world_msg.acks.append(completion.seqnum)

        # 6. add seq# to list
        config.WORLD_RECV_SEQS.add(completion.seqnum)

    for delivered in msg.delivered:
        # 1. detect duplication 
        if delivered.seqnum in config.WORLD_RECV_SEQS:
            continue

        print("package " + str(delivered.packageid) + " is delivered")
        
        # 2. change package status to delivered
        db_updatePackage(csr, delivered.packageid, 'delivered')
        try:
            mailMan(csr, delivered.packageid) # send email
        except Exception as e:
            print("Email not sent because: " + str(e) + " pkgid = " + str(delivered.packageid))
        
        # 3. send UPkgDelivered to amz
        deliveredMsg = amazon_msg.upkgdelivered.add()
        deliveredMsg.pkgid = delivered.packageid
        amz_seq += 1
        deliveredMsg.seq = amz_seq
        
        # 4. send ack to world
        world_msg.acks.append(delivered.seqnum)
        
        # 5. add seq# to list
        config.WORLD_RECV_SEQS.add(delivered.seqnum)
    # for finished in msg.finished:
    
    for ack in msg.acks:
        print("received ack from world " + str(ack))
        # add ack to receive list
        config.WORLD_RECV_ACKS.add(ack)
    
    for status in msg.truckstatus:
        # 1. detect duplication
        if status.seqnum in config.WORLD_RECV_SEQS:
            continue
        print("update truck " + str(status.truckid) + "'s status to " + str(status.status))
        
        # 2. update truck status
        db_updateTruck(csr, status.truckid, status.status)
        
        # 3. send ack to world
        world_msg.acks.append(status.seqnum)
        
        # 4. add seq# to list
        config.WORLD_RECV_SEQS.add(status.seqnum)
    
    for error in msg.error:
        # 1. detect duplication
        if error.seqnum in config.WORLD_RECV_SEQS:
            continue
        print("Received error from world: " + error.err)
        
        # 2. send ack to world
        world_msg.acks.append(error.seqnum)
        
        # 3. add seq# to list
        config.WORLD_RECV_SEQS.add(error.seqnum)
    
    csr.close()
    con.commit()
    return amazon_msg, world_msg

def process_wTask(con, world_response, world_socket, amz_socket, AMZ_SEQ):
    amazon_msg, world_msg = processWmsg(con, world_response, AMZ_SEQ)

    world_msg.disconnect = False

    # send message to world and amazon
    sender(world_socket, world_msg)
    print("send to world =================\n" + str(world_msg))
    if str(amazon_msg) != '':
        sender(amz_socket, amazon_msg)
    print('send to AMZ ==============\n' + str(amazon_msg))


# # TEST ========== processWmsg
# msg = world_ups_pb2.UResponses()
# #Completion1
# complete_1 = msg.completions.add()
# complete_1.truckid = 1
# complete_1.x = 0
# complete_1.y = 0
# complete_1.status = 'invalid'
# complete_1.seqnum = 11
# #Completion2
# complete_2 = msg.completions.add()
# complete_2.truckid = 2
# complete_2.x = 0
# complete_2.y = 0
# complete_2.status = 'waiting for pickup'
# complete_2.seqnum = 22
# #Delivered
# delivery = msg.delivered.add()
# delivery.truckid = 1
# delivery.packageid = 123
# delivery.seqnum = 33
# #Acks
# msg.acks.append(111)
# msg.acks.append(222)
# #Truck status
# truckstatus = msg.truckstatus.add()
# truckstatus.truckid = 3
# truckstatus.status = 'test status'
# truckstatus.x = 44
# truckstatus.y = 55
# truckstatus.seqnum = 44
# #Errors
# e = msg.error.add()
# e.err = 'error info'
# e.originseqnum = 123
# e.seqnum = 55

# con = connectDB()
# csr = con.cursor()
# clearDB(con)
# initTrucks(con, 10)
# db_updateTruck(csr, 1, 'en route to a warehouse')
# db_updateTruck(csr, 2, 'delivering')
# db_insertPackage(csr, 123, 0, 0, 'owner', 'status', 'product_name', 1)
# amsg, wmsg = processWmsg(con, msg, 0)
# disconnectDB(con)
# print("Amazon message ========== \n" + str(amsg))
# print("World message ========== \n" + str(wmsg))