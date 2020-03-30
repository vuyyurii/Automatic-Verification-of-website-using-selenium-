import time
import json
from selenium import webdriver
from call_center_staff import staff

with open('../config.json') as json_data_file:
    cfg = json.load(json_data_file)

class test():

    def __init__(self):
        '''create driver connection and initialize mail'''
        self.driver = webdriver.Firefox()
        self.driver.get(cfg["URL"])


    def start(self):
        s = staff()
        driver = self.driver
        s.login(driver)

        #for i in range(0, cfg["Patient_Count"]):
        #    s.view_patients(i, driver)
        #print("Patients displayed successfully")

        time.sleep(3)

        s.change_password(driver)
        print("Password changed successfully")

        time.sleep(3)
        s.logout(driver)


    def stop(self):
        self.driver.close()


if __name__ == "__main__":
    pro = test()
    pro.start()
    pro.stop()
