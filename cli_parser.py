from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
import csv

with open('res_cli.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([
        'Имя', 'Номер клиента', 'Рейтинг', 'Заказы', 'Дата создания', 'Город' ])

def parse_pp():
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1366x768')

    #browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
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

    name=input("Введите почту: ")
    passw=input("Введите пароль: ")
    needeedpages = int(input('Введите количество страниц: '))

    try:
        browser.find_element(By.ID, "login-from_email").click()
        browser.find_element(By.ID, "login-from_email").send_keys(name)
        browser.find_element(By.ID, "login-from_password").click()
        browser.find_element(By.ID, "login-from_password").send_keys(passw)
        browser.find_element(By.CLASS_NAME, "ant-btn").click()
        browser.find_element(By.XPATH, "//a[contains(@href,'/client')]").click()

        #Ссылка на элемент

        #Ссылка на элемент

#Словари для принта в эксель
        cli_names = []
        cli_urls = []
        cli_phones = []
        cli_ratings= []
        cli_orders= []
        cli_DOCs= []
        cli_city=[]

        active_page=0
        current_page = 1
#Словари для принта в эксель
        while(active_page != needeedpages):

            path_names_cli = str("//*[@class= 'ant-table-tbody']/tr/td[1]/a")
            path_phones_cli = str("//*[@class= 'ant-table-tbody']/tr/td[2]/a")
            path_rating_cli = str("//*[@class= 'ant-table-tbody']/tr/td[3]")
            path_orders_cli = str("//*[@class= 'ant-table-tbody']/tr/td[4]")
            path_DOC_cli = str("//*[@class= 'ant-table-tbody']/tr/td[5]")

            #Поиск элемента
            links_names_cli = browser.find_elements(By.XPATH, path_names_cli)
            links_phones_cli = browser.find_elements(By.XPATH, path_phones_cli)
            links_rating_cli = browser.find_elements(By.XPATH, path_rating_cli)
            links_orders_bbs = browser.find_elements(By.XPATH, path_orders_cli)
            links_DOC_bbs = browser.find_elements(By.XPATH, path_DOC_cli)
            phoneelem = 0
            #Поиск элемента

            # for name_bbs in names_bbs:
            #     bbs_name.append(name_bbs.text)

            for cli_name in links_names_cli:
                cli_names.append(cli_name.text)

            for cli_name in links_names_cli:
                cli_urls.append(cli_name.get_attribute('href'))

            for cli_phone in links_phones_cli:
                cli_phones.append(cli_phone.text)

            for cli_rating in links_rating_cli:
                cli_ratings.append(cli_rating.text)
            cli_ratings.remove('')
            for cli_order in links_orders_bbs:
                cli_orders.append(cli_order.text)
            cli_orders.remove('')

            for cli_DOC in links_DOC_bbs:
                cli_DOCs.append(cli_DOC.text)
            cli_DOCs.remove('')

            for i in range(len(links_names_cli)):
                phone_link_switch = cli_urls[phoneelem]
                browser.execute_script("window.open('');")
                browser.switch_to.window(browser.window_handles[1])
                browser.get(phone_link_switch)
                if browser.find_elements(By.XPATH, "//tbody/tr[10]/td/span"):
                    city = browser.find_element(By.XPATH, "//tbody/tr[10]/td/span")
                    cli_city.append(city.text)
                    browser.close()
                    browser.switch_to.window(browser.window_handles[-1])
                    phoneelem += 1
                else:
                    cli_city.append('')
                    browser.close()
                    browser.switch_to.window(browser.window_handles[-1])
                    phoneelem += 1

            print(f'Страница номер {current_page} проверена.')
            current_page += 1
            active_page += 1
            browser.get(f'https://podprismotrom-ykt.ru/client?page={str(current_page)}')

    except Exception as e:
        print(e)


    for cli_names, cli_phones, cli_ratings, cli_orders, cli_DOCs, cli_city in zip(cli_names, cli_phones, cli_ratings, cli_orders, cli_DOCs, cli_city):
        flatten = cli_names, cli_phones, cli_ratings, cli_orders, cli_DOCs, cli_city
        file = open('res_cli.csv', 'a', encoding='utf-8-sig', newline='')
        writer = csv.writer(file, delimiter=';')
        writer.writerow(flatten)
        file.close()
    print('Файл res_cli.csv создан')

    browser.quit()

pp_result = parse_pp()
