import time
import re
import sys
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date


def get_message_count():
    # gets the message count from the queue
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="processMessagesForm"]/div'))
        )
    finally:
        s = driver.find_element_by_xpath('//*[@id="processMessagesForm"]/div').text
    return int(re.findall('\d+', s)[0])


file = 'osb_config.ini'
config = ConfigParser()
config.read(file)

OSB_USERNAME = config['osb_credentials']['username']
OSB_PASSWORD = config['osb_credentials']['password']

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"  # works before the page is fully loaded

country = sys.argv[1]  # country as commandline argument
dom = sys.argv[2]
# LNSS11gProdSubjectMaster
queue = sys.argv[3]
# ybchoice-sync-qlab-sm-deadletter.muncie.queue

filename = queue + '_' + str(date.today())
fileobj = open('BackupMessages/' + filename+".txt","w")

driver = webdriver.Chrome(desired_capabilities=caps, executable_path=config['urls']['driver_path'])
driver.maximize_window()

if country:
    url = config['urls'][country]
else:
    exit()

driver.get(url + "login/auth;jsessionid=EC5B63AB3AAB2B0E2D58675885BB05E5")
# time.sleep(15)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))
    )
finally:
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(OSB_USERNAME)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(OSB_PASSWORD)
    driver.find_element_by_xpath('//*[@id="submit"]').click()

if country == 'us':
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mon-content"]/li[2]/a'))
    )
    finally:
        driver.find_element_by_xpath('//*[@id="mon-content"]/li[2]/a').click()
elif country == 'ca':
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mon-content"]/li[1]/a'))
    )
    finally:
        driver.find_element_by_xpath('//*[@id="mon-content"]/li[1]/a').click()

message_count = 0
try:
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.LINK_TEXT, dom))
)
finally:
    print(dom)
    driver.find_element_by_link_text(dom).click()
try:
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mon-content"]/span'))
)
finally:
    deadletter_xpath = '//*[@id="mon-content"]/table[2]//*[text()="Deadletter"]'
messages_count_xpath = deadletter_xpath + '//following-sibling::td[6]/a'  # only gives the deadletters with messages in them
message_count_elements = driver.find_elements_by_xpath(messages_count_xpath)
queue_name_xpath = messages_count_xpath + '/ancestor::td/preceding-sibling::td[4]'
queue_name_elements = driver.find_elements_by_xpath(queue_name_xpath)
queue_names = []
for q in queue_name_elements:
    queue_names.append(q.text)

queue_name = queue
try:
    print("Queue names: ", queue_names)
    # print(queue)
    index = queue_names.index(queue)
    # print(index)
except:
    print("Queue has no messages to backup")
    driver.quit()
    exit()
message = message_count_elements[index]
count = int(message.text)
print(queue_name, count)
message.click()
message_count = get_message_count()

try:
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mon-content"]/span'))
    )
finally:
    message_count = get_message_count()
# print(message_count)

# checkbox_elements_xpath = '//*[@id="processMessagesForm"]/span/table/tbody/tr/td[contains(@class, "mon-info")][1]'
backup_message_path = '//*[@id="processMessagesForm"]/span/table/tbody/tr/td[contains(@class, "mon-info")][2]/a'
backup_message_elements = driver.find_elements_by_xpath(backup_message_path)
print("loaded checkboxes count: ", len(backup_message_elements))

for i in range(len(backup_message_elements)):
    backup_message_path = '//*[@id="processMessagesForm"]/span/table/tbody/tr/td[contains(@class, "mon-info")][2]/a'
    backup_message_elements = driver.find_elements_by_xpath(backup_message_path)
    # time.sleep(5)
    print(i, len(backup_message_elements))
    backup_message_elements[i].click()
    time.sleep(3)
    # print(driver.find_element_by_css_selector('body > table').text)
    try:
        fileobj.writelines(driver.find_element_by_css_selector('body > table').text)
        # fileobj.writelines(driver.find_element_by_css_selector('body > table').text.encode('ascii', 'ignore'))
        fileobj.write('\n')
        # fileobj.writelines(driver.find_element_by_css_selector('#payload').text)
        fileobj.writelines(driver.find_element_by_css_selector('#payload').text.encode('ascii', 'ignore').decode('ascii'))
        fileobj.write('\n')
        fileobj.write("-"*100)
        fileobj.write('\n')
    except Exception as e:
        print(e)
        continue
    finally:
        driver.back()
        time.sleep(3)

try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mon-content"]/span'))
    )
finally:
    driver.get(url + "Prod11g/" + dom[11:])
    try:
        WebDriverWait(driver, 30).until(
            EC.url_to_be(url + "Prod11g/" + dom[11:])
        )
    finally:
        driver.refresh()
# time.sleep(25)
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mon-content"]/span'))
    )
finally:    
    driver.get(url + "Prod11g/")
    try:
        WebDriverWait(driver, 30).until(
            EC.url_to_be(url + "Prod11g/")
        )
    finally:
        driver.refresh()

fileobj.close()
driver.quit()