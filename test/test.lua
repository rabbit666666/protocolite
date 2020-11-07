require("out.app_server_info")
local app_svr_info = NetMessageAppServerInfo.new()
local msg_slots = NetMessageSlots.new()
msg_slots:set_test1({1,2,3})
msg_slots:set_test2({k='v'})

local msg_spin_server = NetMessageSpinServer.new()
msg_spin_server:set_slots(msg_slots)

app_svr_info:set_spin_server(msg_spin_server)
local msg = app_svr_info:serialize()
print(msg)
msg = NetMessageAppServerInfo.new():parse(msg)
print(msg:serialize())