import threading
import logging
import time
import random

class Counter:
    def __init__(self, ini=0):
        self.lock = threading.Lock()
        self.value = ini

    def increment(self):
        self.lock.acquire()
        self.value += 1
        self.lock.release()

    def __str__(self):
        return str(self.value)

def worker(c):
    logging.debug('Starting ...')
    for i in range(2):
        pause = random.random()
        logging.debug('Sleeping %20.2f' % pause)
        time.sleep(pause)
        c.increment()
        logging.debug('counter:  %s' % c)
    logging.debug('Done.')

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
count = Counter()
t1 = threading.Thread(target=worker, args=(count,))
t2 = threading.Thread(target=worker, args=(count,))
t1.start()
t2.start()
