import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

WORLD_HOST = 'vcm-14615.vm.duke.edu'
WORLD_PORT = 12345
AMZ_PORT = 33333

def createWorldSocket():
    s = socket.socket()
    s.connect((WORLD_HOST, WORLD_PORT))
    return s

def createAmzSocket():
    amz_s = socket.socket()
    amz_s.bind((socket.gethostbyname(socket.gethostname()), AMZ_PORT))
    amz_s.listen(5) 
    amz_conn, addr = amz_s.accept()
    return amz_conn

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