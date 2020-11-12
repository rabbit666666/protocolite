local protocol = require("lua.app_server_info")
local json = require("cjson")

local apple_lst = {}
for i=1, 3 do
    local apple = protocol.new_Apple()
    apple:set_weight(19.99)
    local seed = protocol.new_Seed()
    seed:set_size(5)
    apple:set_seed(seed)
    apple_lst[i] = apple
end

local fruit = protocol.new_Fruit()
fruit:set_basket_1(apple_lst)
local apple = fruit:get_basket_1()[1]   ---@type Apple
print('apple.weight:', apple:get_weight())
print('seed.size:', apple:get_seed():get_size())

local msg = fruit:serialize()
print(json.encode(msg))

msg = protocol.parse(msg)
print(json.encode(msg:serialize()))
