from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import datetime

def xpath_element(xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        element = []
    return element


def real_time_price(stock_code):
    one_year_target = []
    volume = []
    url = 'https://ca.finance.yahoo.com/quote/' + stock_code + '?p=' + stock_code + '&.tsrc=fin-srch'
    driver.get(url)
    ######################################
    #       Price and Price Changes      #
    ######################################
    xpath = '//*[@id="quote-header-info"]/div[3]/div[1]/div'
    stock_price_info = xpath_element(xpath)
    if stock_price_info:
        stock_price_temp = stock_price_info.text.split()[0]
        if stock_price_temp.find('+') != -1:
            price = stock_price_temp.split('+')[0]
            try:
                change = '+' + stock_price_temp.split('+')[1] + ' ' + stock_price_info.text.split()[1]
            except IndexError:
                change = []
        elif stock_price_temp.find('-') != -1:
            price = stock_price_temp.split('-')[0]
            try:
                change = '-' + stock_price_temp.split('-')[1] + ' ' + stock_price_info.text.split()[1]
            except IndexError:
                change = []

        else:
            price, change = [], []
    else:
        price, change = [], []

    ######################################
    ######################################
    xpath = '//*[@id="quote-summary"]/div[1]'
    volume_temp = xpath_element(xpath)
    if volume_temp:
        for i, text in enumerate(volume_temp.text.split()):
            if text == 'Volume':
                volume = volume_temp.text.split()[i + 1]
                break
            else:
                volume = []
    else:
        volume = []

    ######################################
    ######################################

    xpath = '// *[ @ id = "quote-summary"] / div[2]'
    target_temp = xpath_element(xpath)
    if target_temp:
        for i, text in enumerate(target_temp.text.split()):
            if text == 'Est':
                if target_temp.text.split()[i + 1] != 'N/A':
                    one_year_target = target_temp.text.split()[i + 1]
                    break
                else:
                    one_year_target = []
            else:
                one_year_target = []

    latest_pattern = []
    return price, change, volume, latest_pattern, one_year_target


chrome_options = Options()
chrome_options.add_argument("--headless")  # disables Chrome window
chrome_options.add_argument('--no-sandbox')
service = Service(executable_path='C:\Program Files (x86)\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(options=chrome_options, service=service)

Stock = ['BRK-B']


interrupted = False
while True:
    info = []
    time_stamp = datetime.datetime.now()
    time_stamp = time_stamp.strftime("%Y-%m-%d %H:%M:%S")

    for StockCode in Stock:
        Price, Change, Volume, LatestPattern, OneYearTarget = real_time_price(StockCode)
        info.append(Price)
        info.extend([Change])
        info.extend([Volume])
        info.extend([LatestPattern])
        info.extend([OneYearTarget])

    col = [time_stamp]
    col.extend(info)
    df = pd.DataFrame(col)
    df = df.T

    df.to_csv(str(time_stamp[0:11]) + 'stock_data.csv', mode='a', header=None)
    print(col)

    if interrupted:
        print("Gotta go")
        break

driver.quit()
print('Driver Quit')
