import multiprocessing
import os
import time


def threadwrap(threadfunc):
    def wrapper():
        while True:
            try:
                threadfunc()
            except Exception as e:
                th_name = multiprocessing.Process.name
                print(f'Падение потока датчика {th_name}, перезапуск...')

    return wrapper


@threadwrap
def foo_1():
    i = 0
    while True:
        time.sleep(1)
        if i == 1:
            raise KeyboardInterrupt
        print("Читаем показания...")
        i += 1


@threadwrap
def foo_2():
    while True:
        time.sleep(1)
        print("Второй датчик...")


thread_dict = {
    'SENSOR_A': multiprocessing.Process(target=foo_2, args=(), name='SENSOR_A'),
    'SENSOR_B': multiprocessing.Process(target=foo_1, args=(), name='SENSOR_B')
}
procs = []

if __name__ == '__main__':
    threads = [t for t in thread_dict.values()]
    for t in threads:
        t.start()
