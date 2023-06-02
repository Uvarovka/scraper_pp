from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
import csv
import pandas as pd

with open("excel_transformer.py") as f:
    exec(f.read())

def extract_first_column_from_excel(filename):
    df = pd.read_excel(filename)
    first_column = df.iloc[:, 0].tolist()
    return first_column

filename = 'number_output.xlsx'
numbers = extract_first_column_from_excel(filename)
print(len(numbers))

def parse_numbers(numbers):
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1366x768')
    chrome_options.add_argument('start-maximized')
    #
    # browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=chrome_options)
    browser.implicitly_wait(5)
    stealth(browser,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    regions = []

    browser.get('https://www.spravportal.ru/Services/PhoneCodes/MobilePhoneInfo.aspx')
    for i in range(0,len(numbers)):
        browser.find_element(By.ID, "textNumDesktop").click()
        browser.find_element(By.ID, "textNumDesktop").send_keys(numbers[i])
        browser.find_element(By.ID, "ctl00_ctl00_cphMain_cphServiceMain_btnSearchDesktop").click()
        if browser.find_elements(By.XPATH, "//*[@class = 'form-group']/div[1]/strong[1]"):
            regions.append(browser.find_element(By.XPATH, "//*[@class = 'form-group']/div[1]/strong[1]").text)
        elif browser.find_elements(By.XPATH, "//*[@id = 'ctl00_ctl00_cphMain_cphServiceMain_WhoCallsPhoneCard_pnlPhoneNumber']"):
            regions.append('Плохой рейтинг на сайте')
            browser.get('https://www.spravportal.ru/Services/PhoneCodes/MobilePhoneInfo.aspx')
        else:
            regions.append('Нет информации')
        browser.find_element(By.ID, "textNumDesktop").clear()
    return regions
    browser.quit()

regions = parse_numbers(numbers)

df = pd.read_excel('number_output.xlsx')
df['Регион'] = regions
df.to_excel('number_output.xlsx', index=False)
