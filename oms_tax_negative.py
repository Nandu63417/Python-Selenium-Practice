import time
import sys
import smtplib
import xml.etree.ElementTree as ET
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


file = 'oms_config.ini'
config = ConfigParser()
config.read(file)

# sub = "OMS_US_UC_Alerts"
# sub = "OMS_US_SR_Alerts"
# sub = "OMS_CA_UC_Alerts"
# sub = "OMS_CA_SR_Alerts"
sub = sys.argv[1]
count = ''
main_page = ''
alert_page = ''
alert2_page = ''

def check_balance(driver, order_id):
    print(sub)
    if sub == "OMS_US_SR_Alerts":
        print(sub)
        driver.get('https://oms-seniors.lifetouch.net/yantra/console/order.search')
    elif sub == "OMS_CA_SR_Alerts":
        print(sub)
        driver.get('https://oms-seniors-ca.lifetouch.net/yantra/console/order.search')
    time.sleep(5)
    print(order_id)
    driver.find_element_by_xpath("//TD[@id='searchPanel']/DIV/TABLE/TBODY/TR[1]/TD/TABLE/TBODY/TR[5]/TD/INPUT").send_keys(order_id)
    driver.find_element_by_xpath("//td[@class='searchbuttons']/a/input[@value='Search']").click()
    time.sleep(10)
    amount_due = driver.find_element_by_xpath("//DIV[starts-with(@id, 'v_')]/TABLE/TBODY/TR[5]/TD[not(contains(@class,'totaltext'))][2]/SPAN[1]").text
    print(amount_due)
    return float(amount_due)

def go_next(driver):
    driver.find_element_by_xpath("/HTML/BODY/FORM/TABLE/TBODY/TR[2]/TD/TABLE/TBODY/TR[1]/TD/DIV/TABLE/TBODY/TR/TD[3]/TABLE/TBODY/TR/TD[4]/A/IMG").click()

def alert_type_tax_negative(driver):
    global alert_page
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[starts-with(@id,'v_')]/table/tbody/tr[2]/td[6]"))
        )
    finally:
        print(driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr[2]/td[6]").text)
    driver.find_element_by_xpath("//DIV[starts-with(@id,'v_')]/TABLE/TBODY/TR/TD[2]/A").click()
    driver.set_page_load_timeout(60)
    # time.sleep(5)

    for handle in driver.window_handles:
        if handle != main_page:
            alert_page = handle
    print(alert_page)
    time.sleep(20)
    driver.switch_to.window(alert_page)
    try:
        WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.XPATH, "//frame[@id='yfcRootFrame']"))
        )
    finally:
        driver.switch_to.frame("yfcRootFrame") 
    # driver.switch_to.frame("yfcRootFrame")
    
    return driver.find_element_by_xpath("//tr[@class='evenrow']/td[8]").text


