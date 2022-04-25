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
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="processMessagesForm"]/div/input[1]'))
        )
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


def update_resolved(dom, queue_name, expected_value):
    # After reprocessing, the queue is added to 'res' list if it is completely reprocessed, otherwise to unres
    message_count = get_message_count()
    # print("After reprocessing: ", message_count)
    if message_count != expected_value:
        unres.append(dom)
        unres.append(queue_name)
        unres.append(message_count)
    elif int(message_count) == 0:
        res.append(dom)
        res.append(queue_name)
        res.append(message_count)


def messages_less_than_200(dom, queue_name):
    # for messages less than 200, select all and reprocess
    # time.sleep(5)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mon-content"]/span'))
        )
    finally:
        driver.find_element_by_xpath('//*[@id="messageIDHeader"]').click()
    message_count = get_message_count()
    reprocess_and_click_ok()
    # time.sleep(5)
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mon-content"]/div'))
        )
    finally:
        expected_value = message_count - int(driver.find_element_by_xpath("//*[@id='mon-content']/div").text.split()[0])
    message_count = get_message_count()
    print("Actual Value: ", message_count)
    print("Expected Value: ", expected_value)
    update_resolved(dom, queue_name, expected_value)


file = 'osb_config.ini'
config = ConfigParser()
config.read(file)

OSB_USERNAME = config['osb_credentials']['username']
OSB_PASSWORD = config['osb_credentials']['password']

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"  # works before the page is fully loaded

country = sys.argv[1]  # country as commandline argument

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
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mon-content"]/li[1]/a'))
    )
    finally:
        driver.find_element_by_xpath('//*[@id="mon-content"]/li[1]/a').click()

domains = list((config['domains'][country]).split(','))
res = []
unres = []

message_count = 0
for dom in domains:
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.LINK_TEXT, dom))
    )
    finally:
        print(dom)
        driver.find_element_by_link_text(dom).click()
    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mon-content"]/span'))
    )
    finally:
        deadletter_xpath = '//*[@id="mon-content"]/table[2]//*[text()="Deadletter"]'
    messages_count_xpath = deadletter_xpath + '//following-sibling::td[6]/a'  # only gives the deadletters with messages in them
    message_count_elements = driver.find_elements_by_xpath(messages_count_xpath)
    queue_name_xpath = messages_count_xpath + '/ancestor::td/preceding-sibling::td[4]'
    queue_name_elements = driver.find_elements_by_xpath(queue_name_xpath)
    length_message_count = len(message_count_elements)

    for _ in range(length_message_count):
        # reacquiring the elements as they are detach from dom once the page is reloaded
        driver.refresh()
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="mon-content"]/span'))
            )
        finally:
            message_count_elements = driver.find_elements_by_xpath(messages_count_xpath)
        queue_name_elements = driver.find_elements_by_xpath(queue_name_xpath)
        queue_name = ''
        index = 0
        for name in queue_name_elements:
            queue_name = name.text
            # checking if the queue is already verified and not reprocessed
            if queue_name in unres:
                index += 1
                print(queue_name, ' exists in unres')
            elif queue_name in res:
                print(queue_name, " exists in res. Adding it to unres")
                ind = res.index(queue_name)
                print(ind)
                print('current res: ', res)
                print('current unres: ', unres)
                res.pop(ind+1)
                qcnt = int(message_count_elements[index].text)
                qnm = res.pop(ind)
                dmn = res.pop(ind-1)
                print(dmn, qnm, qcnt)
                unres.append(dmn)
                unres.append(qnm)
                unres.append(qcnt)
                print('new res: ', res)
                print('new unres: ', unres)
                index += 1
            else:
                break
        message = message_count_elements[index]
        count = int(message.text)
        print(queue_name, count)
        if queue_name == 'vmupdate-deadletter.esb.central.queue':
            continue
        message.click()
        # time.sleep(10)
        if count <= 200:
            try:
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="mon-content"]/span'))
                )
            finally:
                messages_less_than_200(dom, queue_name)
        else:
            message_count = get_message_count()
            while message_count > 200:
                if message_count > 1000:
                    max = 100
                    time.sleep(60)
                else:
                    try:
                        WebDriverWait(driver, 120).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="mon-content"]/span'))
                        )
                    finally:
                        message_count = get_message_count()
                        max = 200
                checkbox_elements_xpath = '//*[@id="processMessagesForm"]/span/table/tbody/tr/td[contains(@class, "mon-info")][1]/input[2]'
                checkbox_elements = driver.find_elements_by_xpath(checkbox_elements_xpath)
                # selecting max messages 
                for i in range(max):
                    checkbox_elements[i].click()
                reprocess_and_click_ok()
                # obtaining number of messages reprocessed from the display text
                try:
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, "//*[@id='mon-content']/div"))
                    )
                finally:
                    expected_value = message_count - int(
                    driver.find_element_by_xpath("//*[@id='mon-content']/div").text.split()[0])
                message_count = get_message_count()
                print("Actual Value: ", message_count)
                print("Expected Value: ", expected_value)
                if message_count != expected_value:
                    unres.append(dom)
                    unres.append(queue_name)
                    unres.append(message_count)
                    break
            else:
                # remaining messages less than 200
                messages_less_than_200(dom, queue_name)
        # time.sleep(10)
        try:
            WebDriverWait(driver, 60).until(
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
    # time.sleep(30)

print("Reprocessed: ")
print(res)
print("="*100)
print("Not Reprocessed: ")
print(unres)
driver.quit()