import sys
import time

if __name__ == '__main__':

    start = time.time()

    for i in range(5):
        print(i)

    end = time.time()
    print("time", end - start)