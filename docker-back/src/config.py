def init():
    global WORLD_RECV_SEQS
    WORLD_RECV_SEQS = set()

    global WORLD_RECV_ACKS
    WORLD_RECV_ACKS = set()

    global SEQ_TO_WORLD
    SEQ_TO_WORLD = set()