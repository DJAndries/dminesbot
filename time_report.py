import time

start_time = None

def start_report(name):
    global start_time
    print('Starting ' + name + '...')
    start_time = time.time()

def end_report():
    print('Done ' + str(time.time() - start_time) + 's')
