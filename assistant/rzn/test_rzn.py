import time


def test(number):
    for i in range(number):
        print(i)
        time.sleep(5)


test(10)
