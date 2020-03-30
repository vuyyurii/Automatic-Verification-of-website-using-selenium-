from __future__ import print_function
import json
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

with open('../config.json') as json_data_file:
    cfg = json.load(json_data_file)

with open('../hospital_admin/data.json') as json_file:
    cred = json.load(json_file)


class doctor():

    def login(self, driver):

        uname = cred["Doc"][0]["username"]
        passwd = cred["Doc"][0]["password"]
        assert driver.current_url == cfg["URL"] + "/login"
        driver.find_element_by_id("username").send_keys(uname)
        driver.find_element_by_id("pswrd").send_keys(passwd)
        driver.find_element_by_class_name("login-btn").click()
        # TO CHECK THE WEBPAGE OPENED
        assert driver.current_url == cfg["URL"] + "/doctor/patients"
        assert driver.title == "Dashboard"
        return

    def manage(self, driver):

        driver.find_element_by_xpath(
            "html/body/div[2]/div[1]/div[1]/div[2]/div/a/button").click()

        assert driver.current_url == cfg["URL"] + "/doctor/assistants"
        assert driver.title == "Manage Assistance"

        driver.find_element_by_xpath(
            ".//*[@id='searchForPatientText']").click()
        driver.find_element_by_xpath(".//*[@id='searchForPatientText']").send_keys("AsFn" + str(
            cfg["Cms_Count"] + cfg["Doc_Count"]) + ' ' + "AsLn" + str(cfg["Cms_Count"] + cfg["Doc_Count"]))

        time.sleep(5)
        # xpath = "//ul[contains(@class, 'ui-autocomplete')]/li[1]/div"
        driver.find_element_by_class_name("ui-menu-item-wrapper").click()

        # driver.find_element_by_xpath("//*[contains(text(), 'AsFn')]").click()

        driver.find_element_by_xpath(".//*[@id='add']").click()

        driver.find_element_by_xpath(".//*[@id='confirm-dialog-btn']").click()

        #a = driver.find_element_by_xpath(
        #    ".//*[@id='assistants-table-body']/tr[2]/td[1]")

        #assert a.text == "AsFn" + str(cfg["Cms_Count"] + cfg["Doc_Count"]) + \
        #    ' ' + "AsLn" + str(cfg["Cms_Count"] + cfg["Doc_Count"])

        time.sleep(3)

        driver.find_element_by_xpath(
            ".//*[@id='assistants-table-body']/tr/td[2]/a/button").click()
        driver.find_element_by_xpath(
            ".//*[@id='remove-access-dialog-confirm-btn']").click()
        driver.find_element_by_xpath("html/body/div[6]/div/div")

        driver.find_element_by_xpath(
            "html/body/nav/div/div/div/div[1]/ul/li[1]/a").click()
        # time.sleep(1)

        return

    def view_notify(self, driver):

        driver.find_element_by_xpath(
            "html/body/nav/div/div/div/div[1]/ul/li[1]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath(
            "html/body/nav[2]/div/div/div/div[3]/div/ul/li[2]/a").click()
        assert driver.current_url == cfg["URL"] + \
            "/doctor/notifications/messages"

        return

    def logout(self, driver):

        # For log out
        driver.find_element_by_xpath(
            "html/body/header/div/div/div[1]/a/img").click()
        assert driver.current_url == cfg["URL"] + "/admin/hospitals"

        driver.find_element_by_xpath(
            "html/body/header/div/div/div[2]/table/tbody/tr/td[3]/i").click()
        driver.find_element_by_xpath(
            "html/body/header/div/div/div[2]/ul/li/div[2]/a/button").click()
        return
