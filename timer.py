import time

TIMEOUT_THRESHOLD = 5

def start_timer(timer):
    timer = time.time()

def timeout(timer):
    return time.timer() - timer >=  TIMEOUT_THRESHOLD