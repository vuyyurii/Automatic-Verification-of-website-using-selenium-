from __future__ import print_function
import time
import json
from selenium import webdriver
from assistant_doctor import Assistant_doctor

with open('../config.json') as json_data_file:
    cfg = json.load(json_data_file)

class test():

    def setup(self):
        self.driver = webdriver.Firefox()
        self.driver.get(cfg["URL"])
        #self.mail = Gmail_Api()
        #self.mail.initialize()

        

    def start(self):
        '''automation'''
        driver = self.driver
        m = 1
        count = 6


        ads = Assistant_doctor()
        print ("yes")
        ads.login(driver)
        print ("login successfully")
        time.sleep(4)


        #for i in range(4, 6):
        #    m = m + 1
        ads.as_patients(4, driver)
        print ("checked patients carefully")
        time.sleep(4)

        
        ads.profile(3, driver)
        print("checked profile carefully")
        time.sleep(3)



    def stop(self):
        self.driver.close()


if __name__ == "__main__":

    pro = test()
    pro.setup()
    pro.start()
    pro.stop()

