from ctypes import *
import time
lib = cdll.LoadLibrary("./sum.so")
print("finding all pytha triplets for < 500")
def generate_pythas():
    lib.Hello()


if __name__ == "__main__":
    start = time.time()
    generate_pythas()
    end = time.time()
    elapsed = end - start
    print("Time taken {} seconds".format(elapsed))

