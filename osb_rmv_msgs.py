import time
import re
import sys
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def reprocess_and_click_ok(i):
    print(i)
    # clicks the reprocess button in the queue
    driver.find_element_by_xpath('//*[@id="processMessagesForm"]/div/input[' + str(i) + ']').click()
    alert_obj = driver.switch_to.alert
    alert_obj.accept()
    time.sleep(20)


def get_message_count():
    # gets the message count from the queue
    s = driver.find_element_by_xpath('//*[@id="processMessagesForm"]/div').text
    return int(re.findall('\d+', s)[0])


def update_resolved(dom, queue_name, expected_value):
    # After reprocessing, the queue is added to 'res' list if it is completely reprocessed, otherwise to unres
    message_count = get_message_count()
    print("After reprocessing: ", message_count)
    if message_count != expected_value:
        unres.append(dom)
        unres.append(queue_name)
        unres.append(message_count)
    else:
        res.append(dom)
        res.append(queue_name)
        res.append(message_count)


def messages_less_than_200(dom, queue_name):
    # for messages less than 200, select all and reprocess
    driver.find_element_by_xpath('//*[@id="messageIDHeader"]').click()
    reprocess_and_click_ok(1)
    update_resolved(dom, queue_name, 0)


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
time.sleep(15)

driver.find_element_by_xpath('//*[@id="username"]').send_keys(OSB_USERNAME)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(OSB_PASSWORD)
driver.find_element_by_xpath('//*[@id="submit"]').click()
time.sleep(20)

if country == 'us':
    driver.find_element_by_xpath('//*[@id="mon-content"]/li[2]/a').click()
elif country == 'ca':
    driver.find_element_by_xpath('//*[@id="mon-content"]/li[1]/a').click()

time.sleep(20)
domains = ["LNSS11gProdSubjectMaster"]
res = []
unres = []

message_count = 0
for dom in domains:
    print(dom)
    driver.find_element_by_link_text(dom).click()
    time.sleep(15)
    deadletter_xpath = '//*[@id="mon-content"]/table[2]//*[text()="Deadletter"]'
    messages_count_xpath = deadletter_xpath + '//following-sibling::td[6]/a'  # only gives the deadletters with messages in them
    message_count_elements = driver.find_elements_by_xpath(messages_count_xpath)
    queue_name_xpath = messages_count_xpath + '/ancestor::td/preceding-sibling::td[4]'
    queue_name_elements = driver.find_elements_by_xpath(queue_name_xpath)
    length_message_count = len(message_count_elements)

    for _ in range(length_message_count):
        # reacquiring the elements as they are detach from dom once the page is reloaded
        message_count_elements = driver.find_elements_by_xpath(messages_count_xpath)
        queue_name_elements = driver.find_elements_by_xpath(queue_name_xpath)
        queue_name = ''
        index = 0
        for name in queue_name_elements:
            queue_name = name.text
            # checking if the queue is already verified and not reprocessed
            if queue_name in unres:
                index += 1
                print(queue_name, ' exists')
            else:
                break
        message = message_count_elements[index]
        count = int(message.text)
        print(queue_name, count)
        message.click()
        time.sleep(10)
        if count <= 200:
            messages_less_than_200(dom, queue_name)
        else:
            if queue_name == "ybchoice-sync-qlab-sm-deadletter.muncie.queue":
                rmv = 2
            message_count = get_message_count()
            while message_count > 200:
                time.sleep(10)
                max = 200
                if count > 1000:
                    max = 80
                    time.sleep(30)
                checkbox_elements_xpath = '//*[@id="processMessagesForm"]/span/table/tbody/tr/td[contains(@class, "mon-info")][1]'
                checkbox_elements = driver.find_elements_by_xpath(checkbox_elements_xpath)
                # selecting max messages 
                for i in range(max):
                    checkbox_elements[i].click()
                reprocess_and_click_ok(rmv)
                # obtaining number of messages reprocessed from the display text
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
        time.sleep(5)
        driver.get(url + "Prod11g/" + dom[11:])
        time.sleep(20)
    driver.get(url + "Prod11g/")
    time.sleep(20)

print("Reprocessed: ")
print(res)
print("===================================================================")
print("Not Reprocessed")
print(unres)
driver.quit()