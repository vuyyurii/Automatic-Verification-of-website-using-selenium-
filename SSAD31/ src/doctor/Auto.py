from __future__ import print_function
import time
import json
from selenium import webdriver
from Gmail import Gmail_Api
from doctor import doctor

with open('../config.json') as json_data_file:
    cfg = json.load(json_data_file)


class test():

    def setup(self):

        # OPening the required URL and initializing the gmail api class
        self.driver = webdriver.Firefox()
        self.driver.get(cfg["URL"])
        self.gmail = Gmail_Api()
        self.gmail.initialize()

    def start(self):

        driver = self.driver

        doc = doctor()
        doc.login(driver)

        doc.manage(driver)
        print("Manage Assitance feature is successful")

        doc.view_notify(driver)
        print("View Notifications feature is successful")

    def stop(self):

        self.driver.close()


if __name__ == "__main__":

    pro = test()
    pro.setup()
    pro.start()
    pro.stop()
