import multiprocessing
import os
import time


def foo_1():
    i = 0
    while True:
        time.sleep(1)
        if i == 1:
            raise multiprocessing.ProcessError
        print("Читаем показания...")
        i += 1

def foo_2():
    while True:
        time.sleep(1)
        print("Второй датчик...")


# thread_dict = {
#     'SENSOR_A': multiprocessing.Process(target=foo_2, args=(), name='SENSOR_A'),
#     'SENSOR_B': multiprocessing.Process(target=foo_1, args=(), name='SENSOR_B')
# }
procs = []

if __name__ == '__main__':
    threads = []

    proc = multiprocessing.Process(target=foo_1, args=())
    proc_2 = multiprocessing.Process(target=foo_2, args=())
    procs.append(proc)
    procs.append(proc_2)
    proc.start()
    proc_2.start()

    while True:
        # проходимся по объектам потоков
        for thread in threads:
            # если поток умер
            if not thread.is_alive():
                print(f'Поток, читающий {thread.name} умер')
                procc = multiprocessing.Process(target=foo_1, args=())
                procs.append(procc)
                procc.start()

