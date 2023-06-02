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

with open('res_bbs.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([
        'Няня', 'Номер няни', 'Фото профиля', 'Возраст', 'Обо мне', 'Мои преимущества', 'Кол-во выполненных заказов', ])

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

    name=input("Введите почту: ")
    passw=input("Введите пароль: ")
    needeedpages = int(input('Введите количество страниц: '))

    try:
        browser.find_element(By.ID, "login-from_email").click()
        browser.find_element(By.ID, "login-from_email").send_keys(name)
        browser.find_element(By.ID, "login-from_password").click()
        browser.find_element(By.ID, "login-from_password").send_keys(passw)
        browser.find_element(By.CLASS_NAME, "ant-btn").click()
        browser.find_element(By.XPATH, "//a[contains(@href,'/baby-sitter')]").click()

        #Ссылка на элемент
        path_names_bbs = str("//*[@class= 'ant-table-tbody']/tr/td[1]/a")

        path_phones_bbs = str("//*[@class= 'ant-table-tbody']/tr/td[2]/a")

        #Ссылка на элемент

        has_photo = "Есть фото профиля"
        hasnot_photo = "Нет фото профиля"
        old_date_splitter = '/'
        new_date_splitter = ' из '
#Словари для принта в эксель
        bbs_name = []
        urls_bbs = []
        bbs_phone= []
        ages= []
        abouts= []
        advantages= []
        bbs_orders= []
        photo_bbs = []
        current_page = 1
        active_page = 0
        phoneelem = 0
#Словари для принта в эксель
        while(active_page != needeedpages):


            #Поиск элемента
            names_bbs = browser.find_elements(By.XPATH, path_names_bbs)
            phones_bbs = browser.find_elements(By.XPATH, path_phones_bbs)

            #Поиск элемента

            # for name_bbs in names_bbs:
            #     bbs_name.append(name_bbs.text)

            for url_bbs in names_bbs:
                urls_bbs.append(url_bbs.get_attribute('href'))

            for phone_bbs in phones_bbs:
                bbs_phone.append(phone_bbs.text)

            for i in range(len(names_bbs)):
                phone_link_switch = urls_bbs[phoneelem]
                browser.execute_script("window.open('');")
                browser.switch_to.window(browser.window_handles[1])
                browser.get(phone_link_switch)
                full_names_bbs = browser.find_element(By.XPATH, "//tbody/tr[6]/td/span")
                age = browser.find_element(By.XPATH, "//tbody/tr[10]/td/span")
                about = browser.find_element(By.XPATH, "//tbody/tr[12]/td/span")
                advantage = browser.find_element(By.XPATH, "//tbody/tr[14]/td/span")
                orders = browser.find_element(By.XPATH, "//tbody/tr[16]/td/span")

                bbs_name.append(full_names_bbs.text)
                ages.append(age.text)
                abouts.append(about.text)
                advantages.append(advantage.text)
                fix_orders = orders.text.replace(old_date_splitter, new_date_splitter)
                bbs_orders.append(fix_orders)
                if browser.find_elements(By.XPATH, "//img[@src='/images/no-image.png']"):
                    photo_bbs.append(hasnot_photo)
                else:
                    photo_bbs.append(has_photo)
                browser.close()
                browser.switch_to.window(browser.window_handles[-1])
                phoneelem += 1

            print(f'Страница номер {current_page} проверена.')
            current_page += 1
            active_page += 1
            browser.get(f'https://podprismotrom-ykt.ru/baby-sitter?page={str(current_page)}')

    except Exception as e:
        print(e)


    for bbs_name, bbs_phone, photo_bbs, ages, abouts, advantages, bbs_orders in zip(bbs_name, bbs_phone, photo_bbs, ages, abouts, advantages, bbs_orders):
        flatten = bbs_name, bbs_phone, photo_bbs, ages, abouts, advantages, bbs_orders
        file = open('res_bbs.csv', 'a', encoding='utf-8-sig', newline='')
        writer = csv.writer(file, delimiter=';')
        writer.writerow(flatten)
    file.close()
    print('Файл res_bbs.csv создан')

    browser.quit()

pp_result = parse_pp()
