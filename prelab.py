import time
import smtplib
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from outlookmail2 import send_email
import pyautogui
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

file = 'osb_config.ini'
config = ConfigParser()
config.read(file)

PRELAB_USERNAME = config['osb_credentials']['username']
PRELAB_PASSWORD = config['osb_credentials']['password']

url = 'https://prelabmanagement.lifetouch.net/dashboard'

driver = webdriver.Chrome(config['urls']['driver_path'])
driver.maximize_window()

driver.get(url)

# driver.find_element_by_xpath("/html/body/div[3]/div[11]/div/button/span").click()
driver.find_element_by_css_selector("#cas > div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-draggable.ui-resizable > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button > span").click()
driver.find_element_by_css_selector("#username").send_keys(PRELAB_USERNAME)
driver.find_element_by_css_selector("#password").send_keys(PRELAB_PASSWORD)
driver.find_element_by_css_selector("#btnSubmit").click()

# driver.find_element_by_css_selector("body > app-root > div > div.main-panel > app-dashboard > div > div.ng-star-inserted > input:nth-child(18)")
# /html/body/app-root/div/div[2]/app-dashboard/div/div[2]/input[15]
# //*[@id="mat-tab-content-7-0"]/div/div/div/canvas
# driver.find_element_by_xpath('//*[@id="mat-tab-content-7-0"]/div/div/div/canvas')
# driver.set_page_load_timeout(120)
# try:
#     WebDriverWait(driver, 120).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, '#mat-tab-content-1-0 > div > div > div > canvas'))
#     )
# finally:          
#     print(driver.find_element_by_css_selector('#mat-tab-content-1-0 > div > div > div > canvas').tag_name)

try:
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'body > app-root > div > div.main-panel > app-dashboard > div > div.ng-star-inserted > input:nth-child(20)'))
    )
finally:          
    # print(driver.find_element_by_css_selector('body > app-root > div > div.main-panel > app-dashboard > div > div.ng-star-inserted > input:nth-child(20)').tag_name)
    for x in driver.find_elements_by_css_selector('body > app-root > div > div.main-panel > app-dashboard > div > div.ng-star-inserted > input'):
        # if x.get_attribute("name").find('BRT AUDIT CHECK') != -1 or x.get_attribute("name").find('SERVICE RETOUCH') != -1 or x.get_attribute("name").find('BRT EDIT CHECK') != -1:
        if x.get_attribute("name").find('BRT AUDIT CHECK') != -1:
            print(x.get_attribute("name"))
            x.click()
    # driver.find_element_by_css_selector('body > app-root > div > div.main-panel > app-dashboard > div > div.ng-star-inserted > input:nth-child(20)').click()