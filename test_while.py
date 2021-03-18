import time
import json
import ast

ss = ['https://market.kz/nedvizhimost/?page=1571&query%5Bdata%5D%5Bprice%5D%5Bfrom%5D=10000000', 'https://market.kz/nedvizhimost/?page=1522&query%5Bdata%5D%5Bprice%5D%5Bfrom%5D=10000000']

def write_href_fin(text):
    fp = open('href_fin.txt', 'a')
    fp.write(str(text) + '\n')
    fp.close()

hh = 'https://market.kz/nedvizhimost/?page=1571&query%5Bdata%5D%5Bprice%5D%5Bfrom%5D=10000000'

def read_page():
    sp = []
    page_ = open("href_fin.txt", 'r').read().split('\n')
    for i in page_:
        z = i.replace('[', '').replace(']', '').replace('"', '').replace("'", '')
        l = z.replace(' ', '').split(',')
        for i in l:
            sp.append(i)
    print(hh in sp)




read_page()