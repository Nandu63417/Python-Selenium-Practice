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

def reprocess_and_click_ok():
    # clicks the reprocess button in the queue
    try:
        time.sleep(5)
    finally:
        driver.find_element_by_xpath('//*[@id="processMessagesForm"]/div/input[1]').click()
    alert_obj = driver.switch_to.alert
    alert_obj.accept()
    time.sleep(5)


def get_message_count():
    # gets the message count from the queue
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="processMessagesForm"]/div'))
        )
    finally:
        s = driver.find_element_by_xpath('//*[@id="processMessagesForm"]/div').text
    return int(re.findall('\d+', s)[0])



def messages_less_than_200(queue_name):
    # for messages less than 200, select all and reprocess
    # time.sleep(5)
    try:
        time.sleep(15)
    finally:
        driver.find_element_by_xpath('//*[@id="messageIDHeader"]').click()
    message_count = get_message_count()
    reprocess_and_click_ok()
    # time.sleep(5)
    try:
        time.sleep(15)
    finally:
        expected_value = message_count - int(driver.find_element_by_xpath("//*[@id='mon-content']/div").text.split()[0])
    message_count = get_message_count()
    print("Actual Value: ", message_count)
    print("Expected Value: ", expected_value)

file = 'osb_config.ini'
config = ConfigParser()
config.read(file)

OSB_USERNAME = config['osb_credentials']['username']
OSB_PASSWORD = config['osb_credentials']['password']

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"  # works before the page is fully loaded

driver = webdriver.Chrome(desired_capabilities=caps, executable_path=config['urls']['driver_path'])
driver.maximize_window()

url = "https://qa-osb-monitor.lifetouch.net/osb-monitor/QA11g/OneLab/bulkfulfillment-v2-deadletter.esb.central.queue"

driver.get(url)

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))
    )
finally:
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(OSB_USERNAME)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(OSB_PASSWORD)
    driver.find_element_by_xpath('//*[@id="submit"]').click()

# try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//*[@id="mon-content"]/li[2]/a'))
#     )
# finally:
#     driver.find_element_by_xpath('//*[@id="mon-content"]/li[2]/a').click()

try:
        # WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="mon-content"]/span'))
    # )
    time.sleep(15)
finally:
    deadletter_xpath = '//*[@id="mon-content"]/table[1]/tbody/tr[2]/td[1]'
messages_count_xpath = deadletter_xpath + '//following-sibling::td[6]/a'  # only gives the deadletters with messages in them
message_count_elements = driver.find_elements_by_xpath(messages_count_xpath)
queue_name_xpath = messages_count_xpath + '/ancestor::td/preceding-sibling::td[4]'
queue_name_elements = driver.find_elements_by_xpath(queue_name_xpath)
length_message_count = len(message_count_elements) 
print(queue_name_elements)   

for _ in range(length_message_count):
    # reacquiring the elements as they are detach from dom once the page is reloaded
    driver.refresh()
    try:
        time.sleep(15)
    finally:
        message_count_elements = driver.find_elements_by_xpath(messages_count_xpath)
    queue_name_elements = driver.find_elements_by_xpath(queue_name_xpath)
    queue_name = ''
    index = 0
    for name in queue_name_elements:
        queue_name = name.text
    message = message_count_elements[index]
    count = int(message.text)
    print(queue_name, count)
    # if queue_name == 'boc-createbulkorder-deadletter.esb.central.queue':
    #     continue
    message.click()
    # time.sleep(10)
    if count <= 200:
        try:
            time.sleep(15)
        finally:
            messages_less_than_200(queue_name)
    else:
        message_count = get_message_count()
        print("Initial Message count: ", message_count)
        while message_count > 200:
            if message_count > 1000:
                max = 100
                time.sleep(15)
            else:
                try:
                    time.sleep(10)
                finally:
                    message_count = get_message_count()
                    max = 200
            checkbox_elements_xpath = '//*[@id="processMessagesForm"]/span/table/tbody/tr/td[contains(@class, "mon-info")][1]/input[2]'
            checkbox_elements = driver.find_elements_by_xpath(checkbox_elements_xpath)
            print("loaded checkboxes count: ", len(checkbox_elements))
            if len(checkbox_elements) < max:
                max = len(checkbox_elements)
            print(max)
            # selecting max messages 
            for i in range(max):
                checkbox_elements[i].click()
                # time.sleep(1)
            reprocess_and_click_ok()
            # obtaining number of messages reprocessed from the display text
            try:
                WebDriverWait(driver, 300).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="processMessagesForm"]/div'))
                )
            finally:
                expected_value = message_count - int(
                driver.find_element_by_xpath("//*[@id='mon-content']/div").text.split()[0])
            message_count = get_message_count()
            print("Actual Value: ", message_count)
            print("Expected Value: ", expected_value)
        else:
            # remaining messages less than 200
            messages_less_than_200(queue_name)
    # time.sleep(10)