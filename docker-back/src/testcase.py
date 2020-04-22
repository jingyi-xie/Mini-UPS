# # ========== TEST 1 ==========
# msg = IG1_pb2.AMsg()
# # ASendTruck
# sendTruck = msg.asendtruck.add()
# wh_info = sendTruck.whinfo
# wh_info.whid = ?
# wh_info.x = ?
# wh_info.y = ?
# sendTruck.x = 5
# sendTruck.y = 5
# sendTruck.pkgid = 1
# product = sendTruck.products.add()
# product.id = 1
# product.description = 'product1'
# product.count = 1
# sendTruck.upsid = 'upsid1'
# sendTruck.seq = ?


# # ========== TEST 2 ==========
# msg = IG1_pb2.AMsg()
# # ASendTruck
# sendTruck = msg.asendtruck.add()
# wh_info = sendTruck.whinfo
# wh_info.whid = ?
# wh_info.x = ?
# wh_info.y = ?
# sendTruck.x = 10
# sendTruck.y = 10
# sendTruck.pkgid = 2
# product = sendTruck.products.add()
# product.id = 2
# product.description = 'product2'
# product.count = 2
# sendTruck.upsid = 'upsid2'
# sendTruck.seq = ?
# # AFinishLoading
# fl = msg.afinishloading.add()
# fl.pkgid = 1
# fl.truckid = 0
# fl.seq = ?
# # Ack
# msg.ack.append(???)
