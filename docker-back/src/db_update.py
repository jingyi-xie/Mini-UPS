import os
import urllib.parse as up
import psycopg2

# TODO: modify csr, conn for multithreading

def connectDB():
    con = psycopg2.connect(
        database="cobajydu",
        user="cobajydu",
        password="JKeoMazBOeXzE_dbVcBEUyUEZsIZz77s",
        host="rajje.db.elephantsql.com",
        port="5432"
    )
    csr = con.cursor()
    return con, csr

def clearDB(csr):
    sql = "TRUNCATE upsapp_ups_package, upsapp_ups_truck"
    csr.execute(sql)
    # sql = "TRUNCATE upsapp_ups_user"
    # csr.execute(sql)

def disconnectDB(con, csr):
    csr.close()
    con.close()

# package operations
def insertPackage(csr, package_id, x, y, owner, status, product_name, truck_id):
    owner = '\'' + owner + '\''
    status = '\'' + status + '\''
    product_name = '\'' + product_name + '\''

    sql = "INSERT INTO upsapp_ups_package (package_id, x, y, owner, status, product_name, truck_id) VALUES (%d, %d, %d, %s, %s, %s, %d)"
    csr.execute(sql % (package_id, x, y, owner, status, product_name, truck_id))

def updatePackage(csr, package_id, status):
    status = '\'' + status + '\''
    sql = "UPDATE upsapp_ups_package SET status = (%s) WHERE package_id = (%d)"
    csr.execute(sql % (status, package_id))

def getPackege(csr, package_id):
    sql = "SELECT status from upsapp_ups_package WHERE package_id = (%d)"
    csr.execute(sql % package_id)


# truck operations
def insertTruck(csr, truck_id, status):
    status = '\'' + status + '\''
    sql = "INSERT INTO upsapp_ups_truck (truck_id, status) VALUES (%d, %s)"
    csr.execute(sql % (truck_id, status))

def updateTruck(csr, truck_id, status):
    status = '\'' + status + '\''
    sql = "UPDATE upsapp_ups_truck SET status = (%s) WHERE truck_id = (%d)"
    csr.execute(sql % (status, truck_id))

def getTruck(csr, truck_id):
    sql = "SELECT status from upsapp_ups_truck WHERE truck_id = (%d)"
    csr.execute(sql % truck_id)

# test:
# con, csr = connectDB()

# insertPackage(csr, 200, 0, 0, 'owner', 'status', 'product_name', 500)
# updatePackage(csr, 200, 'updated status')
# csr.execute('SELECT * FROM upsapp_ups_package')

# entries = csr.fetchall()

# for i in entries:
#     print(i)

# disconnectDB(con, csr)