from db_update import *
from world_helper import *
from proto import IG1_pb2

def findIdleTruck():
    return 10


def process_amsg(con, msg):
    for item in msg.asendtruck:
        csr = con.cursor()
        truck_id = findIdleTruck()
        db_updateTruck(csr, truck_id, 'warehouse')
        csr.close()
        # TODO: world send truck

# # test
# msg = IG1_pb2.AMsg()
# sendTruck = msg.asendtruck.add()
# wh_info = sendTruck.whinfo
# wh_info.whid = 1
# wh_info.x = 2
# wh_info.y = 3
# sendTruck.x = 0
# sendTruck.y = 0
# sendTruck.pkgid = 12
# product = sendTruck.products.add()
# product.id = 1
# product.description = 'description info'
# product.count = 5
# sendTruck.upsid = 'upsid'
# sendTruck.seq = 12345

# # db
# con = connectDB()
# clearDB(con)

# initTrucks(100)
# process_amsg(con, msg)

# con.commit()