import random
import hashlib
import base64
import time


class Flag():

    flag = str(random.randint(0,2**32)).encode('utf-8')
    def hash_func(self, data):
        f = hashlib.md5(data)
        return f.hexdigest()

    def chiper(self, data):
        return base64.b64encode((data.encode('utf-8')))

    def create_flag(self):
        chiper_flag = self.hash_func(self.flag)
        chiper_flag = self.chiper(chiper_flag).decode('utf-8')
        return chiper_flag[0:28]


def generate(flag):
    for key in range(2**32):
        res = base64.b64encode((hashlib.md5(str(key).encode('utf-8')).hexdigest()).encode('utf-8')).decode('utf-8')
        if res[:28] == flag:
            print('ok')
            return res[:28]

if __name__ == '__main__':
    f = Flag()
    flag = f.create_flag()
    print(flag)
    print(2**32)
    start_time = time.time()
    h = generate(flag)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(h)
