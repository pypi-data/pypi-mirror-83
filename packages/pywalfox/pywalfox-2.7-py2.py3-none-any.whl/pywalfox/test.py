import os
import sys
import threading

def print_work_b():
    print('Starting of thread :', threading.currentThread().name)
    print('Finishing of thread :', threading.currentThread().name)


a = threading.Thread(target=print_work_b, name='Thread-a')
a.daemon = True
a.start()
