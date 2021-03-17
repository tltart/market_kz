import multiprocessing
import os






def run():
    proc = os.getpid()
    pid.append(proc)
    print(pid)

    if proc in pid:
        return
    procs.remove(proc)

procs = []

pid = []

if __name__ == '__main__':
# def pr_run():
    for _ in range(5):
       proc = multiprocessing.Process(target=run, args=())
       procs.append(proc)
       proc.start()



    for proc in procs:
        proc.join()

    while True:
        for proc in procs:
            if proc.is_alive():
                pass
            else:
                proc = multiprocessing.Process(target=run, args=())
                procs.append(proc)
                proc.start()


# with multiprocessing.Pool(5) as process:
    #     process.map(run)
    #
    # while len(multiprocessing.active_children()) < 1:
    #     with multiprocessing.Pool(5) as process:
    #         process.map(run, procs)
