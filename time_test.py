import datetime


def read_pr():
    proxy = open("proxyes.txt", 'r').read().split("\n")
    print(len(proxy))
    second = datetime.datetime.now().timestamp()
    print(second)


def wr_pr():
    list_proxies = []
    with open("proxyes_2.txt", "w") as file:
        file.write(datetime.time)
        for line in list_proxies:
            file.write(line + '\n')



read_pr()