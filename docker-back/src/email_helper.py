import yagmail
from db_update import connectDB, disconnectDB

def send_email(receiver, pkgid):
    body = "Your pakage is delivered, id is " + str(pkgid)
    yag = yagmail.SMTP('ece568ups@gmail.com', '568upsece')
    yag.send(
        to=receiver,
        subject="UPS from ECE568",
        contents=body,
    )

def db_getEmail(csr, name):
    name = '\'' + name + '\''
    sql = ('SELECT email from upsapp_ups_user WHERE username = (%s)')
    csr.execute(sql % name)
    if csr.rowcount:
        return csr.fetchone()[0]
    print("db_getEmail NO MATCHED EMAIL, name = " + name)
    return None

def db_getOwner(csr, pkgid):
    sql = ('SELECT owner from upsapp_ups_package WHERE package_id = (%d)')
    csr.execute(sql % pkgid)
    if csr.rowcount:
        return csr.fetchone()[0]
    print("db_getOwner NO MATCHED OWNER, pigid = " + str(pkgid))
    return None

def mailMan(csr, pkgid):
    owner = db_getOwner(csr, pkgid)
    receiver = db_getEmail(csr, owner)
    send_email(receiver, pkgid)
    print("mail man sent email") # testing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# test:
con= connectDB()
csr = con.cursor()

print('getowner: ' + str(db_getOwner(csr, 1)))
print('getemail: ' + str(db_getEmail(csr, 'upsid')))

csr.close()
# disconnect
disconnectDB(con)
