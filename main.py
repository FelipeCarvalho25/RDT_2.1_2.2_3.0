from threading import Thread, Event
from queue import Queue
import host_b
import host_a

queue_a = Queue()
queue_b = Queue()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    thread_host_a = Thread(target=host_a.host_a_sender, kwargs={'queue_a': queue_a, 'queue_b': queue_b}, name='host_a')
    thread_host_b = Thread(target=host_b.receiver_host_b, kwargs={'queue_a': queue_a, 'queue_b': queue_b}, name='host_b')

    thread_host_a.start()
    thread_host_b.start()
    thread_host_a.join()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
