#!/usr/bin/python3
# hashes are a great way to divide work.


import hashlib


def alpha_shard(word):
    """ do a poor job of assigning data to servers by using first letters. """
    if word[0] < 'g':
        return 'sever0'
    elif word[0] < 'n':
        return "server1"
    elif word[0] < 't':
        return 'server2'
    else:
        return 'server3'


def hash_shard(word):
    """ assign data to servers using python's built-in hash() function """
    return "server%d" % (hash(word) % 4)


def md5_shard(word):
    data = word.encode('utf-8')
    return "server%d" % (hashlib.md5(data).digest()[-1] % 4)


if __name__ == '__main__':
    words = open('/usr/share/dict/words').read().split()
    for fun in alpha_shard, hash_shard, md5_shard:
        d = {'server0': 0, 'server1': 0, 'server2': 0, 'server3': 0}
        for word in words:
            d[fun(word.lower())] += 1
        print(fun.__name__[:-6])
        for key, value in sorted(d.items()):
            print(" {} {} {:.2}".format(key, value, value / len(words)))
        print()
