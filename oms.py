import time
import smtplib
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from outlookmail2 import send_email
import pyautogui
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def oms_us_uc():
    sub = "OMS_US_UC_Alerts"
    queues = list((config['queues']['uc']).split(','))

    driver.get(config['urls'][sub])
    driver.minimize_window()
    driver.set_page_load_timeout(60)
    driver.find_element_by_name("UserId").clear()
    driver.minimize_window()
    driver.find_element_by_name("UserId").send_keys(OMS_USERNAME)
    driver.find_element_by_name("Password").clear()
    driver.minimize_window()
    driver.find_element_by_name("Password").send_keys(OMS_PASSWORD)
    driver.find_element_by_name("btnLogin").click()
    driver.minimize_window()
    driver.set_page_load_timeout(60)

    flag = 0
    print(sub)
    body = ""
    for queue in queues:
        count = driver.find_element_by_xpath('//td/a[contains(text(),"' + queue + '")]/parent::td//following-sibling::td[2]').text
        # print(queue, count)
        if int(count) != 0:
            flag = 1
            body += queue + "   " + count + '\n'
    print(body)
    # msg = f"Subject: {sub}\n\n{body}"
    if(flag != 0):
        send_email(OUTLOOK_USERNAME, OUTLOOK_PASSWORD, recepients, sub, body)
        time.sleep(10)
    flag = 0
 

def oms_us_sr():
    sub = "OMS_US_SR_Alerts"
    queues = list((config['queues']['sr']).split(','))

    driver.get(config['urls'][sub])
    driver.minimize_window()
    driver.set_page_load_timeout(60)
    driver.find_element_by_name("UserId").clear()
    driver.minimize_window()
    driver.find_element_by_name("UserId").send_keys(OMS_USERNAME)
    driver.find_element_by_name("Password").clear()
    driver.minimize_window()
    driver.find_element_by_name("Password").send_keys(OMS_PASSWORD)
    driver.find_element_by_name("btnLogin").click()
    driver.minimize_window()
    driver.set_page_load_timeout(60)

    flag = 0
    print(sub)
    body = ""
    for queue in queues:
        count = driver.find_element_by_xpath('//td/a[contains(text(),"' + queue + '")]/parent::td//following-sibling::td[2]').text
        if int(count) != 0:
            flag = 1
            body += queue + "   " + count + '\n'
        driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
        driver.set_page_load_timeout(30)
    print(body)
    # msg = f"Subject: {sub}\n\n{body}"
    if(flag != 0):
        send_email(OUTLOOK_USERNAME, OUTLOOK_PASSWORD, recepients, sub, body)
        time.sleep(10)
    flag = 0


def oms_ca_uc():
    sub = "OMS_CA_UC_Alerts"
    queues = queues = list((config['queues']['uc']).split(','))

    driver.get(config['urls'][sub])
    driver.minimize_window()
    driver.set_page_load_timeout(60)
    driver.find_element_by_name("UserId").clear()
    driver.minimize_window()
    driver.find_element_by_name("UserId").send_keys(OMS_USERNAME)
    driver.find_element_by_name("Password").clear()
    driver.minimize_window()
    driver.find_element_by_name("Password").send_keys(OMS_PASSWORD)
    driver.find_element_by_name("btnLogin").click()
    driver.minimize_window()
    driver.set_page_load_timeout(180)

    flag = 0
    print(sub)
    body = ""
    for queue in queues:
        count = driver.find_element_by_xpath('//td/a[contains(text(),"' + queue + '")]/parent::td//following-sibling::td[2]').text
        # print(queue, count)
        if int(count) != 0:
            flag = 1
            body += queue + "   " + count + '\n'
        driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
        driver.set_page_load_timeout(30)
    print(body)
    # msg = f"Subject: {sub}\n\n{body}"
    if(flag != 0):
        send_email(OUTLOOK_USERNAME, OUTLOOK_PASSWORD, recepients, sub, body)
        time.sleep(10)
    flag = 0


def oms_ca_sr():
    sub = "OMS_CA_SR_Alerts"
    queues = queues = list((config['queues']['sr']).split(','))

    driver.get(config['urls'][sub])
    driver.minimize_window()
    driver.set_page_load_timeout(60)
    driver.find_element_by_name("UserId").clear()
    driver.minimize_window()
    driver.find_element_by_name("UserId").send_keys(OMS_USERNAME)
    driver.find_element_by_name("Password").clear()
    driver.minimize_window()
    driver.find_element_by_name("Password").send_keys(OMS_PASSWORD)
    driver.find_element_by_name("btnLogin").click()
    driver.minimize_window()
    driver.set_page_load_timeout(120)
    # time.sleep(30)
    
    flag = 0
    print(sub)
    body = ""
    for queue in queues:
        count = driver.find_element_by_xpath('//td/a[contains(text(),"' + queue + '")]/parent::td//following-sibling::td[2]').text
        if int(count) != 0:
            flag = 1
            body += queue + "   " + count + '\n'
        driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
        driver.set_page_load_timeout(30)
    print(body)
    # msg = f"Subject: {sub}\n\n{body}"
    if(flag != 0):
        send_email(OUTLOOK_USERNAME, OUTLOOK_PASSWORD, recepients, sub, body)
        time.sleep(10)
    flag = 0


file = 'oms_config.ini'
config = ConfigParser()
config.read(file)

OMS_USERNAME = config['oms_credentials']['username']
OMS_PASSWORD = config['oms_credentials']['password']

# GMAIL_USERNAME = config['gmail_credentials']['account']
# GMAIL_PASSWORD = config['gmail_credentials']['pwd']

OUTLOOK_USERNAME = config['outlook_credentials']['account']
OUTLOOK_PASSWORD = config['outlook_credentials']['pwd']
# print(OUTLOOK_USERNAME, OUTLOOK_PASSWORD)

# recepients = ['v-NKappaganthula@shutterfly.com', 'v-kalpana.joga@shutterfly.com', 'v-srija.prattipati@shutterfly.com']
recepients = list((config['outlook_credentials']['recepients']).split(','))

# options = webdriver.IeOptions()
# options.add_argument('headless')
# options.add_argument('--disable-gpu')
# # options.add_argument('-private')
# options.set_capability("silent", True)
# options.ignore_protected_mode_settings = True
# # options.force_create_process_api = True
# driver = webdriver.Ie(options=options)

driver = webdriver.Ie(config['urls']['driver_path'])
# driver.maximize_window()
driver.minimize_window()

# pyautogui.keyDown('alt') 
# pyautogui.keyDown('space') 
# pyautogui.press('n') 
# pyautogui.keyUp('space') 
# pyautogui.keyUp('alt') 

# driver.set_window_size(100,100)

# driver.find_element_by_css_selector("body").send_keys(Keys.PAGE_DOWN)

time.sleep(5)
while(1):
    # with smtplib.SMTP_SSL(config['gmail_credentials']['server'], 465) as smtp:
    #     smtp.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    oms_us_uc()
    oms_us_sr()
    oms_ca_uc()
    oms_ca_sr()
    
    time.sleep(1800)
    driver.refresh()