import socket
from proto import *
from command_helper import *
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint


def main():
    WORLD_HOST = '127.0.0.1' 
    WORLD_PORT = 12345
    TRUCK_NUM = 2000
    world_s = socket.socket()
    world_s.connect((WORLD_HOST, WORLD_PORT))
    connectCommand = world_ups_pb2.UConnect()
    ENCODED_MESSAGE = createInitialConnect(connectCommand, TRUCK_NUM)
    
    _EncodeVarint(world_s.send, len(ENCODED_MESSAGE.SerializeToString()), None)
    world_s.send(ENCODED_MESSAGE.SerializeToString())
    var_int_buff = []
    while True:
        buf = world_s.recv(1)
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        if new_pos != 0:
            break
    whole_message = world_s.recv(msg_len)
    connectResult = world_ups_pb2.UConnected()
    connectResult.ParseFromString(whole_message)
    print(connectResult)


if __name__ == "__main__":
    main()