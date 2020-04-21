def init():
    global WORLD_RECV_SEQS
    WORLD_RECV_SEQS = set()

    global WORLD_RECV_ACKS
    WORLD_RECV_ACKS = set()

    global WORLD_MSG_MAP
    WORLD_MSG_MAP = dict()