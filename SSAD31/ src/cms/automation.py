import time
import json
from selenium import webdriver
from cms import CMS

with open('../config.json') as json_data_file:
    cfg = json.load(json_data_file)


class test():

    def __init__(self):
        '''create driver connection and initialize mail'''
        self.driver = webdriver.Firefox()
        self.driver.get(cfg["URL"])

    def start(self):
        '''automation'''
        data = {}
        data['article'] = []
        driver = self.driver

        # Login as Hospital CMS
        c = CMS()
        c.login(driver)


        #for adding messages
        for i in range(1, cfg["message_count"]):
            c.send_message(1, driver)
            time.sleep(3)
        print("Messages sent successfully")
        time.sleep(3)

        c.change_password(driver)
        print("Password changed successfully")
        time.sleep(3)

        c.edit_profile(driver)
        print("Profile edited successfully")
        time.sleep(3)

        c.search(driver)
        print("Articles searched successfully")
        time.sleep(3)

        c.logout(driver)

    def stop(self):

        self.driver.close()


if __name__ == "__main__":

    pro = test()
    pro.start()
    pro.stop()
