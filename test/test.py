import py.app_server_info as proto

if __name__ == '__main__':
    apples = []
    for _ in range(3):
        apple = proto.Apple()
        apple.set_weight(19.99)
        apples.append(apple)

    fruit = proto.Fruit()
    fruit.set_basket_1(apples)
    msg = fruit.serialize()
    print(msg)
    msg = proto.Fruit().parse(msg)
    print(msg.serialize())
