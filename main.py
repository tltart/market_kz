import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from random import choice
import pandas as pd
import time
from multiprocessing import Process
from threading import Thread
import datetime
from random import random

from market_kz.parse_proxy import Parse_proxy

class P():

    def __init__(self):
        self.proxy = None
        self.proxy_choice = ''
        self.user_agent = None
        self.user_agent_choice = None
        self.df = pd.DataFrame({'Object': [], 'Name': [], 'City': [], 'Phone': [], 'Price': [], 'href': []})
        self.capa = DesiredCapabilities.CHROME
        self.capa["pageLoadStrategy"] = "none"
        self.url = ''
        self.false_parse = 0


    def read_page(self):
        page_ = open("page.txt", 'r')
        self.page = int(page_.read())
        page_.close()
        return self.page

    def write_page(self):
        page_ = open("page.txt", 'w')
        page_.write(str(self.page + 1))
        page_.close()

    def write_false_url(self, text):
        fp = open('result.txt', 'a')
        fp.write(text + '\n')
        fp.close()

    def write_href_fin(self, text):
        fp = open('href_fin.txt', 'a')
        fp.write(text + '\n')
        fp.close()

    def new_driver(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--proxy-server=%s' % self.get_proxy())
        self.options.add_argument('--user-agent=%s' % self.get_user_agent())
        self.driver = webdriver.Chrome(desired_capabilities=self.capa, executable_path="chromedriver.exe", options=self.options)
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(self.driver, 5)

    def get_proxy(self):
        tt = random()
        self.proxy = open("proxyes.txt", 'r').read().split("\n")
        while self.proxy_choice == '':
            if len(self.proxy) < 3 and (int(self.proxy[0]) + 30) < int(datetime.datetime.now().timestamp()):
                print(f'Процесс {os.getpid()} начал добывать прокси')
                with open("proxyes.txt", "w") as file:
                    file.write(str(int(datetime.datetime.now().timestamp())))
                    file.close()
                self.reload_proxy_list(self.proxy)
            else:
                while len(self.proxy) < 2:
                    print(f'процесс {os.getpid()} начал ожидать прокси лист')
                    time.sleep(10)
                    self.proxy = open("proxyes.txt", 'r').read().split("\n")
            try:
                # self.proxy = open("proxyes.txt", 'r').read().split("\n")
                self.proxy.pop()
                print(f'Длина прокси листа: {len(self.proxy)}')
                self.proxy_choice = self.proxy[1]
                self.proxy.remove(self.proxy_choice)
                with open('proxyes.txt', 'w') as fp:
                    for i in self.proxy:
                        fp.write(i + '\n')
                print(self.proxy_choice)
            except Exception as e:
                print(f'Процесс {os.getpid()}: не открывается файл с проксями...')
                continue
        print(self.proxy_choice)
        return self.proxy_choice

    def get_user_agent(self):
        self.user_agent = open("user_agent.txt", 'r').read().split("\n")
        self.user_agent.pop()
        self.user_agent_choice = choice(self.user_agent)
        return self.user_agent_choice

    def write_csv(self, object, name, city, phone, price, href_i):
        self.df.loc[0] = [object, name, city, phone, price, href_i]
        self.df.to_csv('data_13.csv', mode='a', encoding='utf-8', header=False, index=False, sep=";")
        return

    def get_url(self, url):
        self.url = url
        try:
            if self.url != '':
                self.new_driver()
                self.driver.get(self.url)
                self.get_page_from_site(self.url)
                return self.url
            else:
                self.read_page()
                self.write_page()
                self.url = f'https://market.kz/nedvizhimost/?page={self.page}&query%5Bdata%5D%5Bprice%5D%5Bfrom%5D=10000000'
                self.new_driver()
                self.driver.get(self.url)
                self.get_page_from_site(self.url)
                return

        except Exception as e:
            print("Не открылась ссылка...")
            self.check_page_in_fail_to_for_write(self.url)
            self.driver.close()
            return self.url


    def check_page_in_fail_to_for_write(self, url):
        sp = []
        page_ = open("result.txt", 'r').read().split('\n')
        for i in page_:
            sp.append(i)
        sp.pop()
        if url in sp:
            print("Не записываю URL он есть уже в листе")
            return
        print("Записываем URL в файл, его еще нет в листе")
        self.write_false_url(url)
        return

    def check_href_in_page_fail(self, href_list):
        sp = []
        res = []
        page_ = open("href_fin.txt", 'r').read().split('\n')

        for i in page_:
            z = i.replace('[', '').replace(']', '').replace('"', '').replace("'", '')
            l = z.replace(' ', '').split(',')
            for i in l:
                sp.append(i)
        for i in sp:
            if i in href_list:
                res.append(i)
        if len(res) != 0:
            self.write_href_fin(res)
            return

    def chek_fail_result_url_to_get(self):
        page_ = open("result.txt", 'r').read().split('\n')
        if len(page_) > 2:
            page_.pop()
            self.url = page_[0]
            page_.pop(0)
            with open('result.txt', 'w') as ff:
                for i in page_:
                    ff.write(str(i) + '\n')
            return self.url
        self.url = ''
        return self.url

    def reload_proxy_list(self, proxy):
        try:
            self.do_new_proxies_list()
            return

            while len(proxy) < 6:
                print(f'Процесс: {os.getpid()} ждет листа прокси')
                proxy = open("proxyes.txt", 'r').read().split("\n")
                print(f'У процесса {os.getpid()} длина прокси листа: {len(proxy)}')

        except Exception as e:
            print("Не смог прочитать файл с прокси")
            return
        print('Просто возвращаюсь из функии reload_proxy_list')
        return
    def do_new_proxies_list(self):
        par_pr_instance = Parse_proxy()
        par_pr_instance.run_parse_proxy()
        return


    def get_page_from_site(self, url):
        href_list = []
        fail_try = 0
        fail_try_href = 0
        while fail_try < 6:
            print(self.url)
            try:
                print("Жду открытия страницы...")
                print(self.proxy_choice)
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#goods > div:nth-child(1) > div > div.a-card__description > div.a-card__header > div.a-card__header-top > div.a-card__left-half > div.a-card__title > a")))
                while fail_try_href < 6:
                    try:
                        time.sleep(1)
                        self.driver.execute_script("window.stop()")
                        elements = self.driver.find_elements_by_class_name('ddl_product_link')
                        for el in elements:
                            href = el.get_attribute('href')
                            href_list.append(href)
                        print(f'Количество ссылок на странице: {len(href_list)}')
                        if len(href_list) > 0:
                            print('Передаю на сбор данных...')
                            self.get_data_from_page(href_list)
                            return
                        print("Ошибка сбора ссылок, запишу в fail...")
                        self.write_false_url(self.url)
                        self.driver.close()
                        return
                    except Exception as e:
                        if fail_try_href == 5:
                            print("Не смог собрать ссылки, запишу эту страницу в fail...")
                            self.write_false_url(self.url)
                            return
                        pass
                    fail_try_href += 1
                    print(f'Не смог собрать ссылки {fail_try_href} раз')
                return
            except Exception as e:
                if fail_try == 5:
                    print("Страница на загрузилась, записываю в файл адрес страницы...")
                    self.check_page_in_fail_to_for_write(self.url)
                    self.driver.close()
                    return
                fail_try += 1
                print(f'Не дождался открытия страницы {fail_try} раз...')
                continue

        return

    def get_data_from_page(self, href_list):
        false_parse = 0
        while len(href_list) and false_parse < 6:
            i = href_list.pop(0)
            print(f'Открываю ссылку: {i}')
            print(f'Длина списка ссылок: {len(href_list)}')
            self.driver.get(i)
            try:
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#content > div.container.flex > div.show-block-right > div.offer__sidebar-wr.hot-right-container > div.offer__sidebar-sticky > div > div.advert-contacts > div.advert-phones > button > p > span:nth-child(2)')))
                self.driver.find_element_by_css_selector('#content > div.container.flex > div.show-block-right > div.offer__sidebar-wr.hot-right-container > div.offer__sidebar-sticky > div > div.advert-contacts > div.advert-phones > button > p > span:nth-child(2)').click()
                try:
                    city = self.driver.find_element_by_css_selector('#content > div.container.flex > div.show-block-left > div.flex > div > div.show-header > div > div > a').text
                except:
                    city = "None"
                object = self.driver.find_element_by_css_selector('#content > div.container.flex > div.show-block-left > div.flex > div > div.show-header > h1').text
                name = self.driver.find_element_by_css_selector('#content > div.container.flex > div.show-block-right > div.offer__sidebar-wr.hot-right-container > div.offer__sidebar-sticky > div > div.advert-profile > div > div.advert-owner__name > a').text
                price = self.driver.find_element_by_css_selector('#content > div.container.flex > div.show-block-right > div.offer__sidebar-wr.hot-right-container > div.offer__sidebar-sticky > div > div.misc-fields.field-price > div > dl > dd').text
                time.sleep(1)
                phone = self.driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[2]/div[1]/div[2]/div/div[4]/div[1]/div[2]/dl/dd/div/span[1]').text

                self.write_csv(object, name, city, phone, price, i)
                print(f'записал в файл данные {phone}, {object}')
                time.sleep(1)

            except Exception as e:
                print(f'Не распарсил страницу, повторяю... попытка: {false_parse}')
                false_parse += 1
                href_list.append(i)
                continue

        if len(href_list) != 0 and false_parse == 5:
            print(f'Сделал {false_parse} попыток, закончил неудачно.')
            print(f'Записываю ссылки страниц для парсинга')
            self.check_href_in_page_fail(href_list)
            print(f'Закрываю драйвер...')
            self.close_driver()
            time.sleep(2)
            return

        print(f"Закончил парсить страницу")
        self.write_page()
        self.url = ''
        return self.run()

    def close_driver(self):
        self.driver.close()
        time.sleep(10)
        self.driver.quit()
        time.sleep(10)



    def run(self):
        # print(f'Процесс номер: {os.getpid()} страница: {self.read_page()}')
        while int(self.read_page()) < 2800:
            self.chek_fail_result_url_to_get()
            self.proxy_choice = ''
            try:
                print(len(self.proxy))
            except:
                print("Еще нет списка прокси")
            try:
                if self.url != '':
                    self.get_url(self.url)
                else:
                    self.get_url('')
            except Exception as e:
                print("Перезапуск заново....")
                continue
        print("Закончил все превсе...")
        return

if __name__ == '__main__':
    # pp = P()
    # pp.run()


    procs = []
    for _ in range(os.cpu_count()):
        proc = Process(target=P().run, args=())
        procs.append(proc)
        time.sleep(random())
        proc.start()

    for _ in procs:
        _.join()







