import time
import smtplib
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import oms_item_code
import oms_tax_negative
import oms_unknown_error
from outlookmail2 import send_email


def oms_us_uc():
    global main_page, alert_page, alert2_page

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
        driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
        driver.set_page_load_timeout(30)
    print("Before reprocessing Item Codes: ")
    print(body)
    check_mlt = False
    # count = driver.find_element_by_xpath('//td/a[contains(text(),"BOC Related Alerts")]/parent::td//following-sibling::td[2]').text
    # if int(count) == 0:
    count = driver.find_element_by_xpath('//td/a[contains(text(),"MLT Related Alerts")]/parent::td//following-sibling::td[2]').text
    if int(count) != 0:
        print('MLT Related Alerts', count)
        driver.find_element_by_link_text("MLT Related Alerts").click()
    # else:
    check_mlt = True
    #     print('BOC Related Alerts', count)
    #     driver.find_element_by_link_text("BOC Related Alerts").click()

    driver.set_page_load_timeout(30)
    time.sleep(5)
    oms_item_code.old_codes = ['51857','54452','50531','54659','50525']
    oms_item_code.new_codes = ['50452','57575','57987','57615','51332']

    if int(count) > 1:
        driver.find_element_by_xpath("//div[@id='ipc1']/table/thead/tr/td[1]/input").click()
        driver.find_element_by_xpath("//tr[@id='ipt1']/td[2]/table/tbody/tr/td/table/tbody/tr/td").click()
        time.sleep(5)

    oms_item_code.reprocess(driver, int(count)) 
    driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
    
    if(check_mlt):
        count = driver.find_element_by_xpath('//td/a[contains(text(),"MLT Related Alerts")]/parent::td//following-sibling::td[2]').text
        if int(count) != 0:
            print('MLT Related Alerts', count)
            driver.find_element_by_link_text("MLT Related Alerts").click()
            driver.set_page_load_timeout(30)
            time.sleep(5)
            if int(count) > 1:
                driver.find_element_by_xpath("//div[@id='ipc1']/table/thead/tr/td[1]/input").click()
                driver.find_element_by_xpath("//tr[@id='ipt1']/td[2]/table/tbody/tr/td/table/tbody/tr/td").click()
                time.sleep(5)
            oms_item_code.reprocess(driver, int(count))

    driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()    
    body = ""
    for queue in queues:
        count = driver.find_element_by_xpath('//td/a[contains(text(),"' + queue + '")]/parent::td//following-sibling::td[2]').text
        # print(queue, count)
        if int(count) != 0:
            flag = 1
            body += queue + "   " + count + '\n'
    print("After reprocessing Item Codes: ")
    print(body)

    # with smtplib.SMTP_SSL(config['gmail_credentials']['server'], 465) as smtp:
    #     smtp.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    #     msg = f"Subject: {sub}\n\n{body}"
    if(flag != 0):
        send_email(OUTLOOK_USERNAME, OUTLOOK_PASSWORD, recepients, sub, body)
        time.sleep(10)
    flag = 0
 

