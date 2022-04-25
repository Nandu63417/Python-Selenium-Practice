import time
import os
import smtplib

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

OMS_USERNAME = os.environ.get('OSB_USERNAME')
OMS_PASSWORD = os.environ.get('OSB_PASSWORD')

# print(OSB_USERNAME, OSB_PASSWORD)

GMAIL_USERNAME = os.environ.get('GMAIL_USERNAME')
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')

# recepients = ['v-NKappaganthula@shutterfly.com', 'v-kalpana.joga@shutterfly.com', 'v-srija.prattipati@shutterfly.com']
recepients = ['v-NKappaganthula@shutterfly.com']

driver = webdriver.Ie("drivers\IEDriverServer.exe")
driver.maximize_window()


queues = ['SOLO Related Alerts']
sub = "OMS CA SR Alerts"

while(1):
    driver.get("https://oms-seniors-ca.lifetouch.net/yantra/console/login.jsp?ErrorMsg=Unsupported_Login_Procedure")
    driver.set_page_load_timeout(30)
    if driver.find_element_by_name("UserId").get_attribute("value"):
        driver.find_element_by_name("btnLogin").click()
        driver.set_page_load_timeout(30)
    else:
        driver.find_element_by_name("UserId").send_keys(OMS_USERNAME)
        driver.find_element_by_name("Password").send_keys(OMS_PASSWORD)
        driver.find_element_by_name("btnLogin").click()
        driver.set_page_load_timeout(30)
    flag = 0
    print(sub)
    body = ""

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(GMAIL_USERNAME, GMAIL_PASSWORD)

        for queue in queues:
            count = driver.find_element_by_xpath('//td/a[contains(text(),"' + queue + '")]/parent::td//following-sibling::td[2]').text
            # print(queue, count)
            if int(count) != 0:
                flag = 1
            body += queue + "   " + count + '\n'

            driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
            # driver.refresh()
        print(body)

        msg = f"Subject: {sub}\n\n{body}"

        if(flag != 0):
            smtp.sendmail(GMAIL_USERNAME, recepients, msg)
            print(flag)

        flag = 0

        driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
        # driver.refresh()
    # break
    time.sleep(1800)
    driver.refresh()
