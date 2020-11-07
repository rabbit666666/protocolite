from out.app_server_info import *

if __name__ == '__main__':
    app_svr_info = NetMessageAppServerInfo()
    msg_slots = NetMessageSlots()
    msg_slots.set_test1([1, 2, 3])
    msg_slots.set_test2({'k': 'v'})
    msg_spin_server = NetMessageSpinServer()
    msg_spin_server.set_slots(msg_slots)
    app_svr_info.set_spin_server(msg_spin_server)
    msg = app_svr_info.serialize()
    print(msg)
    msg = NetMessageAppServerInfo().parse(msg)
    print(msg.serialize())