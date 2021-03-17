from selenium import webdriver
from random import choice
import time


class Parse_proxy():
    def __init__(self):
        self.user_agent = open("user_agent.txt", 'r').read().split("\n")
        self.user_agent_choice = choice(self.user_agent)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        # options.add_argument('--proxy-server=%s' % proxy_choice)
        options.add_argument('--user-agent=%s' % self.user_agent_choice)
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
        self.url = "https://hidemy.name/ru/proxy-list/?maxtime=1500&type=s#list"
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)


    def get_data(self):
        ip_addr = 1
        port_addr = 1
        ip_addr_2 = 1
        port_addr_2 = 2

        list_proxies = []

        try:
            while True:
                element = self.driver.find_elements_by_xpath(f'/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[{ip_addr}]/td[{ip_addr_2}]')[0].text
                element_2 = self.driver.find_elements_by_xpath(f'/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[{port_addr}]/td[{port_addr_2}]')[0].text
                speed = self.driver.find_elements_by_xpath(f'/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[{ip_addr}]/td[4]/div/p')[0].text
                sock = element + ":" + element_2
                try:
                    speed_socket = int(speed[0:4])
                    if speed_socket < 1500:
                        list_proxies.append(sock)
                    else:
                        pass
                except Exception as e:
                    print(e)

                ip_addr += 1
                port_addr += 1

        except Exception as e:
            print(e)

        print(list_proxies)
        if len(list_proxies) < 2:
            self.get_data()
        with open("proxyes.txt", "w") as file:
            for line in list_proxies:
                file.write(line + '\n')

    def run_parse_proxy(self):
        self.get_data()
        self.driver.close()
        self.driver.quit()

if __name__ == '__main__':
    parser = Parse_proxy()
    parser.run_parse_proxy()

