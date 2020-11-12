import py.app_server_info as proto

if __name__ == '__main__':
    apples = []
    for i in range(3):
        apple = proto.Apple()
        apple.set_name("apple_{}".format(i))
        apple.set_size(float(i + 1))
        apple.set_weight(float(10))
        apples.append(apple)
    basket = proto.Basket()
    basket.set_apples(apples)
    msg = basket.serialize()
    print(msg)
    msg = proto.Basket().parse(msg)
    print(msg.serialize())
