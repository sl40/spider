from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.support.wait import WebDriverWait

import scrapy

display = Display(visible=0, size=(800, 600))
display.start()
browser = webdriver.Chrome('/Users/silin/yourdream/chromedriver', )
try:
    browser.get('http://fund.eastmoney.com/f10/jjjz_450002.html')
    # input = browser.find_element_by_id('search-input')
    # input.send_keys('国富')
    # input.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser,10)
    # wait.until(ES.presence_of_all_elements_located((By.ID, 'content_left')))
    for _ in browser.find_elements_by_xpath('//*[td]'):
        print(_.text)

finally:
    display.stop()
    browser.close()



