local protocol = require("lua.app_server_info")
local json = require("cjson")

local apple_lst = {}
for i=1, 3 do
    local apple = protocol.new_Apple()
    apple:set_name("apple_" .. i)
    apple:set_size(i)
    apple:set_weight(10)
    apple_lst[i] = apple
end

local basket = protocol.new_Basket()
basket:set_apples(apple_lst)
local apple = basket:get_apples()[1]   ---@type Apple
print('apple.name:', apple:get_name())
print('apple.weight:', apple:get_weight())

local msg = basket:serialize()
print(json.encode(msg))

msg = protocol.parse(msg)
print(json.encode(msg:serialize()))
