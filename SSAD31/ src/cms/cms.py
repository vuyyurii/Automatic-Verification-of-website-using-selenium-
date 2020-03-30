from __future__ import print_function
import json
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

'''get info from config file'''
with open('../config.json') as json_data_file:
    cfg = json.load(json_data_file)

with open('../hospital_admin/data.json') as json_file:
    cred = json.load(json_file)

class CMS():
    '''automates various activities of Hospital CMS'''

    def login(self, driver):
        '''verify login'''
        uname = cred["CMS"][0]["username"]
        passwd = cred["CMS"][0]["password"]
        assert driver.current_url == cfg["URL"]+"/login"
        driver.find_element_by_id("username").send_keys(uname)
        driver.find_element_by_id("pswrd").send_keys(passwd)
        time.sleep(1)
        driver.find_element_by_class_name("login-btn").click()
        assert driver.current_url == cfg["URL"]+"/hospital/articles"
        assert driver.title == "Articles"
        return

    def add_article(self, i, driver):
        '''verifies adding article'''
        driver.find_element_by_xpath("//button[contains(.,'Add Article')]").click()

        assert driver.current_url == cfg["URL"]+"/hospital/add-article"

        img = driver.find_element_by_xpath("//input[@type='image']")
        img.send_keys(os.getcwd() + "/image.jpeg")
        img.submit()

        driver.find_element_by_xpath("//input[@id='title']").click()
        driver.find_element_by_xpath("//input[@id='title']").clear()
        driver.find_element_by_xpath("//input[@id='title']").send_keys("title" + str(i))

        driver.find_element_by_xpath("//button[@title='Choose One']").click()
        #dropdown = Select(driver.find_element_by_xpath("//button[@aria-expanded='true']"))
        if i % 4 == 0:
            driver.find_element_by_xpath("//span[contains(.,'Specific patients')]").click()
            #specific patients
        elif i % 4 == 1:
            driver.find_element_by_xpath("//a[contains(.,'All tagged patients')]").click()
            #all tagged patients

        driver.find_element_by_xpath("//input[@id='tag-input-tokenfield']").click()
        driver.find_element_by_xpath("//input[@id='tag-input-tokenfield']").clear()
        driver.find_element_by_xpath(
            "//input[@id='tag-input-tokenfield']").send_keys("Pre Diabetic"+Keys.TAB)

        driver.find_element_by_xpath("//textarea[@id='body']").click()
        driver.find_element_by_xpath("//textarea[@id='body']").clear()
        driver.find_element_by_xpath("//textarea[@id='body']").send_keys("content" + str(i))

        driver.find_element_by_xpath(
            "//button[@class='apply-btn article-btn-width  outline-none margin-right-12 ']").click()

        time.sleep(3)

        if i % 4 == 0:
            driver.find_element_by_xpath(
                "//button[@class='apply-btn article-btn-width choose-patients outline-none margin-right-12 ']").click()
            driver.find_element_by_xpath("//input[@id='select-all']").click()
            driver.find_element_by_xpath("//button[@id='done']").click()
            driver.find_element_by_xpath("//button[@id='confirm-patients-btn']").click()
        else:
            driver.find_element_by_xpath("//button[@id='public-article-confirmation-btn']").click()

        assert driver.current_url == cfg["URL"]+"hospital/articles"

    def send_message(self, i, driver):
        '''verifies sending messages'''
        driver.find_element_by_xpath("//a[@href='/hospital/messages']").click()
        assert driver.current_url == cfg["URL"]+"/hospital/messages"

        driver.find_element_by_xpath("//textarea[@id='message']").click()
        driver.find_element_by_xpath("//textarea[@id='message']").clear()
        driver.find_element_by_xpath("//textarea[@id='message']").send_keys("message" + str(i))

        driver.find_element_by_xpath("//input[@id='select-all']").click()
        driver.find_element_by_xpath("//button[@id='done']").click()
        time.sleep(3)
        driver.find_element_by_xpath("//button[@id='confirm-patients-btn']").click()
        assert driver.current_url == cfg["URL"]+"/hospital/messages"

    def change_password(self, driver):
        '''verifies the changing of password'''
        driver.find_element_by_xpath("/html/body/header/div/div/div[2]/table/tbody/tr/td[2]/img").click()
        driver.find_element_by_xpath("/html/body/header/div/div/div[2]/ul/li/div[1]/div[2]/p[2]/a").click()
        assert driver.current_url == cfg["URL"] + "/hospital/change-password"

        passwd = cred["CMS"][0]["password"]
        driver.find_element_by_xpath('//*[@id="currentPassword"]').click()
        driver.find_element_by_xpath('//*[@id="currentPassword"]').clear()
        driver.find_element_by_xpath('//*[@id="currentPassword"]').send_keys(passwd)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="newPassword"]').click()
        driver.find_element_by_xpath('//*[@id="newPassword"]').clear()
        driver.find_element_by_xpath('//*[@id="newPassword"]').send_keys(passwd)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="confirmNewPassword"]').click()
        driver.find_element_by_xpath('//*[@id="confirmNewPassword"]').clear()
        driver.find_element_by_xpath('//*[@id="confirmNewPassword"]').send_keys(passwd)
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div/div/div/div[2]/form/div/button').click()

        driver.find_element_by_xpath('/html/body/div/div/p[2]/a').click()
        assert driver.current_url == cfg["URL"] + "/hospital/articles"
        assert driver.title == "Articles"


    def search(self, driver):
        '''verifies the search feature'''
        driver.find_element_by_xpath('//*[@id="search"]').click()
        driver.find_element_by_xpath('//*[@id="search"]').clear()
        driver.find_element_by_xpath('//*[@id="search"]').send_keys("title0")

        driver.find_element_by_xpath('//*[@id="search-icon"]').click()
        #assert driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/a/div/div/div[2]/p[1]').text() == "title0"
        #assert driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/a/div/div/div[2]/p[2]').text() == "content0"


    def edit_profile(self, driver):
        '''verifies editing profile'''
        driver.find_element_by_xpath(
            "//i[@class='fa fa-caret-down caret-down']").click()
        driver.find_element_by_xpath(
            "//button[@class='pull-left apply-btn outline-none margin-right-12']").click()
        assert driver.current_url == cfg["URL"]+"/hospital/profile"

        driver.find_element_by_xpath("//button[@class='apply-btn outline-none margin-right-12']").click()
        assert driver.current_url == cfg["URL"]+"/hospital/edit-profile"

        driver.find_element_by_xpath("//input[@id='firstName']").click()
        driver.find_element_by_xpath("//input[@id='firstName']").clear()
        driver.find_element_by_xpath("//input[@id='firstName']").send_keys("f")

        driver.find_element_by_xpath("//input[@id='lastName']").click()
        driver.find_element_by_xpath("//input[@id='lastName']").clear()
        driver.find_element_by_xpath("//input[@id='lastName']").send_keys("l")

        driver.find_element_by_xpath("//input[@id='hospitalName']").click()
        driver.find_element_by_xpath("//input[@id='hospitalName']").clear()
        driver.find_element_by_xpath("//input[@id='hospitalName']").send_keys("h")

        driver.find_element_by_xpath("//input[@id='phoneNumber']").click()
        driver.find_element_by_xpath("//input[@id='phoneNumber']").clear()
        driver.find_element_by_xpath("//input[@id='phoneNumber']").send_keys(1110000000)

        driver.find_element_by_xpath("//textarea[@id='address']").click()
        driver.find_element_by_xpath("//textarea[@id='address']").clear()
        driver.find_element_by_xpath("//textarea[@id='address']").send_keys("Address")
        time.sleep(2)
        driver.find_element_by_xpath("//button[@type='submit']").click()

        assert driver.current_url == cfg["URL"]+"/hospital/profile"
        driver.find_element_by_xpath("html/body/header/div/div/div[1]/a/img").click()
        
    def logout(self, driver):
        '''verifies logging out'''
        driver.find_element_by_xpath("html/body/header/div/div/div[2]/table/tbody/tr/td[3]/i").click()
        driver.find_element_by_xpath("html/body/header/div/div/div[2]/ul/li/div[2]/a[2]/button").click()

        assert driver.current_url == cfg["URL"]+"/login"

        return
