import time
import smtplib
import xml.etree.ElementTree as ET
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

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

while(1):
    sub = "OMS_US_UC_Alerts"
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
    count = driver.find_element_by_xpath('//td/a[contains(text(),"MLT Related Alerts")]/parent::td//following-sibling::td[2]').text
    print(count)
    driver.find_element_by_link_text("MLT Related Alerts").click()
    # driver.find_element_by_link_text("SOLO Related Alerts").click()
    driver.set_page_load_timeout(30)
    if int(count) > 1:
        driver.find_element_by_xpath("//div[@id='ipc1']/table/thead/tr/td[1]/input").click()
        driver.find_element_by_xpath("//tr[@id='ipt1']/td[2]/table/tbody/tr/td/table/tbody/tr/td").click()
        
        for _ in range(int(count)):
            main_page = driver.current_window_handle
            time.sleep(5)
            # alert_link = driver.find_element_by_xpath("//DIV[starts-with(@id,'v_')]/TABLE/TBODY/TR/TD[2]/A")
            # action.click(alert_link)
            # action.perform()
            print(driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr[2]/td[6]").text)
            driver.find_element_by_xpath("//DIV[starts-with(@id,'v_')]/TABLE/TBODY/TR/TD[2]/A").click()
            driver.set_page_load_timeout(60)
            time.sleep(10)

            for handle in driver.window_handles:
                if handle != main_page:
                    alert_page = handle
            driver.switch_to.window(alert_page)

            driver.switch_to.frame("yfcRootFrame")
            alert = driver.find_element_by_xpath("//tr[@class='evenrow']/td[7]").text
            print(alert)

            # xml = driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr/td/textarea").text
            # # print(xml)
            # root = ET.fromstring(xml)

            # print(root)
            # for tags in root[1]:
            #     print(tags[0].tag,tags[0].attrib)
                # for attr in tags[0].attrib:
                #     if attr == 'ExtnEventRefID':
                #         # print(list(tags[0].attrib.keys()).index(attr))
                #         print(tags[0].attrib[attr])

            print(driver.find_element_by_id("scbutton2").text)
            driver.find_element_by_id("scbutton2").click()
            time.sleep(5)            

            driver.switch_to.default_content()
            driver.close()
            driver.switch_to.window(main_page)

            driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[3]").click()
            alert_obj = driver.switch_to.alert
            alert_obj.accept()
            time.sleep(10)
            print(driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr[2]/td[6]").text)
            driver.find_element_by_xpath("/HTML/BODY/FORM/TABLE/TBODY/TR[2]/TD/TABLE/TBODY/TR[1]/TD/DIV/TABLE/TBODY/TR/TD[3]/TABLE/TBODY/TR/TD[4]/A/IMG").click()
            time.sleep(5)
            print()

    elif int(count) == 1:
    
        main_page = driver.current_window_handle
        time.sleep(5)

        driver.find_element_by_xpath("//DIV[starts-with(@id,'v_')]/TABLE/TBODY/TR/TD[2]/A").click()
        driver.set_page_load_timeout(30)        

        for handle in driver.window_handles:
            if handle != main_page:
                alert_page = handle
        driver.switch_to.window(alert_page)

        driver.switch_to.frame("yfcRootFrame")
        alert = driver.find_element_by_xpath("//tr[@class='evenrow']/td[7]").text
        print(alert)
        driver.switch_to.default_content()
        driver.close()
        driver.switch_to.window(main_page)      
    

    msg = f"Subject: {sub}\n\n{body}"
    # if(flag != 0):
    #     smtp.sendmail(GMAIL_USERNAME, recepients, msg)
    flag = 0
    driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
    driver.set_page_load_timeout(30)
    break
