from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import csv
import time

def main():
    record = []
    uat_list = get_uat_list()

    for uat in uat_list:
        recs = get_data(uat)
        for rec in recs:
            record.append(rec)

    print(record)
    df = pd.DataFrame(record, columns = ['localitate', 'companie', 'telefonie_fixa', 'internet_fix', 'TV_cablu'])
    df.to_csv('ancom_cluj.csv', index = False)

def get_uat_list():
    driver = webdriver.Firefox()
    driver.get("https://statistica.ancom.ro/sscpds/public/serviceCoverage#gmap")
    driver.maximize_window()

    actions = ActionChains(driver)

    driver.find_element_by_id("countySiruta-field-inputCell").click()
    driver.find_element_by_xpath("//*[text()='J. CLUJ']").click()
    time.sleep(10)

    driver.find_element_by_id("autoComplete-field-inputEl").send_keys('agh')
    time.sleep(2)
    for i in range(3):
        driver.find_element_by_id("autoComplete-field-inputEl").send_keys(Keys.BACKSPACE)
    driver.find_element_by_id("autoComplete-field-inputEl").send_keys(' ')
    time.sleep(2)

    li_list = driver.find_elements_by_class_name("x-boundlist-item")

    uat_list = []
    for li in li_list:
        if li.text != '':
            uat_list.append(li.text.rstrip())
    
    driver.quit()
    return uat_list


def get_data(uat):
    rec = []

    driver = webdriver.Firefox()
    driver.get("https://statistica.ancom.ro/sscpds/public/serviceCoverage#gmap")
    driver.maximize_window()

    actions = ActionChains(driver)

    driver.find_element_by_id("countySiruta-field-inputCell").click()
    driver.find_element_by_xpath("//*[text()='J. CLUJ']").click()
    time.sleep(10)

    driver.find_element_by_id("autoComplete-field-inputEl").send_keys(uat)
    driver.find_element_by_id("autoComplete-field-inputEl").send_keys(Keys.ENTER)
    time.sleep(5)

    map = driver.find_element_by_id("gmap")
    actions.move_to_element(map).perform()
    actions.move_by_offset(0,-10).perform()
    actions.click().perform()

    try:
        a = driver.find_element_by_link_text("aici")
        a.click()
        time.sleep(5)

        rows = driver.find_elements_by_class_name("x-grid-row")
        for row in rows:
            text = row.text.split('\n')
            rec.append([uat,text[0],text[1],text[2],text[3]])
            print(rec)
            print("______________")
    except:
        pass

    driver.quit()
    return rec

if __name__ == "__main__":
    main()