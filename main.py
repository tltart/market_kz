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
        self.df = pd.DataFrame({'Object': [], 'Name': [], 'City': [], 'Phone': [], 'Price': []})
        self.capa = DesiredCapabilities.CHROME
        self.capa["pageLoadStrategy"] = "none"
        self.href_list = []
        self.href = None
        self.z = 0
        self.false_parse = 0
        self.read_page()

    def read_page(self):
        page_ = open("page.txt", 'r')
        self.page = int(page_.read())
        page_.close()
        return self.page

    def write_page(self):
        page_ = open("page.txt", 'w')
        page_.write(str(self.page + 1))
        page_.close()

    def new_driver(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--proxy-server=%s' % self.get_proxy())
        self.options.add_argument('--user-agent=%s' % self.get_user_agent())
        self.driver = webdriver.Chrome(desired_capabilities=self.capa, executable_path="chromedriver.exe", options=self.options)
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(self.driver, 5)
        # self.url = r'https://market.kz/nedvizhimost/?query[data][price][from]=10000000'


    def get_proxy(self):
        self.proxy = open("proxyes.txt", 'r').read().split("\n")
        self.proxy_choice = choice(self.proxy)
        return self.proxy_choice

    def get_user_agent(self):
        self.user_agent = open("user_agent.txt", 'r').read().split("\n")
        self.user_agent_choice = choice(self.user_agent)
        return self.user_agent_choice

    def write_csv(self, object, name, city, phone, price):
        self.df.loc[0] = [object, name, city, phone, price]
        self.df.to_csv('data_3.csv', mode='a', encoding='utf-8', header=False, index=False, sep=";")

    def get_url(self):
        try:
            self.url = f'https://market.kz/nedvizhimost/?page={self.page}&query%5Bdata%5D%5Bprice%5D%5Bfrom%5D=10000000'
            self.new_driver()
            self.driver.get(self.url)
            try:
                self.get_page_from_site()
            except Exception as e:
                print("Не найден элемент")

        except Exception as e:
            print(e)


    def get_page_from_site(self):
        try:
            print("Зашли в парсер")
            # print(self.)
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#goods > div:nth-child(1) > div > div.a-card__description > div.a-card__header > div.a-card__header-top > div.a-card__left-half > div.a-card__title > a")))
            try:
                time.sleep(1)
                self.driver.execute_script("window.stop()")
                elements = self.driver.find_elements_by_class_name('ddl_product_link')
                for el in elements:
                    self.href = el.get_attribute('href')
                    self.href_list.append(self.href)

                print(len(self.href_list))

            except Exception as e:
                # app_url_false = open("result.txt", "a")
                # app_url_false.write(self.href + "\n")
                # app_url_false.close()
                # self.close_driver()
                # print(e)
                pass

        except Exception as e:
            # Добавление пропущенных URL
            # self.close_driver()
            # app_url_false = open("result.txt", "a", encoding='cp1251')
            # app_url_false.write(self.url + "\n")
            # app_url_false.close()
            print("Не взял ссылку")
            # self.run()

    def get_data_from_page(self):
        # self.driver.get(self.href_list[0])

        while len(self.href_list):
            self.z += 1
            i = self.href_list.pop(0)
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

                self.write_csv(object, name, city, phone, price)
                # print(f'Объект: {object}')
                # print(f'Продавец: {name}')
                # print(f'Стоимость : {price}')
                # print(f'Город: {city}')
                print(f'Телефон: {phone}')
                time.sleep(1)

                self.driver.get(self.url)

            except Exception as e:
                print(e)
                self.false_parse += 1
                self.href_list.append(self.href)

        if self.z == 0 and self.false_parse > 50:
            self.close_driver()

            # return
            time.sleep(3)
            parse_new_proxy = Parse_proxy()
            parse_new_proxy.run_parse_proxy()
        if self.z == 0:
            self.close_driver()
            time.sleep(3)
            self.get_url()
            self.get_data_from_page()
        print("Закончили...")
        self.z = 0
        self.read_page()
        self.write_page()
        self.new_page_parse()

    def new_page_parse(self):
        self.get_url()
        self.get_data_from_page()

    def run(self):
        self.read_page()
        self.write_page()
        print(self.read_page())
        self.get_url()
        self.get_data_from_page()
        # self.write_csv()
        print(type(self.page))

    def close_driver(self):
        self.driver.close()
        self.driver.quit()

# def run_proc():
#     while pp.read_page() < 3000:
#         if len(procs) < 15:
#             tt = 15 - int(len(procs))
#             for _ in range(tt):
#                 proc = Process(target=P().run, args=())
#                 procs.append(proc)
#                 proc.start()
#             for proc in procs:
#                 proc.join()


def run_pr():
    for _ in range(15):
        proc = Process(target=P().run, args=())
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    while pp.read_page() < 3000:
        for proc in procs:
            if proc.is_alive():
                pass
            else:
                proc = Process(target=P().run, args=())
                procs.append(proc)
                proc.start()

if __name__ == '__main__':
    pp = P()

    procs = []
    for _ in range(15):
        proc = Process(target=P().run, args=())
        procs.append(proc)
        proc.start()

    # for proc in procs:
    #     proc.join()

    while pp.read_page() < 3000:
        for proc in procs:
            if proc.is_alive():
                pass
            else:
                proc = Process(target=P().run, args=())
                procs.append(proc)
                proc.start()

                # proc.join()






