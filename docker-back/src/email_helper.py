import yagmail
from db_update import connectDB, disconnectDB

def send_email(receiver):
    body = "Your pakage is delivered"
    yag = yagmail.SMTP('ece568ups@gmail.com', '568upsece')
    yag.send(
        to=receiver,
        subject="Yagmail test with attachment",
        contents=body,
    )

def db_getEmail(csr, name):
    name = '\'' + name + '\''
    sql = ('SELECT email from upsapp_ups_user WHERE username = (%s)')
    csr.execute(sql % name)
    return csr.fetchone()[0]

def db_getOwner(csr, pkgid):
    sql = ('SELECT owner from upsapp_ups_package WHERE package_id = (%d)')
    csr.execute(sql % pkgid)
    return csr.fetchone()[0]

def mailMan(csr, pkgid):
    owner = db_getOwner(csr, pkgid)
    receiver = db_getEmail(csr, owner)
    send_email(receiver)
    print("mail man sent email") # testing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# # test:
# con= connectDB()
# csr = con.cursor()

# print(db_getOwner(csr, 123))
# print(db_getEmail(csr, 'aaa'))

# csr.close()
# # disconnect
# disconnectDB(con)
