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


from market_kz.parse_proxy import Parse_proxy

class P():
    def __init__(self):
        self.proxy = None
        self.proxy_choice = None
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
        self.proxy = open("proxyes.txt", 'r').read().split("\n")
        self.proxy_choice = choice(self.proxy)
        return self.proxy_choice

    def get_user_agent(self):
        self.user_agent = open("user_agent.txt", 'r').read().split("\n")
        self.user_agent_choice = choice(self.user_agent)
        return self.user_agent_choice

    def write_csv(self, object, name, city, phone, price, href_i):
        self.df.loc[0] = [object, name, city, phone, price, href_i]
        self.df.to_csv('data_4.csv', mode='a', encoding='utf-8', header=False, index=False, sep=";")
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
            self.write_false_url(self.url)




    def get_page_from_site(self, url):
        href_list = []
        fail_try = 0
        fail_try_href = 0
        while fail_try < 6:
            print(self.url)
            try:
                print("Страница открылась, собираю все ссылки...")
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
                    fail_try_href += 1
                    print(f'Не смог собрать ссылки {fail_try_href} раз')
            except Exception as e:
                if fail_try == 5:
                    print("Ссылки не смог взять, не дождался элемента, записываю...")
                    self.write_false_url(self.url)
                    self.driver.close()

                    return self.url
                fail_try += 1
                print(f'Не дождался элемента на странице {fail_try} раз')
                continue
        self.url = ''
        return self.url

    def get_data_from_page(self, href_list):
        false_parse = 0
        while len(href_list) and false_parse < 5:
            print("Первая ссылка пошла....")
            i = href_list.pop(0)
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

        if len(href_list) != 0 and false_parse <= 5:
            print(f'Сделал {false_parse} попыток, закончил неудачно.')
            print(f'Записываю ссылки страниц конечных')
            self.write_href_fin(href_list)
            print(f'Закрываю драйвер...')
            self.close_driver()
            time.sleep(2)
            return

        print(f"Закончил парсить страницу")
        self.write_page()
        self.run()

    def close_driver(self):
        self.driver.close()
        self.driver.quit()

    def run(self):
        print(f'Процесс номер: {os.getpid()} страница: {self.read_page()}')
        num_fail_get_page = 0
        while int(self.read_page()) < 2800:
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
    pp = P()
    pp.run()


    # procs = []
    # for _ in range(5):
    #     proc = Process(target=P().run, args=())
    #     procs.append(proc)
    #     proc.start()