def reprocess(driver, count):
    global alert_page
    global alert2_page

    main_page = driver.current_window_handle
    alert_page = ''
    alert2_page = ''
    x = 0
    # y = 0
    for _ in range(count): 
        
        print(driver.find_element_by_xpath("//DIV[starts-with(@id,'v_')]/TABLE/TBODY/TR/TD[2]/A").text, len(driver.find_element_by_xpath("//DIV[starts-with(@id,'v_')]/TABLE/TBODY/TR/TD[2]/A").text))
        if len(driver.find_element_by_xpath("//DIV[starts-with(@id,'v_')]/TABLE/TBODY/TR/TD[2]/A").text) < 22:
            print('Other alert by length')
            x += 1
            print('alerts left: ', count - x)
            if int(count) == 1 or (count - x) == 0:
                time.sleep(5)
                return
            go_next(driver)
            time.sleep(5)
            continue
        alert = alert_type_tax_negative(driver)
        if alert.find('Tax cannot be negative') != -1:
            print('Tax cannot be negative')
        else:
            print('Other alert')
            x += 1
            driver.switch_to.default_content()
            driver.close()
            driver.switch_to.window(main_page)
            print('alerts left: ', count - x)
            if int(count) == 1 or (count - x) == 0:
                time.sleep(5)
                return
            go_next(driver)
            time.sleep(5)
            continue

        xml = driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr/td/textarea").text
        # print(xml)
        root = ET.fromstring(xml)

        # .//*[@attr]
        for tax in root.findall(".//*[@TaxPercentage]"):
            # print(tax.text, tax.attrib)
            if float(tax.attrib['TaxPercentage']) < 0:
                print(tax.attrib['TaxPercentage'])
                tax.set('TaxPercentage', str(float(tax.attrib['TaxPercentage']) * -1))

        for tax in root.findall(".//*[@TaxPercentage]"):
            print(tax.attrib['TaxPercentage'])

        new_xml = ET.tostring(root, encoding = 'unicode')
        new_xml = str(new_xml)
        new_xml = new_xml.replace('ns0','It')
        # print(xml, type(xml))
        # print(new_xml, type(new_xml))

        for order in root.iter('Order'):
            order_id = order.attrib['OrderNo']
        print(order_id)

        print(driver.find_element_by_xpath("//tr[@class='evenrow']/td[6]").text)
        
        if driver.find_element_by_xpath("//tr[@class='evenrow']/td[6]").text == 'Initial':
            driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr/td/textarea").clear()
            driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr/td/textarea").send_keys(new_xml)
        
            driver.find_element_by_xpath("//table[@class='detailpagetitle1']/tbody/tr[@class='pagetitle2']/td[@class='detailpagetitle6']/input[@value='Save']").send_keys(Keys.ENTER)
            time.sleep(30) 

        driver.switch_to.window(alert_page)
        driver.switch_to.frame("yfcRootFrame") 
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
            time.sleep(5)
            driver.switch_to.frame("yfcRootFrame")    
            # print(driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr/td/textarea").text)

            print(driver.find_element_by_xpath("//table[@class='anchor']/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]").text)
            driver.find_element_by_xpath("//table[@class='anchor']/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]").click()
            time.sleep(20)

            # driver.find_element_by_xpath("//table[@class='detailpagetitle1']/tbody/tr[@class='pagetitle2']/td[@class='detailpagetitle6']/input[@value='Close']").send_keys(Keys.ENTER)
            print('main page: ', main_page)
            print('alert page: ', alert_page)
            print('alert2 page: ', alert2_page)
            print('current window: ', driver.current_window_handle)
            driver.close()

            time.sleep(20)
            print(main_page, alert2_page, len(driver.window_handles))
            for handle2 in driver.window_handles:
                print(handle2)
                if handle2 != alert2_page and handle2 != main_page:
                    alert_page = handle2
            print('alert page: ', alert_page)

            driver.switch_to.window(alert_page)
            print(driver.current_window_handle)
            
            driver.close()

            # Error 403
            # driver.back()

            time.sleep(20)

            driver.switch_to.window(main_page)
            time.sleep(30)
            driver.find_element_by_xpath("//DIV[starts-with(@id,'v_')]/TABLE/TBODY/TR/TD[2]/A").click()
            time.sleep(20)

            print(main_page, alert_page, len(driver.window_handles))
            for handle in driver.window_handles:
                print(handle)
                if handle != main_page:
                    alert_page = handle
            print('alert page: ', alert_page)
            driver.switch_to.window(alert_page)
            driver.switch_to.frame("yfcRootFrame")
            print(driver.find_element_by_xpath("//tr[@class='evenrow']/td[6]").text)

        while driver.find_element_by_xpath("//tr[@class='evenrow']/td[6]").text == 'PendingReprocess':
            driver.switch_to.default_content()
            driver.close()
            driver.switch_to.window(main_page)
            driver.refresh()
            
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')

                alert = driver.switch_to.alert
                alert.accept()
                print("alert accepted")
            except TimeoutException:
                print("no alert")
            time.sleep(60)
            driver.find_element_by_xpath("//DIV[starts-with(@id,'v_')]/TABLE/TBODY/TR/TD[2]/A").click()
            time.sleep(10)

            print(main_page, alert_page, len(driver.window_handles))
            for handle in driver.window_handles:
                print(handle)
                if handle != main_page:
                    alert_page = handle
            print('alert page: ', alert_page)
            driver.switch_to.window(alert_page)
            driver.switch_to.frame("yfcRootFrame")
            print(driver.find_element_by_xpath("//tr[@class='evenrow']/td[6]").text)
    
        driver.close()
        time.sleep(20)
        driver.switch_to.window(main_page)
        time.sleep(30)

        state = driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr[2]/td[6]").text
        print(state)
        driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[3]").click()
        
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                'Timed out waiting for PA creation ' +
                                'confirmation popup to appear.')

            alert = driver.switch_to.alert
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")

        time.sleep(10)
        print('After refreshing: ')
        print(driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr[2]/td[6]").text)
        # print('count - z = ', int(count) - z)
        if driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr[2]/td[6]").text == 'Closed':
            amount_due = check_balance(driver, order_id)
            if amount_due != 0.00:
                print(driver.find_elements_by_xpath("//table[starts-with(@id,'ipclbIP')]/tbody/tr/td[4]")[0].text)
                driver.find_elements_by_xpath("//table[starts-with(@id,'ipclbIP')]/tbody/tr/td[4]")[0].click()
                alert = driver.switch_to.alert
                alert.accept()
                print('Amount Due erased')
                time.sleep(20)

            driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
            # driver.get('https://oms-seniors.lifetouch.net/yantra/console/home.detail')
            # driver.get('https://oms-seniors-ca.lifetouch.net/yantra/console/home.detail')
            x = 0
            driver.set_page_load_timeout(30)
            time.sleep(15)
            # prev_count = count
            count = int(driver.find_element_by_xpath('//td/a[contains(text(),"SOLO Related Alerts")]/parent::td//following-sibling::td[2]').text)
            print("Alerts left = ",count)
            # y = prev_count - count
            if count == 0:
                return
            driver.find_element_by_link_text("SOLO Related Alerts").click()  
            time.sleep(10)              
            if int(count) > 1:
                driver.find_element_by_xpath("//div[@id='ipc1']/table/thead/tr/td[1]/input").click()
                driver.find_element_by_xpath("//tr[@id='ipt1']/td[2]/table/tbody/tr/td/table/tbody/tr/td").click()

        else:
            if int(count) == 1:
                time.sleep(5)
                return
            print(count) 
            go_next(driver)

        time.sleep(5)
        print()

def solve():
    global driver, count, main_page, alert_page, alert2_page

    driver = webdriver.Ie(config['urls']['driver_path']) 
    OMS_USERNAME = config['oms_credentials']['username']
    OMS_PASSWORD = config['oms_credentials']['password']

    # GMAIL_USERNAME = config['gmail_credentials']['account']
    # GMAIL_PASSWORD = config['gmail_credentials']['pwd']

    # recepients = ['v-NKappaganthula@shutterfly.com', 'v-kalpana.joga@shutterfly.com', 'v-srija.prattipati@shutterfly.com']
    # recepients = list((config['gmail_credentials']['recepients']).split(','))

    # driver.maximize_window()
    driver.minimize_window()
    # action = ActionChains(driver)

    # queues = list((config['queues']['uc']).split(','))
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
    driver.set_page_load_timeout(120)
    time.sleep(30)
    

    # flag = 0
    print(sub)
    body = ""
    for queue in queues:
        count = driver.find_element_by_xpath('//td/a[contains(text(),"' + queue + '")]/parent::td//following-sibling::td[2]').text
        # print(queue, count)
        if int(count) != 0:
            # flag = 1
            body += queue + "   " + count + '\n'
    print(body)
    driver.find_element_by_link_text("SOLO Related Alerts").click()
    driver.set_page_load_timeout(60)
    time.sleep(5)

    main_page = driver.current_window_handle
    alert_page = ''
    alert2_page = ''
    if int(count) > 1:
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='ipc1']/table/thead/tr/td[1]/input"))
            )
        finally:
            driver.find_element_by_xpath("//div[@id='ipc1']/table/thead/tr/td[1]/input").click()
            driver.find_element_by_xpath("//tr[@id='ipt1']/td[2]/table/tbody/tr/td/table/tbody/tr/td").click()


    reprocess(driver, int(count))
    # check_balance('L8DN7GH8')

    # msg = f"Subject: {sub}\n\n{body}"
    # if(flag != 0):
    #     smtp.sendmail(GMAIL_USERNAME, recepients, msg)
    # flag = 0
    driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
    driver.set_page_load_timeout(30)

solve()