from threading import Thread, Event
from queue import Queue
import host_b
import host_a

queue = Queue()
event = Event()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    thread_host_a = Thread(target=host_a.host_a_sender, kwargs={'queue': queue, 'event': event}, name='host_a')
    thread_host_b = Thread(target=host_b.receiver_host_b, kwargs={'queue': queue, 'event': event}, name='host_b')

    thread_host_a.start()
    thread_host_b.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
