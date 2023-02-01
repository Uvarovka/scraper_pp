from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import time
from bs4 import BeautifulSoup
import requests
import lxml

def parse_pp():
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("detach", True)

    browser = webdriver.Chrome(options=chrome_options)

    stealth(browser,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    browser.get('https://podprismotrom-ykt.ru/login')  # Открываем сайт

    name='info@itkitchen.su'
    passw='123123'

    try:
        time.sleep(2)
        browser.find_element(By.ID, "login-from_email").click()
        time.sleep(1)
        browser.find_element(By.ID, "login-from_email").send_keys(name)
        time.sleep(1)
        browser.find_element(By.ID, "login-from_password").click()
        time.sleep(1)
        browser.find_element(By.ID, "login-from_password").send_keys(passw)
        time.sleep(1)
        browser.find_element(By.CLASS_NAME, "ant-btn").click()
        time.sleep(5)
        browser.find_element(By.XPATH, "//a[contains(@href,'/order')]").click()
        time.sleep(5)

        pagen = browser.find_element(By.XPATH, "//ul[@class = 'ant-pagination ant-table-pagination ant-table-pagination-right']/li[8]/a")
        print(int(pagen.text))

        #Ссылка на элемент
        path_link_cli = str("//*[@class= 'ant-table-tbody']/tr/td[1]/a")

        path_names_bbs = str("//*[@class= 'ant-table-tbody']/tr/td[2]")
        path_link_bbs = str("//*[@class= 'ant-table-tbody']/tr/td[2]/a")

        path_cost = str("//*[@class= 'ant-table-tbody']/tr/td[3]/span")

        path_ToC = str("//*[@class= 'ant-table-tbody']/tr/td[4]/span")

        path_street = str("//*[@class= 'ant-table-tbody']/tr/td[5]")

        path_status = str("//*[@class= 'ant-table-tbody']/tr/td[6]/span")

        path_DoC = str("//*[@class= 'ant-table-tbody']/tr/td[7]/span")
        #Ссылка на элемент

        #Поиск элемента
        links_cli = browser.find_elements(By.XPATH, path_link_cli)
        names_bbs = browser.find_elements(By.XPATH, path_names_bbs)
        links_bbs = browser.find_elements(By.XPATH, path_link_bbs)
        links_cost = browser.find_elements(By.XPATH, path_cost)
        links_ToC = browser.find_elements(By.XPATH, path_ToC)
        links_street = browser.find_elements(By.XPATH, path_street)
        links_status = browser.find_elements(By.XPATH, path_status)
        links_DoC = browser.find_elements(By.XPATH, path_DoC)
        #Поиск элемента

        orig_link = browser.current_window_handle

        time.sleep(5)
        len_link_tabs = len(links_cli)
        len_names_tabs = len(names_bbs)

#Словари для принта в эксель
        names_cli = []
        urls_cli = []
        cli_phone=[]
        urls_bbs = []
        links_urls_bbs =[]
        cost =[]
        ToC =[]
        address=[]
        status=[]
        DoC=[]
        cli_i_num=0

#Словари для принта в эксель


        for name_cli in links_cli:
            names_cli.append(name_cli.text)
        print(names_cli)

        for url_cli in links_cli:
            urls_cli.append(url_cli.get_attribute('href'))
        print(urls_cli)
        print(len(urls_cli))
        print(urls_cli[cli_i_num])
        for url_bbs in names_bbs:
            urls_bbs.append(url_bbs.text)
        urls_bbs.pop(0)

        print(str(urls_bbs))
        print(len(urls_bbs))

        for link_bbs in links_bbs:
            links_urls_bbs.append(link_bbs.get_attribute('href'))
        print(str(links_urls_bbs))
        print(len(links_urls_bbs))


        for cli_i in links_cli:
            time.sleep(2)
            browser.switch_to.new_window('urls_cli[cli_i_num]')
            path_phone = str("//td/span/a")
            phone = browser.find_elements(By.XPATH, path_phone)
            cli_phone.append(cli_i.text)
            print('zaebisya')
            browser.close()
            browser.switch_to.window(orig_link)
            cli_i_num+=1
            time.sleep(2)
        print(cli_phone)

        # y = 1
        # for i in range(0, len_names_tabs):
        #     data.insert(y, urls_cli[i])
        #     y +=2
        # if data == []:
        #     pp_array = ['Ошибка словарь пустой']
        # else:
        #     pp_array = data

    except Exception as e:
        print(e)
        pp_array = ['Ошибка']

    time.sleep(2)

    browser.close()

    #print(pp_array)
    return pp_array

pp_result = parse_pp()
