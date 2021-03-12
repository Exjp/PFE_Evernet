import multiprocessing, os, time

def worker(file):
    os.system(file)


if __name__ == '__main__':
    num = 10
    for i in range(5000):
        #for i in range(1):
        p = multiprocessing.Process(target=worker, args=("Client2.py",))
        p.start()
        print(i)
        time.sleep(0.2)
    exit()
