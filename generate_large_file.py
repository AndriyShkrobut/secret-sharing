import sys

with open('test.txt', 'wb') as file:
    one = 1
    i = 500 * 10 ** 6
    while i != 0:
        file.write(one.to_bytes(1, sys.byteorder))
        i -= 1