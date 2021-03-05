import multiprocessing
import os

all_processes = ('Server.py test', 'ClientTU.py')

def execute(process):
    os.system(f'python3 {process}')

process_pool= multiprocessing.Pool(processes = 2)
process_pool.map(execute, all_processes)
