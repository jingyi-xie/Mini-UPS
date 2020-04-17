import socket
from proto import *
from command_helper import *
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

def sender(socket, msg):
    serialized = msg.SerializeToString()
    _EncodeVarint(socket.send, len(serialized), None)
    socket.send(serialized)

def receiver(socket):
    var_int_buff = []
    while True:
        buf = socket.recv(1)
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        if new_pos != 0:
            break
    whole_message = socket.recv(msg_len)
    return whole_message

def main():
    WORLD_HOST = '127.0.0.1' 
    WORLD_PORT = 12345
    TRUCK_NUM = 2000

    WORLD_ID = 0
    WORLD_SEQ = 1

    world_s = socket.socket()
    world_s.connect((WORLD_HOST, WORLD_PORT))
    connectCommand = world_ups_pb2.UConnect()
    connectCommand = createInitialConnect(connectCommand, TRUCK_NUM)

    sender(world_s, connectCommand)
    whole_message = receiver(world_s)

    connectResult = world_ups_pb2.UConnected()
    connectResult.ParseFromString(whole_message)
    WORLD_ID = connectResult.worldid
    print(connectResult)

    # accept connection from Amazon
    AMZ_PORT = 33333
    amz_s = socket.socket()
    amz_s.bind(('', AMZ_PORT))
    amz_s.listen(5) 
    amz_conn, addr = amz_s.accept()
    worldIdMsg = IG1.pb2.UMsg()
    worldIdMsg = insertInitialWorld(worldIdMsg, WORLD_ID, WORLD_SEQ)
    WORLD_SEQ += 1
    sender(amz_conn, worldIdMsg)

    sendIDResult = IG1.pb2.AMsg()
    ack_message = receiver(world_s)
    sendIDResult.ParseFromString(ack_message)
    ack = sendIDResult.ack
    print(ack)






if __name__ == "__main__":
    main()
