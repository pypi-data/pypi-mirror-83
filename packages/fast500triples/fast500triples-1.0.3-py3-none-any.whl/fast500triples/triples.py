from ctypes import *
import time
import os
basedir = os.path.abspath(os.path.dirname(__file__))
libpath = os.path.join(basedir, 'sum.so')
print(libpath)
lib = cdll.LoadLibrary(libpath)
print("finding all pytha triplets for < 500")
def generate_pythas():
    lib.Hello()


if __name__ == "__main__":
    start = time.time()
    generate_pythas()
    end = time.time()
    elapsed = end - start
    print("Time taken {} seconds".format(elapsed))

