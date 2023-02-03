from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
import csv

with open('res.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([
        'Клиент', 'Номер Клиента', 'Няня', 'Цена', 'Время', 'Адрес', 'Статус', 'Дата создание'])

def parse_pp():
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1366x768')

    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(5)
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

    needeedpages = int(input('Введите количество страниц: '))

    try:
        browser.find_element(By.ID, "login-from_email").click()
        browser.find_element(By.ID, "login-from_email").send_keys(name)
        browser.find_element(By.ID, "login-from_password").click()
        browser.find_element(By.ID, "login-from_password").send_keys(passw)
        browser.find_element(By.CLASS_NAME, "ant-btn").click()
        browser.find_element(By.XPATH, "//a[contains(@href,'/order')]").click()
        
        pagen_find = browser.find_element(By.XPATH, "//ul[@class = 'ant-pagination ant-table-pagination ant-table-pagination-right']/li[8]/a")
        pagen = int(pagen_find.text)

        #Ссылка на элемент
        path_link_cli = str("//*[@class= 'ant-table-tbody']/tr/td[1]/a")

        path_names_bbs = str("//*[@class= 'ant-table-tbody']/tr/td[2]")
        path_link_bbs = str("//*[@class= 'ant-table-tbody']/tr/td[2]/a")

        path_cost = str("//*[@class= 'ant-table-tbody']/tr/td[3]/span")

        path_ToC = str("//*[@class= 'ant-table-tbody']/tr/td[4]/span")

        path_street = str("//*[@class= 'ant-table-tbody']/tr/td[5]")

        path_status = str("//*[@class= 'ant-table-tbody']/tr/td[6]/span")

        path_DoC = str("//*[@class= 'ant-table-tbody']/tr/td[7]/span")

        path_next_button_for3pages = str("//li[9]/button/span[1]")
        path_next_button_for4 = str("//li[10]/button/span[1]")
        path_next_button_ok = str("//li[11]/button/span[1]")
        #Ссылка на элемент

#Словари для принта в эксель
        cli_full=[]
        names_cli = []
        urls_cli = []
        cli_phone=[]
        bbs_full=[]
        urls_bbs = []
        links_urls_bbs =[]
        cost =[]
        ToC =[]
        address=[]
        status=[]
        DoC=[]

        current_page = 1

        active_page = 0
#Словари для принта в эксель
        while(active_page != needeedpages):


            #Поиск элемента
            links_cli = browser.find_elements(By.XPATH, path_link_cli)
            names_bbs = browser.find_elements(By.XPATH, path_names_bbs)
            links_bbs = browser.find_elements(By.XPATH, path_link_bbs)
            links_cost = browser.find_elements(By.XPATH, path_cost)
            links_ToC = browser.find_elements(By.XPATH, path_ToC)
            links_street = browser.find_elements(By.XPATH, path_street)
            links_status = browser.find_elements(By.XPATH, path_status)
            links_DoC = browser.find_elements(By.XPATH, path_DoC)


            if current_page < 4:
                next_button_for3pages = browser.find_element(By.XPATH, path_next_button_for3pages)
            elif current_page == 4:
                next_button_for4 = browser.find_element(By.XPATH, path_next_button_for4)
            else:
                next_button_ok = browser.find_element(By.XPATH, path_next_button_ok)

            len_link_tabs = len(links_cli)
            #Поиск элемента

            for name_cli in links_cli:
                names_cli.append(name_cli.text)

            for url_cli in links_cli:
                urls_cli.append(url_cli.get_attribute('href'))

            cli_names = 0
            for cli_nme in range(0, len_link_tabs):
                cli_full.insert(cli_names, names_cli[cli_nme])
                cli_names +=1
               
            for url_bbs in names_bbs:
                urls_bbs.append(url_bbs.text)
            urls_bbs.remove('')
            len_names_tabs = len(urls_bbs)

            for link_bbs in links_bbs:
                links_urls_bbs.append(link_bbs.get_attribute('href'))
            bbs_names = 0

            for nme_bbs in range(0, len_names_tabs):
                bbs_full.insert(bbs_names, urls_bbs[nme_bbs])
                bbs_names +=1
            
            for link_cost in links_cost:
                cost.append(link_cost.text)

            for link_ToC in links_ToC:
                ToC.append(link_ToC.text)

            for link_address in links_street:
                address.append(link_address.text)
            address.remove('')

            for link_status in links_status:
                status.append(link_status.text)

            for link_DoC in links_DoC:
                DoC.append(link_DoC.text)

            for i in range(len(links_cli)):
                phone_link_switch = urls_cli[i]
                browser.execute_script("window.open('');")
                browser.switch_to.window(browser.window_handles[1])                
                browser.get(phone_link_switch)
                phone = browser.find_element(By.XPATH, "//tbody/tr/td[1]/span[1]/a")
                cli_phone.append(phone.text)
                browser.close()
                browser.switch_to.window(browser.window_handles[-1])
            if current_page < 4:
                next_button_for3pages.click()
            elif current_page == 4:
                next_button_for4.click()
            else:
                next_button_ok.click()
            print(f'Страница номер {current_page} проверена.')
            current_page += 1
            active_page += 1
    except Exception as e:
        print(e)
        

    for cli_full, cli_phone, urls_bbs, cost, ToC, address, status, DoC in zip(cli_full, cli_phone, urls_bbs, cost, ToC, address, status, DoC):
        flatten = cli_full, cli_phone, urls_bbs, cost, ToC, address, status, DoC
        file = open('res.csv', 'a', encoding='utf-8-sig', newline='')
        writer = csv.writer(file, delimiter=';')
        writer.writerow(flatten)
    file.close()
    print('Файл res.csv создан')

    browser.quit()

pp_result = parse_pp()
