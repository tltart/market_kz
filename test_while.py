import time
import json
import ast

ss = ['https://market.kz/nedvizhimost/?page=1571&query%5Bdata%5D%5Bprice%5D%5Bfrom%5D=10000000', 'https://market.kz/nedvizhimost/?page=1522&query%5Bdata%5D%5Bprice%5D%5Bfrom%5D=10000000']

def write_href_fin(text):
    fp = open('href_fin.txt', 'a')
    fp.write(str(text) + '\n')
    fp.close()

hh = ['https://market.kz/nedvizhimost/?page=1571&query%5Bdata%5D%5Bprice%5D%5Bfrom%5D=10000000', 'https://market.kz/nedvizhimost/?page=1573&query%5Bdata%5D%5Bprice%5D%5Bfrom%5D=10000000']

url = 'https://market.kz/nedvizhimost/?page=1571&query%5Bdata%5D%5Bprice%5D%5Bfrom%5D=10000000'

def read_page():
    sp = []
    page_ = open("href_fin.txt", 'r').read().split('\n')
    for i in page_:
        z = i.replace('[', '').replace(']', '').replace('"', '').replace("'", '')
        l = z.replace(' ', '').split(',')
        for i in l:
            sp.append(i)
    print(sp)

    return read_page()


def read_page_3():
    sp = []
    res = []
    page_ = open("href_fin.txt", 'r').read().split('\n')
    for i in page_:
        z = i.replace('[', '').replace(']', '').replace('"', '').replace("'", '')
        l = z.replace(' ', '').split(',')
        for i in l:
            sp.append(i)
    for i in sp:
        if i in hh:
            res.append(i)
    print(res)


def check_url_in_file():
    page_ = open("result.txt", 'r').read().split('\n')
    if len(page_) > 1:
        page_.pop()
        print(page_[0])
        page_.pop(0)
        with open('res_2.txt', 'a') as ff:
            for i in page_:
                ff.write(str(i) + '\n')






check_url_in_file()