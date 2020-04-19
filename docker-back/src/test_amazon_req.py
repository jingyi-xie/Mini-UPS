from db_update import db_updateTruck, db_insertPackage, db_updatePackage
from world_helper import initTrucks
from proto import IG1_pb2


def findIdleTruck(csr):
    csr.execute('SELECT truck_id FROM upsapp_ups_truck WHERE status = \'idle\'')
    return csr.fetchone()[0]


def processAmsg(con, msg):
    csr = con.cursor()
    for item in msg.asendtruck:
        # update truck
        truck_id = findIdleTruck(csr)
        db_updateTruck(csr, truck_id, 'loading')

        # TODO: world send truck

        # insert pkg
        package_id = item.pkgid
        x = item.x
        y = item.y
        owner = ''
        if item.upsid:
            owner = item.upsid
        status = 'loading'
        product_name = getProductName(item.products)
        db_insertPackage(csr, package_id, x, y, owner,
                         status, product_name, truck_id)

    for item in msg.afinishloading:
        db_updateTruck(csr, item.truckid, 'shipping')
        db_updatePackage(csr, item.pkgid, 'shipping')
    csr.close()
    con.commit()

def getProductName(products):
    names = ''
    for item in products:
        names += item.description + ', '
    return names

# # TEST ========== processAmsg
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

# initTrucks(10)
# processAmsg(con, msg)

# con.commit()


# # TEST ========== findIdleTruck
# con = connectDB()
# csr = con.cursor()
# print(findIdleTruck(csr))
# csr.close()
# con.close()
