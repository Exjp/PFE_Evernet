import multiprocessing, os

def worker(file):
    os.system(file)


if __name__ == '__main__':
    num = 10
    for i in range(80):
        p = multiprocessing.Process(target=worker, args=("Client2.py",))
        p.start()
