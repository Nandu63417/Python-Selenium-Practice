import time
import smtplib
import xml.etree.ElementTree as ET
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

file = 'oms_config.ini'
config = ConfigParser()
config.read(file)

OMS_USERNAME = config['oms_credentials']['username']
OMS_PASSWORD = config['oms_credentials']['password']

GMAIL_USERNAME = config['gmail_credentials']['account']
GMAIL_PASSWORD = config['gmail_credentials']['pwd']

# recepients = ['v-NKappaganthula@shutterfly.com', 'v-kalpana.joga@shutterfly.com', 'v-srija.prattipati@shutterfly.com']
recepients = list((config['gmail_credentials']['recepients']).split(','))

driver = webdriver.Ie(config['urls']['driver_path'])
driver.maximize_window()
action = ActionChains(driver)

sub = "OMS_US_UC_Alerts"
# sub = "OMS_US_SR_Alerts"
# sub = "OMS_CA_UC_Alerts"
# sub = "OMS_CA_SR_Alerts"
queues = list((config['queues']['uc']).split(','))
# queues = list((config['queues']['sr']).split(','))

driver.get(config['urls'][sub])
driver.set_page_load_timeout(30)
driver.find_element_by_name("UserId").clear()
driver.find_element_by_name("UserId").send_keys(OMS_USERNAME)
driver.find_element_by_name("Password").clear()
driver.find_element_by_name("Password").send_keys(OMS_PASSWORD)
driver.find_element_by_name("btnLogin").click()
driver.set_page_load_timeout(30)
# time.sleep(10)

flag = 0
print(sub)
body = ""
for queue in queues:
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//td/a[contains(text(),"' + queue + '")]/parent::td//following-sibling::td[2]'))
        )
    finally:
        count = driver.find_element_by_xpath('//td/a[contains(text(),"' + queue + '")]/parent::td//following-sibling::td[2]').text
    # print(queue, count)
    if int(count) != 0:
        flag = 1
        body += queue + "   " + count + '\n'
print(body)

try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//td/a[contains(text(),"BOC Related Alerts")]/parent::td//following-sibling::td[2]'))
    )
finally:
    count = driver.find_element_by_xpath('//td/a[contains(text(),"BOC Related Alerts")]/parent::td//following-sibling::td[2]').text
if int(count) == 0:
    count = driver.find_element_by_xpath('//td/a[contains(text(),"MLT Related Alerts")]/parent::td//following-sibling::td[2]').text
    print('MLT Related Alerts', count)
    driver.find_element_by_link_text("MLT Related Alerts").click()
else:
    print('BOC Related Alerts', count)
    driver.find_element_by_link_text("BOC Related Alerts").click()

driver.set_page_load_timeout(30)
# time.sleep(5)

main_page = driver.current_window_handle
alert_page = ''
alert2_page = ''

def alert_type_satellite():
    global alert_page
    # global alert2_page
    main_page = driver.current_window_handle
    # time.sleep(5)
    # alert_link = driver.find_element_by_xpath("//DIV[starts-with(@id,'v_')]/TABLE/TBODY/TR/TD[2]/A")
    # action.click(alert_link)
    # action.perform()
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[starts-with(@id,'v_')]/table/tbody/tr[2]/td[6]"))
        )
    finally:
        print(driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr[2]/td[6]").text)
    driver.find_element_by_xpath("//DIV[starts-with(@id,'v_')]/TABLE/TBODY/TR/TD[2]/A").click()
    driver.set_page_load_timeout(60)
    # time.sleep(10)
    print(len(driver.window_handles))
    for handle in driver.window_handles:
        if handle != main_page:
            alert_page = handle
    driver.switch_to.window(alert_page)

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//frame[@id='yfcRootFrame']"))
        )
    finally:
        driver.switch_to.frame("yfcRootFrame")

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//tr[@class='evenrow']/td[3]/a"))
        )
    finally:
        driver.find_element_by_xpath("//tr[@class='evenrow']/td[3]/a").text
    driver.find_element_by_xpath("//tr[@class='evenrow']/td[3]/a").click()
    # time.sleep(5)
    print('main_page = ', main_page,'alert_page = ', alert_page, len(driver.window_handles))
    print('current_window_handle = ', driver.current_window_handle)
    for handle2 in driver.window_handles:
        print(handle2)
        if handle2 != alert_page and handle2 != main_page:
            alert2_page = handle2
    print(alert2_page)
    driver.switch_to.window(alert2_page)
    # time.sleep(5)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//frame[@id='yfcRootFrame']"))
        )
    finally:
        driver.switch_to.frame("yfcRootFrame")
    alert = ''
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[starts-with(@id, 'v_')]/table/tbody/tr/td/textarea"))
        )
    finally:
        alert_xml = driver.find_element_by_xpath("//div[starts-with(@id, 'v_')]/table/tbody/tr/td/textarea").text
    if alert_xml.find('Satellite Location is not yet defined in OMS') != -1:
        alert = 'Satellite Location is not yet defined in OMS'  
    print(alert)              

    driver.find_element_by_xpath("//table[@class='detailpagetitle1']/tbody/tr[@class='pagetitle2']/td[@class='detailpagetitle6']/input[@value='Close']").send_keys(Keys.ENTER)
    # driver.switch_to.default_content()
    driver.switch_to.window(alert_page)
    # time.sleep(5)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//frame[@id='yfcRootFrame']"))
        )
    finally:
        driver.switch_to.frame("yfcRootFrame")
    return alert