def oms_us_sr():
    global main_page, alert_page, alert2_page

    sub = "OMS_US_SR_Alerts"
    queues = list((config['queues']['sr']).split(','))

    driver.get(config['urls'][sub])
    driver.minimize_window()
    driver.set_page_load_timeout(60)
    driver.find_element_by_name("UserId").clear()
    driver.find_element_by_name("UserId").send_keys(OMS_USERNAME)
    driver.minimize_window()
    driver.find_element_by_name("Password").clear()
    driver.find_element_by_name("Password").send_keys(OMS_PASSWORD)
    driver.minimize_window()
    driver.find_element_by_name("btnLogin").click()
    driver.minimize_window()
    driver.set_page_load_timeout(60)

    flag = 0
    print(sub)
    body = ""
    for queue in queues:
        count = driver.find_element_by_xpath('//td/a[contains(text(),"' + queue + '")]/parent::td//following-sibling::td[2]').text
        if int(count) != 0:
            # flag = 1
            body += queue + "   " + count + '\n'
        driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
        driver.set_page_load_timeout(30)
    print("Before reprocessing Tax Negatives and Unknown Alerts: ")
    print(body)

    driver.find_element_by_link_text("SOLO Related Alerts").click()
    driver.set_page_load_timeout(60)
    time.sleep(5)

    if int(count) > 1:
        driver.find_element_by_xpath("//div[@id='ipc1']/table/thead/tr/td[1]/input").click()
        driver.find_element_by_xpath("//tr[@id='ipt1']/td[2]/table/tbody/tr/td/table/tbody/tr/td").click()
        time.sleep(5)

    x = 0
    while(int(count) - x != 0):
        if oms_tax_negative.alert_type_tax_negative(driver).find('Tax cannot be negative') != -1:
            oms_tax_negative.reprocess(driver, int(count))
            x = 0
        else:
            driver.switch_to.default_content()
            driver.close()
            driver.switch_to.window(main_page)
            if oms_unknown_error.alert_type_unknown_error(driver) == 'Unknown Error':
                oms_unknown_error.reprocess(driver, int(count))
                x = 0
            else:
                print('Other alert')
                x += 1
                driver.switch_to.default_content()
                driver.close()
                driver.switch_to.window(main_page)
                print('alerts left: ', int(count) - x)
                if int(count) == 1:
                    time.sleep(5)
                    return
                oms_tax_negative.go_next(driver)
                time.sleep(5)

    driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
    body = ""
    for queue in queues:
        count = driver.find_element_by_xpath('//td/a[contains(text(),"' + queue + '")]/parent::td//following-sibling::td[2]').text
        if int(count) != 0:
            flag = 1
            body += queue + "   " + count + '\n'
        driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
        driver.set_page_load_timeout(30)
    print("After reprocessing Tax Negatives and Unknown Alerts: ")
    print(body)

    # with smtplib.SMTP_SSL(config['gmail_credentials']['server'], 465) as smtp:
    #     smtp.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    #     msg = f"Subject: {sub}\n\n{body}"
    if(flag != 0):
        send_email(OUTLOOK_USERNAME, OUTLOOK_PASSWORD, recepients, sub, body)
        time.sleep(10)
    flag = 0

def oms_ca_uc():
    global main_page, alert_page, alert2_page

    sub = "OMS_CA_UC_Alerts"
    queues = queues = list((config['queues']['uc']).split(','))

    driver.get(config['urls'][sub])
    driver.minimize_window()
    driver.set_page_load_timeout(60)
    driver.find_element_by_name("UserId").clear()
    driver.find_element_by_name("UserId").send_keys(OMS_USERNAME)
    driver.minimize_window()
    driver.find_element_by_name("Password").clear()
    driver.find_element_by_name("Password").send_keys(OMS_PASSWORD)
    driver.minimize_window()
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
            # flag = 1
            body += queue + "   " + count + '\n'
        driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
        driver.set_page_load_timeout(30)
    print("Before reprocessing Item Codes: ")
    print(body)
    check_mlt = False
    count = driver.find_element_by_xpath('//td/a[contains(text(),"BOC Related Alerts")]/parent::td//following-sibling::td[2]').text
    if int(count) == 0:
        count = driver.find_element_by_xpath('//td/a[contains(text(),"MLT Related Alerts")]/parent::td//following-sibling::td[2]').text
        if int(count) != 0:
            print('MLT Related Alerts', count)
            driver.find_element_by_link_text("MLT Related Alerts").click()
    else:
        check_mlt = True
        print('BOC Related Alerts', count)
        driver.find_element_by_link_text("BOC Related Alerts").click()

    driver.set_page_load_timeout(30)
    time.sleep(5)
    oms_item_code.old_codes = ['51857','54452','50531','54659','50525']
    oms_item_code.new_codes = ['50452','57575','57987','57615','51332']
    
    if int(count) > 1:
        driver.find_element_by_xpath("//div[@id='ipc1']/table/thead/tr/td[1]/input").click()
        driver.find_element_by_xpath("//tr[@id='ipt1']/td[2]/table/tbody/tr/td/table/tbody/tr/td").click()
        time.sleep(5)

    oms_item_code.reprocess(driver, int(count))
    driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
    
    if(check_mlt):
        count = driver.find_element_by_xpath('//td/a[contains(text(),"MLT Related Alerts")]/parent::td//following-sibling::td[2]').text
        if int(count) != 0:
            print('MLT Related Alerts', count)
            driver.find_element_by_link_text("MLT Related Alerts").click()
            driver.set_page_load_timeout(30)
            time.sleep(5)
            if int(count) > 1:
                driver.find_element_by_xpath("//div[@id='ipc1']/table/thead/tr/td[1]/input").click()
                driver.find_element_by_xpath("//tr[@id='ipt1']/td[2]/table/tbody/tr/td/table/tbody/tr/td").click()
                time.sleep(5)
            oms_item_code.reprocess(driver, int(count))
    
    driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
    body = ""
    for queue in queues:
        count = driver.find_element_by_xpath('//td/a[contains(text(),"' + queue + '")]/parent::td//following-sibling::td[2]').text
        # print(queue, count)
        if int(count) != 0:
            flag = 1
            body += queue + "   " + count + '\n'
        driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
        driver.set_page_load_timeout(30)
    print("After reprocessing Item Codes: ")
    print(body) 
    
    # with smtplib.SMTP_SSL(config['gmail_credentials']['server'], 465) as smtp:
    #     smtp.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    #     msg = f"Subject: {sub}\n\n{body}"
    if(flag != 0):
        send_email(OUTLOOK_USERNAME, OUTLOOK_PASSWORD, recepients, sub, body)
        time.sleep(10)
    flag = 0


