from selenium import webdriver
from random import choice
import time




user_agent = open("user_agent.txt", 'r').read().split("\n")
user_agent_choice = choice(user_agent)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
# options.add_argument('--proxy-server=%s' % proxy_choice)
options.add_argument('--user-agent=%s' % user_agent_choice)
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)

url = "https://hidemy.name/ru/proxy-list/?type=s#list"

driver.implicitly_wait(10)
driver.get(url)

time.sleep(5)

ip_addr = 1
port_addr = 1
ip_addr_2 = 1
port_addr_2 = 2

list_proxies = []

try:
    while True:
        element = driver.find_elements_by_xpath(f'/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[{ip_addr}]/td[{ip_addr_2}]')[0].text
        element_2 = driver.find_elements_by_xpath(f'/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[{port_addr}]/td[{port_addr_2}]')[0].text
        speed = driver.find_elements_by_xpath(f'/html/body/div[1]/div[4]/div/div[4]/table/tbody/tr[{ip_addr}]/td[4]/div/p')[0].text
        sock = element + ":" + element_2
        try:
            speed_socket = int(speed[0:4])
            if speed_socket < 1000:
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
with open("proxyes.txt", "w") as file:
    for line in list_proxies:
        file.write(line + '\n')

time.sleep(5)

driver.close()
driver.quit()
