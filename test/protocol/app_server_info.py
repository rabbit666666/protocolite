
class NetMessageSlots:
    test1 = []
    test2 = {}

class NetMessageSpinServer:
    slots = NetMessageSlots()

class NetMessageAppServerInfo:
    spin_server = NetMessageSpinServer()
    apk_name = ''
