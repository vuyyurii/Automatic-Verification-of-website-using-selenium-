from __future__ import print_function
import json
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


with open('../config.json') as json_data_file:
    cfg = json.load(json_data_file)

with open('../hospital_admin/data.json') as json_file:
    cred = json.load(json_file)

class Assistant_doctor():
    '''automates various activities of assistant doctor'''
    def __init__(self):
        '''initialize the email ids'''
        self.ast = cfg["Email_Assist"].split("@")


    def login(self,driver):
        '''verify login'''
        uname = cred["Assistant"][0]["username"]
        passwd = cred["Assistant"][0]["password"]
        assert driver.current_url, cfg["URL"] + "/login"
        driver.find_element_by_id("username").send_keys(uname)
        driver.find_element_by_id("pswrd").send_keys(passwd)
        driver.find_element_by_class_name("login-btn").click()
        assert driver.current_url,  cfg["URL"] +" /doctor/patients"
        assert driver.title, "Assistant_doctors"
        return

    def search(self, i, driver):

        driver.find_element_by_xpath('//*[@id="searchForPatientText"]').click()
        driver.find_element_by_xpath('//*[@id="searchForPatientText"]').clear()
        driver.find_element_by_xpath('//*[@id="searchForPatientText"]').send_keys("R" + Keys.TAB)


        return

    def choose_doctor(self, i ,driver):

        if driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div/button').is_displayed():
            driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div/button').click()
            s1 = Select(driver.find_element_by_xpath('//*[@id="doctor-name"]'))
            s1.select_by_value("58")
            #time.sleep(3)
            return

        else:
            return

    def filters(self, i ,driver):

        driver.find_element_by_xpath('//*[@id="filterBtn"]').click()

        driver.find_element_by_xpath('//*[@id="surgery-date"]').click()
        s1 = Select(driver.find_element_by_class_name('monthselect'))
        if i % 2 == 0:
            s1.select_by_value('6')
            time.sleep(3)
            s2 = Select(driver.find_element_by_class_name('yearselect'))
            s2.select_by_value('2004')
            sn1 = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/table/tbody/tr[4]/td[4]')
        else:
            s1.select_by_value('4')
            time.sleep(3)
            s2 = Select(driver.find_element_by_class_name('yearselect'))
            s2.select_by_value('2002')
            sn1 = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/table/tbody/tr[4]/td[4]')

        ActionChains(driver).move_to_element(sn1).click().click().perform()
        
        driver.find_element_by_xpath('//*[@id="rightMenu"]/div/button[1]').click()

        return


    def click_buttons(self, i, driver):

        if i % 3 == 0:
            #d1 = driver.find_element_by_xpath('//*[@id="page-selection"]/ul/li[1]/a')
            if driver.find_element_by_xpath('//*[@id="page-selection"]/ul/li[1]/a').is_displayed():
                driver.find_element_by_xpath('//*[@id="page-selection"]/ul/li[1]/a').click()
        elif i % 3 == 1:
            #d2 = driver.find_element_by_xpath('//*[@id="page-selection"]/ul/li[2]/a')
            if driver.find_element_by_xpath('//*[@id="page-selection"]/ul/li[2]/a').is_displayed():
                driver.find_element_by_xpath('//*[@id="page-selection"]/ul/li[2]/a').click()
        else:
            #d3 = driver.find_element_by_xpath('//*[@id="page-selection"]/ul/li[3]/a')
            if driver.find_element_by_xpath('//*[@id="page-selection"]/ul/li[3]/a').is_displayed():
                driver.find_element_by_xpath('//*[@id="page-selection"]/ul/li[3]/a').click()

        return


    def as_patients(self, i, driver):

        driver.find_element_by_xpath('//*[@id="searchForPatientText"]').clear()

        #self.search(i, driver)
        assert driver.current_url,  cfg["URL"] + "/doctor/patients"
        assert driver.title, "Assistant_doctors"

        #driver.find_element_by_xpath('//*[@id="searchForPatientText"]').clear()

        # self.choose_doctor(i, driver)
        assert driver.current_url,  cfg["URL"] + "/doctor/patients"
        assert driver.title, "Assistant_doctors"
        print ('chosen')
        time.sleep(3)

        #self.filters(i, driver)
        assert driver.current_url,  cfg["URL"] + "/doctor/patients"
        assert driver.title, "Assistant_doctors"

        self.click_buttons(i, driver)
        print ('button clicked')
        assert driver.current_url,  cfg["URL"] + "/doctor/patients"
        assert driver.title, "Assistant_doctors"

        self.filters(i, driver)

        return

    def logout(self, i, driver):
        driver.find_element_by_xpath('/html/body/header/div/div/div[2]/ul/li/div[2]/a[2]/button').click()
        assert driver.current_url,  cfg["URL"] + "/login"

        return

    def password_change(self, i, driver):

        passwd = cred["Assistant"][0]["password"]

        driver.find_element_by_xpath('/html/body/header/div/div/div[2]/ul/li/div[1]/div[2]/p[2]/a').click()
        assert driver.current_url,  cfg["URL"] + "/doctor/change-password"
        assert driver.title, "Password_change"

        driver.find_element_by_xpath('//*[@id="currentPassword"]').clear()
        driver.find_element_by_xpath('//*[@id="currentPassword"]').send_keys(passwd)

        driver.find_element_by_xpath('//*[@id="newPassword"]').clear()
        driver.find_element_by_xpath('//*[@id="newPassword"]').send_keys(passwd)

        driver.find_element_by_xpath('//*[@id="confirmNewPassword"]').clear()
        driver.find_element_by_xpath('//*[@id="confirmNewPassword"]').send_keys(passwd)

        driver.find_element_by_xpath('/html/body/div/div/div/div[2]/form/div/button').click()

        assert driver.current_url, cfg["URL"] + "/doctor/patients"
        assert driver.title, "Assistant_doctors"
        
        return

    def my_profile(self, i, driver):

        driver.find_element_by_xpath('/html/body/header/div/div/div[2]/ul/li/div[2]/a[1]/button').click()

        driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[5]/a/button').click()
        assert driver.current_url,  cfg["URL"] + "/doctor/profile"
        assert driver.title, "Profile"

        driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div[5]/a/button").click()

        assert driver.current_url,  cfg["URL"] + "/doctor/edit-profile"
        assert driver.title, "edit_profile"

        driver.find_element_by_xpath('//*[@id="firstName"]').clear()
        driver.find_element_by_xpath('//*[@id="firstName"]').send_keys("Ravi" + str(i))

        driver.find_element_by_xpath('//*[@id="lastName"]').clear()
        driver.find_element_by_xpath('//*[@id="lastName"]').send_keys("Dubey" + str(i))

        if i % 2 == 0:
            driver.find_element_by_xpath('//*[@id="update-profile"]/div/div[2]/div/button').click()
        else:
            driver.find_element_by_xpath('//*[@id="update-profile"]/div/div[2]/div/a/button').click()

        assert driver.current_url,  cfg["URL"] + "/doctor/profile"
        assert driver.title, "Profile"

        driver.find_element_by_xpath('/html/body/nav/div/div/div/div[1]/ul/li[1]/a').click()

        assert driver.current_url,  cfg["URL"] + "/doctor/patients"
        assert driver.title, "Assistant_doctors"

        return


    def profile(self, i, driver):
        driver.find_element_by_xpath('/html/body/header/div/div/div[2]/table/tbody/tr/td[3]/i').click()

        if i % 3 == 0:
            self.password_change(i, driver)
        elif i % 3 == 0:
            self.my_profile(i, driver)
        else:
            self.logout(i, driver)

        return
