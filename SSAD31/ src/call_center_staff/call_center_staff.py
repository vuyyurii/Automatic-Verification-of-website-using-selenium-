from __future__ import print_function
import time
import json

'''get info from config file'''
with open('../config.json') as json_data_file:
    cfg = json.load(json_data_file)

with open('../super_admin/data.json') as json_file:
    cred = json.load(json_file)

class staff():
    '''automates various activities of Hospital CMS'''

    def login(self, driver):
        '''verify login'''
        uname = cred["Staff"][0]["username"]
        passwd = cred["Staff"][0]["password"]
        assert driver.current_url == cfg["URL"] + "/login"
        driver.find_element_by_id("username").send_keys(uname)
        driver.find_element_by_id("pswrd").send_keys(passwd)
        time.sleep(1)
        driver.find_element_by_class_name("login-btn").click()
        assert driver.current_url == cfg["URL"] + "/call-center/patients"
        assert driver.title == "Patients"
        return

    def view_patients(self, i, driver):

        '''verifies the patients displayed'''
        pass

    def change_password(self, driver):
        '''verifies change password'''
        driver.find_element_by_xpath("/html/body/header/div/div/div[2]/table/tbody/tr/td[2]/img").click()
        driver.find_element_by_xpath("/html/body/header/div/div/div[2]/ul/li/div[1]/div[2]/p[2]/a").click()
        assert driver.current_url == cfg["URL"] + "/call-center/change-password"
        passwd = cred["Staff"][0]["password"]

        driver.find_element_by_xpath('//*[@id="currentPassword"]').click()
        driver.find_element_by_xpath('//*[@id="currentPassword"]').clear()
        driver.find_element_by_xpath('//*[@id="currentPassword"]').send_keys(passwd)

        driver.find_element_by_xpath('//*[@id="newPassword"]').click()
        driver.find_element_by_xpath('//*[@id="newPassword"]').clear()
        driver.find_element_by_xpath('//*[@id="newPassword"]').send_keys(passwd)

        driver.find_element_by_xpath('//*[@id="confirmNewPassword"]').click()
        driver.find_element_by_xpath('//*[@id="confirmNewPassword"]').clear()
        driver.find_element_by_xpath('//*[@id="confirmNewPassword"]').send_keys(passwd)
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div/div/div/div[2]/form/div/button').click()

        driver.find_element_by_xpath('/html/body/div/div/p[2]/a').click()
        assert driver.current_url == cfg["URL"] + "/call-center/patients"
        assert driver.title == "Patients"


    def logout(self, driver):
        '''verifies logging out'''
        driver.find_element_by_xpath("html/body/header/div/div/div[2]/table/tbody/tr/td[3]/i").click()
        driver.find_element_by_xpath("html/body/header/div/div/div[2]/ul/li/div[2]/a/button").click()

        assert driver.current_url == cfg["URL"] + "/login"

        return
