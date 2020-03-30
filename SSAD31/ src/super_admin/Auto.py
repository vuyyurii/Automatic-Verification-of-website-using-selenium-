from __future__ import print_function
from selenium import webdriver
from Gmail import Gmail_Api
from SuperAdmin import SuperAdmin
import time
import json


with open('../config.json') as json_data_file:
    cfg = json.load(json_data_file)


class test():

    def setup(self):

        # Opening the required URL and initializing the gmail api class
        self.driver = webdriver.Firefox()
        self.driver.get(cfg["URL"])
        self.gmail = Gmail_Api()
        self.gmail.initialize()

    def start(self):

        data = {}
        data['Hos_Ad'] = []
        data['Staff'] = []
        driver = self.driver

        # Login as Super Admin with credentials from config file
        superadmin = SuperAdmin()
        superadmin.login(driver)

        # for adding hospitals according to config file count
        for i in range(cfg["Hospital_Count"]):
            superadmin.add_hospital(i, driver)
        print("Add Hospital Function is Successful")
        time.sleep(20)

        # Get credentials from gmail using Gmail API
        self.gmail.get_allrequired(
            'me',
            'from:do-not-reply@onwardhealth.co is:unread',
            data,
            'Hos_Ad')

        # For adding Call Center Staff. No  of objects given in config file.
        for i in range(cfg["Staff_Count"]):
            superadmin.add_staff(i, driver)
        print("Add Staff Function is Successful")
        time.sleep(20)

        # Get credentials from gmail using Gmail API
        self.gmail.get_allrequired(
            'me', 'from:do-not-reply@onwardhealth.co is:unread', data, 'Staff')

        # Redirect all credentials of the users to a file in json format
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)

        # For Checking Functioning Of Password Change Feature
        superadmin.password_change(driver)

        superadmin.search(driver)

        superadmin.edit(driver)

        # superAdmin.deactivate(driver)

    def stop(self):

        self.driver.close()


if __name__ == "__main__":

    pro = test()
    pro.setup()
    pro.start()
    pro.stop()
