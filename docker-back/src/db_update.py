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
    return con

def clearDB(con):
    csr = con.cursor()
    sql = "TRUNCATE upsapp_ups_package, upsapp_ups_truck"
    csr.execute(sql)
    # sql = "TRUNCATE upsapp_ups_user"
    # csr.execute(sql)
    csr.close()
    con.commit()

def disconnectDB(con):
    con.close()

# package operations
def db_insertPackage(csr, package_id, x, y, owner, status, product_name, truck_id):
    owner = '\'' + owner + '\''
    status = '\'' + status + '\''
    product_name = '\'' + product_name + '\''

    sql = "INSERT INTO upsapp_ups_package (package_id, x, y, owner, status, product_name, truck_id) VALUES (%d, %d, %d, %s, %s, %s, %d)"
    csr.execute(sql % (package_id, x, y, owner, status, product_name, truck_id))

def db_updatePackage(csr, package_id, status):
    status = '\'' + status + '\''
    sql = "UPDATE upsapp_ups_package SET status = (%s) WHERE package_id = (%d)"
    csr.execute(sql % (status, package_id))

def db_getPackege(csr, package_id):
    sql = "SELECT status from upsapp_ups_package WHERE package_id = (%d)"
    csr.execute(sql % package_id)


# truck operations
def db_insertTruck(csr, truck_id, status):
    status = '\'' + status + '\''
    sql = "INSERT INTO upsapp_ups_truck (truck_id, status) VALUES (%d, %s)"
    csr.execute(sql % (truck_id, status))

def db_updateTruck(csr, truck_id, status):
    status = '\'' + status + '\''
    sql = "UPDATE upsapp_ups_truck SET status = (%s) WHERE truck_id = (%d)"
    csr.execute(sql % (status, truck_id))

def db_getTruck(csr, truck_id):
    sql = "SELECT status from upsapp_ups_truck WHERE truck_id = (%d)"
    csr.execute(sql % truck_id)

# # test:
# con= connectDB()
# # insert pkg
# csr = con.cursor()
# db_insertPackage(csr, 200, 0, 0, 'owner', 'status', 'product_name', 500)
# db_updatePackage(csr, 200, 'updated status')
# csr.execute('SELECT * FROM upsapp_ups_package')
# entries = csr.fetchall()

# for i in entries:
#     print(i)

# csr.close()
# # clear
# clearDB(con)
# csr = con.cursor()
# csr.execute('SELECT * FROM upsapp_ups_package')
# entries = csr.fetchall()

# for i in entries:
#     print(i)

# csr.close()
# # disconnect
# disconnectDB(con)