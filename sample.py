from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

driver1 = webdriver.Chrome('chromedriver.exe')
driver2 = webdriver.Ie('IEDriverServer.exe')

driver1.get('https://www.youtube.com')
time.sleep(5)
driver1.close()
time.sleep(10)
driver2.get('https://www.youtube.com')
time.sleep(5)
driver2.close()