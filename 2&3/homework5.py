# -*- coding: utf8 -*-
import random


class Bitarray:
    def __init__(self, size):
        """ Create a bit array of a specific size """
        self.size = size
        self.bitarray = bytearray(size / 8 + 1)

    def set(self, n):
        """ Sets the nth element of the bitarray """

        index = n / 8
        position = n % 8
        self.bitarray[index] = self.bitarray[index] | 1 << (7 - position)

    def get(self, n):
        """ Gets the nth element of the bitarray """

        index = n / 8
        position = n % 8
        return (self.bitarray[index] & (1 << (7 - position))) > 0


def BKDRHash(key, seed, max_size):
    # seed = 131  31 131 1313 13131 131313 etc..
    hash = 0
    for i in range(len(key)):
        hash = (hash * seed) + ord(key[i])
        hash = hash % max_size
    return hash


if __name__ == "__main__":
    max_size = 10000
    # the total table /max_size is 10000
    bitarray_obj = Bitarray(max_size)
    elements = 500
    # we add 500 elements
    list = []
    for t in range(elements):
        length = random.randint(1, 100)
        # the length of str is from 1 to 100 (random)
        count = 0
        str = ''
        for i in range(length):
            str = str + chr(random.randint(32, 127))
            # form the str
        list.append(str)
        count = count + 1
        hash1 = BKDRHash(str, 31, max_size)
        hash2 = BKDRHash(str, 100, max_size)
        hash3 = BKDRHash(str, 189, max_size)
        hash4 = BKDRHash(str, 598, max_size)
        hash5 = BKDRHash(str, 403, max_size)
        hash6 = BKDRHash(str, 574, max_size)
        hash7 = BKDRHash(str, 215, max_size)
        hash8 = BKDRHash(str, 191, max_size)
        hash9 = BKDRHash(str, 33, max_size)
        hash10 = BKDRHash(str, 5, max_size)
        bitarray_obj.set(hash1)
        bitarray_obj.set(hash2)
        bitarray_obj.set(hash3)
        bitarray_obj.set(hash4)
        bitarray_obj.set(hash5)
        bitarray_obj.set(hash6)
        bitarray_obj.set(hash7)
        bitarray_obj.set(hash8)
        bitarray_obj.set(hash9)
        bitarray_obj.set(hash10)
        # use the formula ln(2)*m\n, we get number of hash_fuction =10
        # so we use 3 hash functions
    print "It's now testing..."
    test_num = 10000
    false_count = 0
    for i in range(test_num):
        length = random.randint(1, 100)
        # the length of str is from 1 to 100 (random)
        str = ''
        for i in range(length):
            str = str + chr(random.randint(32, 127))
            # form the testing str
        test_hash1 = BKDRHash(str, 31, max_size)
        test_hash2 = BKDRHash(str, 100, max_size)
        test_hash3 = BKDRHash(str, 189, max_size)
        test_hash4 = BKDRHash(str, 598, max_size)
        test_hash5 = BKDRHash(str, 403, max_size)
        test_hash6 = BKDRHash(str, 574, max_size)
        test_hash7 = BKDRHash(str, 215, max_size)
        test_hash8 = BKDRHash(str, 191, max_size)
        test_hash9 = BKDRHash(str, 33, max_size)
        test_hash10 = BKDRHash(str, 5, max_size)
        if bitarray_obj.get(test_hash1) and \
                bitarray_obj.get(test_hash2) and \
                bitarray_obj.get(test_hash3) and \
                bitarray_obj.get(test_hash4) and \
                bitarray_obj.get(test_hash5) and \
                bitarray_obj.get(test_hash6) and \
                bitarray_obj.get(test_hash7) and \
                bitarray_obj.get(test_hash8) and \
                bitarray_obj.get(test_hash9) and \
                bitarray_obj.get(test_hash10):
            if not str in list:
                false_count += 1

    print float(false_count) / test_num