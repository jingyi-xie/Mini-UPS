def init():
    global WORLD_RECV_SEQS
    global AMZ_RECV_SEQS
    WORLD_RECV_SEQS = set()
    AMZ_RECV_SEQS = set()

    global WORLD_MSG_MAP
    global AMZ_MSG_MAP
    WORLD_MSG_MAP = dict()
    AMZ_MSG_MAP = dict()