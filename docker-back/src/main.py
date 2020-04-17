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
    world_s = socket.socket()
    world_s.connect((WORLD_HOST, WORLD_PORT))
    connectCommand = world_ups_pb2.UConnect()
    ENCODED_MESSAGE = createInitialConnect(connectCommand, TRUCK_NUM)

    sender(world_s, ENCODED_MESSAGE)
    whole_message = receiver(world_s)

    connectResult = world_ups_pb2.UConnected()
    connectResult.ParseFromString(whole_message)
    print(connectResult)


if __name__ == "__main__":
    main()