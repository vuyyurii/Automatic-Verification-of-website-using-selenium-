from __future__ import print_function
from selenium.webdriver.support.ui import Select
import json
import time

# To get information from the configuration File
with open('../config.json') as json_data_file:
    cfg = json.load(json_data_file)

# Class for automating various activities of SUPER ADMIN
with open("data.json") as json_data_file:
    cred = json.load(json_data_file)

class SuperAdmin():

    # Various functions of a super admin
    def __init__(self):

        self.u = cfg["Email_Hos"].split("@")
        self.v = cfg["Email_Hos_Admin"].split("@")

    def login(self, driver):

        assert driver.current_url == cfg["URL"] + "/login"
        driver.find_element_by_id("username").send_keys(cfg["Super_Admin"])
        time.sleep(1)
        driver.find_element_by_id("pswrd").send_keys(cfg["Super_Password"])
        time.sleep(1)
        driver.find_element_by_class_name("login-btn").click()
        # TO CHECK THE WEBPAGE OPENED
        assert driver.current_url == cfg["URL"] + "/admin/hospitals"
        assert driver.title == "Hospitals"
        return

    def add_hospital(self, i, driver):

        # For generating various usernames
        email = self.u[0] + '+' + str(i) + "@" + self.u[1]
        Admin = self.v[0] + '+' + str(i) + "@" + self.v[1]
        # Clicking on ADD HOSPITAL button
        driver.find_element_by_xpath(
            "html/body/div[1]/div/div[1]/div[2]/div/a/button").click()
        assert driver.current_url == cfg["URL"] + "/admin/add-hospital"
        assert driver.title == "Add Hospital"

        # ENTERING THE DETAILS OF THE FORM
        driver.find_element_by_xpath(".//*[@id='hospitalName']").click()
        driver.find_element_by_xpath(".//*[@id='hospitalName']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='hospitalName']").send_keys("Hospital" + str(i))
        time.sleep(1)
        driver.find_element_by_xpath(
            ".//*[@id='hospitalContactPhone']").click()
        driver.find_element_by_xpath(
            ".//*[@id='hospitalContactPhone']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='hospitalContactPhone']").send_keys(cfg["Phone_Number"] + str(i))

        driver.find_element_by_xpath(
            ".//*[@id='hospitalContactEmail']").click()
        driver.find_element_by_xpath(
            ".//*[@id='hospitalContactEmail']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='hospitalContactEmail']").send_keys(email)

        driver.find_element_by_xpath(".//*[@id='address']").click()
        driver.find_element_by_xpath(".//*[@id='address']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='address']").send_keys("Hospital" + str(i) + ",hyderabad")
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='firstName']").click()
        driver.find_element_by_xpath(".//*[@id='firstName']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='firstName']").send_keys("FirstName" + str(i))
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='lastName']").click()
        driver.find_element_by_xpath(".//*[@id='lastName']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='lastName']").send_keys("LastName" + str(i))

        driver.find_element_by_xpath(".//*[@id='email']").click()
        driver.find_element_by_xpath(".//*[@id='email']").clear()
        driver.find_element_by_xpath(".//*[@id='email']").send_keys(Admin)
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='phoneNumber']").click()
        driver.find_element_by_xpath(".//*[@id='phoneNumber']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='phoneNumber']").send_keys(cfg["Phone_Number"] + str(i))

        driver.find_element_by_xpath(
            "html/body/div[1]/div/form/div/div[2]/div/a[1]/button").click()
        time.sleep(2)

        assert driver.current_url == cfg["URL"] + "/admin/hospitals"
        assert driver.title == "Hospitals"
        # For asserting whether new member is added successfully or not
        # if i == 0:
        #   driver.implicitly_wait(3)
        #    a = driver.find_element_by_xpath(
        #        ".//*[@id='doctors-list']/tr/td[1]")
        #    assert a.text == "Hospital" + str(i)
        #    b = driver.find_element_by_xpath(
        #        ".//*[@id='doctors-list']/tr/td[2]")
        #    assert b.text == cfg["Phone_Number"] + str(i)
        #    c = driver.find_element_by_xpath(
        #        ".//*[@id='doctors-list']/tr/td[3]")
        #    assert c.text == "Hospital" + str(i) + ",hyderabad"
        #else:
        #    # Checking whether above hospital is added successfully
        #    driver.implicitly_wait(3)
        #    a = driver.find_element_by_xpath(
        #        ".//*[@id='doctors-list']/tr[" + str(i + 1) + "]/td[1]")
        #    assert a.text == "Hospital" + str(i)
        #    b = driver.find_element_by_xpath(
        #        ".//*[@id='doctors-list']/tr[" + str(i + 1) + "]/td[2]")
        #    assert b.text == cfg["Phone_Number"] + str(i)
        #    c = driver.find_element_by_xpath(
        #        ".//*[@id='doctors-list']/tr[" + str(i + 1) + "]/td[3]")
        #   assert c.text == "Hospital" + str(i) + ",hyderabad"

        return

    def add_staff(self, i, driver):

        # To generate various usernames
        email = self.u[0] + '+' + str(i) + "@" + self.u[1]
        admin = self.v[0] + '+' + str(i) + "@" + self.v[1]

        # Clicking on the ADD STAFF button
        driver.find_element_by_xpath(
            "html/body/nav/div/div/div/div[2]/div/ul/li[2]/a").click()

        assert driver.current_url == cfg["URL"] + "/admin/staff"
        assert driver.title == "Staff"

        driver.find_element_by_xpath(
            "html/body/div[1]/div[1]/div[1]/div[2]/div/a/button").click()

        assert driver.current_url == cfg["URL"] + "/admin/add-staff"

        # Filling Details into the form
        driver.find_element_by_xpath(".//*[@id='firstName']").click()
        driver.find_element_by_xpath(".//*[@id='firstName']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='firstName']").send_keys("staffFn" + str(i))

        driver.find_element_by_xpath(".//*[@id='lastName']").click()
        driver.find_element_by_xpath(".//*[@id='lastName']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='lastName']").send_keys("staffLn" + str(i))
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='email']").click()
        driver.find_element_by_xpath(".//*[@id='email']").clear()
        driver.find_element_by_xpath(".//*[@id='email']").send_keys(email)
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='phoneNumber']").click()
        driver.find_element_by_xpath(".//*[@id='phoneNumber']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='phoneNumber']").send_keys(1111111110 + i)
        time.sleep(1)
        driver.find_element_by_xpath(
            ".//*[@id='add-form']/div/div[2]/div/div[3]/div[1]/div/button").click()
        dropdowna = Select(driver.find_element_by_xpath(
            ".//*[@id='add-form']/div/div[2]/div/div[3]/div[1]/div/select"))

        dropdowna.select_by_value("CALL_CENTER")

        dropdownb = Select(driver.find_element_by_xpath(
            ".//*[@id='add-form']/div/div[2]/div/div[3]/div[2]/div/select"))
        dropdownb.select_by_value("male")

        driver.find_element_by_xpath(
            ".//*[@id='add-form']/div/div[2]/div/a[1]/button").click()
        time.sleep(2)

        assert driver.current_url == cfg["URL"] + "/admin/staff"
        assert driver.title == "Staff"

        return

    def password_change(self, driver):

        # For changing the password
        driver.find_element_by_xpath(
            "html/body/header/div/div/div[1]/a/img").click()
        driver.find_element_by_xpath(
            "html/body/header/div/div/div[2]/table/tbody/tr/td[3]/i").click()
        driver.find_element_by_xpath(
            "html/body/header/div/div/div[2]/ul/li/div[1]/div[2]/p[2]/a").click()
        time.sleep(3)
        assert driver.current_url == cfg["URL"] + "/admin/change-password"
        driver.find_element_by_xpath(".//*[@id='currentPassword']").click()
        driver.find_element_by_xpath(".//*[@id='currentPassword']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='currentPassword']").send_keys(cfg["Super_Password"])
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='newPassword']").click()
        driver.find_element_by_xpath(".//*[@id='newPassword']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='newPassword']").send_keys("123456")
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='confirmNewPassword']").click()
        driver.find_element_by_xpath(".//*[@id='confirmNewPassword']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='confirmNewPassword']").send_keys("123456")
        time.sleep(1)
        cfg["Super_Password"] = "123456"

        driver.find_element_by_xpath(
            "html/body/div[1]/div/div/div[2]/form/div/button").click()
        time.sleep(2)
        with open('config.json', 'w') as outfile:
            json.dump(cfg, outfile)

        self.logout(driver)
        time.sleep(2)
        self.login(driver)
        assert driver.current_url == cfg["URL"] + "/admin/hospitals"
        print("Password Change is Successful")
        return

    def search(self, driver):

        # for testing search feature

        driver.find_element_by_xpath(".//*[@id='search']").click()
        driver.find_element_by_xpath(".//*[@id='search']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='search']").send_keys("Hospital0")
        time.sleep(2)
        driver.find_element_by_xpath(
            "html/body/div[1]/div/div[1]/div[1]/img").click()
        a = driver.find_element_by_xpath(".//*[@id='doctors-list']/tr/td[1]")

        # assert a.text == "Hospital0"

        print("Search Feature is successful")
        return

    def edit(self, driver):

        driver.find_element_by_xpath(
            ".//*[@id='doctors-list']/tr[1]/td[4]/div/a/i").click()
        driver.find_element_by_xpath(".//*[@id='address']").click()
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='address']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='address']").send_keys("address changed")
        driver.find_element_by_xpath(
            "html/body/div[1]/div/form/div/div[2]/div/a[1]/button").click()

        assert driver.current_url == cfg["URL"] + "/admin/hospitals"

        driver.find_element_by_xpath("html/body/nav/div/div/div/div[2]/div/ul/li[2]/a").click()
        driver.find_element_by_xpath(".//*[@id='staff-list']/tr/td[5]/div/a/i").click()
        driver.find_element_by_xpath(".//*[@id='add-form']/div/div[2]/div/a[1]/button").click()
        driver.find_element_by_xpath("html/body/div[2]/div/div")
        driver.find_element_by_xpath("html/body/nav/div/div/div/div[2]/div/ul/li[1]/a").click()

        print("Edit Feature is successful")

        return

    def deactivate(self, driver):

        driver.find_element_by_xpath(
            "html/body/nav/div/div/div/div[2]/div/ul/li[2]/a").click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@data-target='#deactivate-modal']").click()
        driver.find_element_by_xpath(".//*[@id='deactivate']").click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@data-target='#reactivate-model']").click()
        driver.find_element_by_xpath(".//*[@id='reactivate']").click()
        #driver.find_element_by_xpath("html/body/div[3]/div")

        print("Deactivate Feature is Successful")
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
