import time
import smtplib
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

file = 'osb_config.ini'
config = ConfigParser()
config.read(file)

driver = webdriver.Chrome(config['urls']['driver_path'])
driver.maximize_window()

# driver.get("shutterfly.service-now.com/home.do")
# driver.get("https://shutterfly.service-now.com/nav_to.do?uri=%2Fhome.do")

print(driver.find_element_by_css_selector("#user_info_dropdown > div > span.user-name.hidden-xs.hidden-sm.hidden-md").text)
driver.find_element_by_css_selector("#buttons-group > button.btn.btn-icon.icon-refresh.navbar-btn").click()