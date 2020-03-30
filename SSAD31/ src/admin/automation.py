from __future__ import print_function
import time
import json
from selenium import webdriver
from Gmail import Gmail_Api
from hos_admin import admin

with open('../config.json') as json_data_file:
    cfg = json.load(json_data_file)


class test():

    def __init__(self):
        """create driver connection and initialize mail"""
        self.driver = webdriver.Firefox()
        self.driver.get(cfg["URL"])
        self.gmail = Gmail_Api()
        self.gmail.initialize()

    def start(self):
        """automation"""
        data = {}
        data['Doc'] = []
        data['CMS'] = []
        data['Assistant'] = []
        driver = self.driver
        m = 1

        # Login as Super Admin with credentials from config file
        adm = admin()
        adm.login(driver)

        time.sleep(2)

        # for adding staff according to config file count
        for i in range(cfg["Doc_Count"]):
            adm.add_staff(i, driver, "DOCTOR")
        print("Doctor added successfully")
        time.sleep(10)
        self.gmail.get_allrequired(
            'me', 'from:do-not-reply@onwardhealth.co is:unread', data, 'Doc')

        for i in range(cfg["Doc_Count"], cfg["Doc_Count"] + cfg["Cms_Count"]):
            adm.add_staff(i, driver, "HOSPITAL_CMS")
        print("CMS staff added successfully")
        time.sleep(10)
        self.gmail.get_allrequired(
            'me', 'from:do-not-reply@onwardhealth.co is:unread', data, 'CMS')

        for i in range(cfg["Cms_Count"] + cfg["Doc_Count"],
                       cfg["Assist_Count"] + cfg["Cms_Count"] + cfg["Doc_Count"]):
            adm.add_staff(i, driver, "DOCTOR_ASSISTANT")
        print("Assistant staff added successfully")
        time.sleep(10)
        # Get credentials from gmail using Gmail API
        self.gmail.get_allrequired(
            'me',
            'from:do-not-reply@onwardhealth.co is:unread',
            data,
            'Assistant')

        # Redirect all credentials of the users to a file in json format
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)

            # for adding patients
        for i in range(1, cfg["Patient_Count"]):
            m = m + 1
            adm.add_patient(i, m, driver)
        print("Patient added successfully")
        time.sleep(5)

        adm.add_video(1, driver)
        print("Video added successfully")
        time.sleep(5)

        adm.message(0, driver)
        print("Message send successfully")
        time.sleep(5)

        adm.add_article(1, driver)
        time.sleep(2)

        adm.logout(driver)


    def stop(self):

        self.driver.close()


if __name__ == "__main__":

    pro = test()
    pro.start()
    pro.stop()