def go_next():
    driver.find_element_by_xpath("/HTML/BODY/FORM/TABLE/TBODY/TR[2]/TD/TABLE/TBODY/TR[1]/TD/DIV/TABLE/TBODY/TR/TD[3]/TABLE/TBODY/TR/TD[4]/A/IMG").click()

def reprocess():
    global alert_page
    global alert2_page
    for _ in range(int(count)):
        url = driver.current_url
        print(url)
        alert = alert_type_satellite()

        if alert != 'Satellite Location is not yet defined in OMS':
            driver.switch_to.default_content()
            driver.close()
            driver.switch_to.window(main_page)
            if int(count) == 1:
                # time.sleep(5)
                return
            go_next()
            # time.sleep(5)
            continue

        xml = driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr/td/textarea").text
        # print(xml)
        root = ET.fromstring(xml)

        shipTo = root.find('Extn')

        # for shipTo in root.find('Extn'):
        print(shipTo, len(shipTo), type(shipTo))
        # if len(shipTo) > 0:
        #     print(next(shipTo))
        if shipTo.attrib['ExtnShipOrdersTo'] == 'Satellite':
            shipTo.set('ExtnShipOrdersTo', 'Account')
        
        # for shipTo in root.find('Extn'):
        print('ExtnShipOrdersTo = ',shipTo.attrib['ExtnShipOrdersTo'])
    
        new_xml = ET.tostring(root, encoding = 'unicode')
        new_xml = str(new_xml)
        new_xml = new_xml.replace('ns0','It')
        # print(xml, type(xml))
        # print(new_xml, type(new_xml))

        print(driver.find_element_by_xpath("//tr[@class='evenrow']/td[6]").text)
        
        if driver.find_element_by_xpath("//tr[@class='evenrow']/td[6]").text == 'Initial':
            driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr/td/textarea").clear()
            driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr/td/textarea").send_keys(new_xml)
        
            driver.find_element_by_xpath("//table[@class='detailpagetitle1']/tbody/tr[@class='pagetitle2']/td[@class='detailpagetitle6']/input[@value='Save']").send_keys(Keys.ENTER)
            # time.sleep(30) 

        driver.switch_to.window(alert_page)
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//frame[@id='yfcRootFrame']"))
            )
        finally:
            driver.switch_to.frame("yfcRootFrame")

        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//tr[@class='evenrow']/td[6]"))
            )
        finally:
            print(driver.find_element_by_xpath("//tr[@class='evenrow']/td[6]").text)
        if driver.find_element_by_xpath("//tr[@class='evenrow']/td[6]").text == 'Saved':
            print(driver.find_element_by_xpath("//tr[@class='evenrow']/td[1]/a").text)
            driver.find_element_by_xpath("//tr[@class='evenrow']/td[1]/a").click()
            time.sleep(5)

            print('main_page = ', main_page)
            print('alert_page = ', alert_page)
            print('alert2_page = ', alert2_page)
            print(len(driver.window_handles))
            print('current_window_handle = ', driver.current_window_handle)
            for handle2 in driver.window_handles:
                print(handle2)
                if handle2 != alert_page and handle2 != main_page:
                    alert2_page = handle2
            print(alert2_page)
            driver.switch_to.window(alert2_page)
            # time.sleep(5)
            try:    
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//frame[@id='yfcRootFrame']"))
                )
            finally:
                driver.switch_to.frame("yfcRootFrame")    
            # print(driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr/td/textarea").text)

            print(driver.find_element_by_xpath("//table[@class='anchor']/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]").text)
            driver.find_element_by_xpath("//table[@class='anchor']/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]").click()
            # time.sleep(20)

            # driver.find_element_by_xpath("//table[@class='detailpagetitle1']/tbody/tr[@class='pagetitle2']/td[@class='detailpagetitle6']/input[@value='Close']").send_keys(Keys.ENTER)
            print('main page: ', main_page)
            print('alert page: ', alert_page)
            print('alert2 page: ', alert2_page)
            print('current_window_handle: ', driver.current_window_handle)
            driver.close()
            # driver.find_element_by_xpath("//table[@class='detailpagetitle1']/tbody/tr[@class='pagetitle2']/td[@class='detailpagetitle6']/input[@value='Close']").send_keys(Keys.ENTER)
            # time.sleep(5)

            # time.sleep(20)
            print(main_page, alert_page, len(driver.window_handles))
            for handle2 in driver.window_handles:
                print(handle2)
                if handle2 != alert2_page and handle2 != main_page:
                    alert_page = handle2
            print('alert_page ', alert_page)
            print(driver.window_handles)
            driver.close()

            driver.switch_to.default_content()
            driver.switch_to.window(main_page)
            print(driver.current_window_handle)
            # driver.switch_to.window(main_page)
            # print(driver.current_window_handle)
            # driver.close()
            # driver.back()
            driver.get(url)

            # time.sleep(20)
            # driver.switch_to.window(main_page)
            time.sleep(30)
            driver.find_element_by_xpath("//DIV[starts-with(@id,'v_')]/TABLE/TBODY/TR/TD[2]/A").click()
            time.sleep(5)

            print(main_page, alert_page, len(driver.window_handles))
            for handle in driver.window_handles:
                print(handle)
                if handle != main_page:
                    alert_page = handle
            print('alert page: ', alert_page)
            driver.switch_to.window(alert_page)
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//frame[@id='yfcRootFrame']"))
                )
            finally:
                driver.switch_to.frame("yfcRootFrame")
            print(driver.find_element_by_xpath("//tr[@class='evenrow']/td[6]").text)

        while driver.find_element_by_xpath("//tr[@class='evenrow']/td[6]").text == 'PendingReprocess':
            driver.switch_to_default_content()
            driver.close()
            driver.switch_to.window(main_page)
            driver.refresh()
            time.sleep(60)
            driver.find_element_by_xpath("//DIV[starts-with(@id,'v_')]/TABLE/TBODY/TR/TD[2]/A").click()
            time.sleep(5)

            print(main_page, alert_page, len(driver.window_handles))
            for handle in driver.window_handles:
                print(handle)
                if handle != main_page:
                    alert_page = handle
            print('alert page: ', alert_page)
            driver.switch_to.window(alert_page)
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//frame[@id='yfcRootFrame']"))
                )
            finally:
                driver.switch_to.frame("yfcRootFrame")
            print(driver.find_element_by_xpath("//tr[@class='evenrow']/td[6]").text)
    
        # driver.switch_to.frame("yfcRootFrame")
        # driver.find_element_by_xpath("//table[@class='detailpagetitle1']/tbody/tr[@class='pagetitle2']/td[@class='detailpagetitle6']/input[@value='Close']").send_keys(Keys.ENTER)
        driver.close()
        time.sleep(20)
        driver.switch_to.window(main_page)
        time.sleep(30)

        state = driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr[2]/td[6]").text
        print(state)
        driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[3]").click()
        if state != 'Closed':
            alert_obj = driver.switch_to.alert
            alert_obj.accept()
        time.sleep(10)
        print(driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr[2]/td[6]").text)
        if int(count) == 1:
            time.sleep(5)
            return
        print(count) 
        go_next()
        time.sleep(5)
        print()

if int(count) > 1:
    driver.find_element_by_xpath("//div[@id='ipc1']/table/thead/tr/td[1]/input").click()
    driver.find_element_by_xpath("//tr[@id='ipt1']/td[2]/table/tbody/tr/td/table/tbody/tr/td").click()
    time.sleep(5)

reprocess()

msg = f"Subject: {sub}\n\n{body}"
# if(flag != 0):
#     smtp.sendmail(GMAIL_USERNAME, recepients, msg)
flag = 0
driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
driver.set_page_load_timeout(30)