def oms_ca_sr():
    global main_page, alert_page, alert2_page

    sub = "OMS_CA_SR_Alerts"
    queues = queues = list((config['queues']['sr']).split(','))

    driver.get(config['urls'][sub])
    driver.minimize_window()
    driver.set_page_load_timeout(60)
    driver.find_element_by_name("UserId").clear()
    driver.find_element_by_name("UserId").send_keys(OMS_USERNAME)
    driver.minimize_window()
    driver.find_element_by_name("Password").clear()
    driver.find_element_by_name("Password").send_keys(OMS_PASSWORD)
    driver.minimize_window()
    driver.find_element_by_name("btnLogin").click()
    driver.minimize_window()
    driver.set_page_load_timeout(180)
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
    print("Before reprocessing Tax Negatives: ")
    print(body)

    driver.find_element_by_link_text("SOLO Related Alerts").click()
    driver.set_page_load_timeout(60)
    time.sleep(5)

    if int(count) > 1:
        driver.find_element_by_xpath("//div[@id='ipc1']/table/thead/tr/td[1]/input").click()
        driver.find_element_by_xpath("//tr[@id='ipt1']/td[2]/table/tbody/tr/td/table/tbody/tr/td").click()
        time.sleep(5)

    oms_tax_negative.reprocess(driver, int(count))
    driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()

    driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
    body = ""
    for queue in queues:
        count = driver.find_element_by_xpath('//td/a[contains(text(),"' + queue + '")]/parent::td//following-sibling::td[2]').text
        if int(count) != 0:
            flag = 1
            body += queue + "   " + count + '\n'
        driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
        driver.set_page_load_timeout(30)
    print("After reprocessing Tax Negatives: ")
    print(body)

    # with smtplib.SMTP_SSL(config['gmail_credentials']['server'], 465) as smtp:
    #     smtp.login(GMAIL_USERNAME, GMAIL_PASSWORD)
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

# recepients = ['v-NKappaganthula@shutterfly.com', 'v-kalpana.joga@shutterfly.com', 'v-srija.prattipati@shutterfly.com']
recepients = list((config['outlook_credentials']['recepients']).split(','))


driver = webdriver.Ie(config['urls']['driver_path'])
# driver.maximize_window()
driver.minimize_window()

main_page = driver.current_window_handle
alert_page = ''
alert2_page = ''

while(1):
    # with smtplib.SMTP_SSL(config['gmail_credentials']['server'], 465) as smtp:
    #     smtp.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    oms_us_uc()
    oms_us_sr()
    oms_ca_uc()
    oms_ca_sr()
    driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
    time.sleep(1800)
    driver.refresh()