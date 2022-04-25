import time
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


file = 'oms_config.ini'
config = ConfigParser()
config.read(file)

sub = ''
count = ''
main_page = ''
alert_page = ''

def alert_type(driver):
    global alert_page
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[starts-with(@id,'v_')]/table/tbody/tr[2]/td[6]"))
        )
    finally:
        print(driver.find_element_by_xpath("//div[starts-with(@id,'v_')]/table/tbody/tr[2]/td[6]").text)
    driver.find_element_by_xpath("//DIV[starts-with(@id,'v_')]/TABLE/TBODY/TR/TD[2]/A").click()
    driver.set_page_load_timeout(60)
 
    for handle in driver.window_handles:
        if handle != main_page:
            alert_page = handle
    print(alert_page)
    time.sleep(20)
    driver.switch_to.window(alert_page)
    time.sleep(5)
    try:
        WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.XPATH, "//frame[@id='yfcRootFrame']"))
        )
    finally:
        driver.switch_to.frame("yfcRootFrame") 
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//tr[@class='evenrow']/td[7]"))
        )
    finally:
        return driver.find_element_by_xpath("//tr[@class='evenrow']/td[7]").text

def go_next():
    driver.find_element_by_xpath("/HTML/BODY/FORM/TABLE/TBODY/TR[2]/TD/TABLE/TBODY/TR[1]/TD/DIV/TABLE/TBODY/TR/TD[3]/TABLE/TBODY/TR/TD[4]/A/IMG").click()

def reprocess(driver, count):
    global alert_page
    
    main_page = driver.current_window_handle
    alert_page = ''

    for z in range(int(count)):
        alert = alert_type(driver)
        print(alert)
        # error_code = 'java.lang.NumberFormatException: null'
        # error_code = 'TODO -ERRORCODE'
        error_code = 'java.sql.SQLException'
        if alert != error_code:
            print('Other alert')
            driver.switch_to.default_content()
            driver.close()
            driver.switch_to.window(main_page)
            print('alerts left: ', count - z - 1)
            if int(count) == 1 or count - z - 1 == 0:
                time.sleep(5)
                return
            go_next()
            time.sleep(5)
            continue

        print(driver.find_element_by_xpath("//tr[@class='evenrow']/td[6]").text)

        driver.switch_to.window(alert_page)
        driver.switch_to.frame("yfcRootFrame") 

        print(driver.find_element_by_xpath("//tr[@class='evenrow']/td[6]").text)

        if driver.find_element_by_xpath("//tr[@class='evenrow']/td[6]").text == 'Initial':
            print(driver.find_element_by_xpath("//table[@class='anchor']/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]").text)
            driver.find_element_by_xpath("//table[@class='anchor']/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]").click()
            time.sleep(20)

            # driver.find_element_by_xpath("//table[@class='detailpagetitle1']/tbody/tr[@class='pagetitle2']/td[@class='detailpagetitle6']/input[@value='Close']").send_keys(Keys.ENTER)
            print('main page: ', main_page)
            print('alert page: ', alert_page)
            print('current window: ', driver.current_window_handle)
            time.sleep(20)

            for handle2 in driver.window_handles:
                print(handle2)
                if handle2 != alert2_page and handle2 != main_page:
                    alert_page = handle2
            print('alert page: ', alert_page)

            driver.switch_to.window(alert_page)
            print(driver.current_window_handle)
            driver.close()
            time.sleep(10)
            driver.switch_to.window(main_page)
            time.sleep(15)
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
        print("Alerts left = ",count - z - 1)
        if count != 1 and (count - z) != 1:
            go_next()
            time.sleep(5)
        else:
            return
        print()


def solve():
    global driver, count, main_page, alert_page, alert2_page

    driver = webdriver.Ie(config['urls']['driver_path']) 
    OMS_USERNAME = config['oms_credentials']['username']
    OMS_PASSWORD = config['oms_credentials']['password']

    driver.minimize_window()

    # sub = "OMS_US_UC_Alerts"
    sub = "OMS_US_SR_Alerts"
    # sub = "OMS_CA_UC_Alerts"
    # sub = "OMS_CA_SR_Alerts"
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

    print(sub)
    body = ""
    for queue in queues:
        count = driver.find_element_by_xpath('//td/a[contains(text(),"' + queue + '")]/parent::td//following-sibling::td[2]').text
        if int(count) != 0:
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

    driver.find_element_by_xpath("//DIV[@id='divMenu']/DIV[1]/DIV[2]/TABLE/TBODY/TR[2]/TD[1]/TABLE/TBODY/TR/TD[4]").click()
    driver.set_page_load_timeout(30)

solve()