from selenium import webdriver
from random import choice
import datetime
import time

# list_proxy_main = []

class Parse_proxy():
    def __init__(self):
        self.url = "https://hidemy.name/ru/proxy-list/?maxtime=1500&type=s#list"
        self.list_proxies = []
        self.list_proxy_main = open("proxy_for_proxy.txt", 'r').read().split("\n")
        self.list_proxy_main.pop(0)

    def get_proxy(self):
        self.proxy_choice = choice(self.list_proxy_main)
        return self.proxy_choice

    def new_driver(self):
        user_agent = open("user_agent.txt", 'r').read().split("\n")
        user_agent_choice = choice(user_agent)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--proxy-server=%s' % self.get_proxy())
        options.add_argument('--user-agent=%s' % user_agent_choice)
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
        self.driver.implicitly_wait(10)
        try:
            self.driver.get(self.url)
        except Exception as e:
            print("Ошибка с драйвером")
            self.driver.close()
            self.driver.quit()
            time.sleep(3)
            self.new_driver()
            return


    def get_data(self):
        self.new_driver()
        ip_addr = 1
        port_addr = 1
        ip_addr_2 = 1
        port_addr_2 = 2

        self.list_proxies = []
        i = 0
        print(self.proxy_choice)
        print(self.url)
        while True:
            try:
                element = self.driver.find_elements_by_xpath(f'/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[{ip_addr}]/td[{ip_addr_2}]')[0].text
                element_2 = self.driver.find_elements_by_xpath(f'/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[{port_addr}]/td[{port_addr_2}]')[0].text
                speed = self.driver.find_elements_by_xpath(f'/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[{ip_addr}]/td[4]/div/p')[0].text
                sock = element + ":" + element_2
                try:
                    speed_socket = int(speed[0:4])
                    if speed_socket < 1500:
                        self.list_proxies.append(sock)
                        print(sock)
                    else:
                        pass
                except Exception as e:
                    i += 1
                    print(e)

                port_addr += 1
                ip_addr += 1

            except Exception as e:
                print("Не получил доступ к сайту с прокси")
                return

    def write_data(self):
        print(self.list_proxies)
        while len(self.list_proxies) < 5:
            self.driver.close()
            self.driver.quit()
            time.sleep(3)
            self.get_data()

        self.list_proxies.insert(0, str(int(datetime.datetime.now().timestamp())))
        with open("proxyes.txt", "w") as file:
            for line in self.list_proxies:
                file.write(line + '\n')
        with open('proxy_for_proxy.txt', 'w') as ff:
            self.list_proxies.pop(0)
            for l in self.list_proxies:
                ff.write(l + '\n')
        return len(self.list_proxies)

    def run_parse_proxy(self):
        while len(self.list_proxies) < 5:
            self.get_data()
            self.write_data()
            self.driver.close()
            self.driver.quit()
        return
if __name__ == '__main__':
    parser = Parse_proxy()
    parser.run_parse_proxy()

