from __future__ import print_function
import json
import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import datetime
import pyatspi

'''get info from config file'''
with open('../config.json') as json_data_file:
    cfg = json.load(json_data_file)

with open('../super_admin/data.json') as json_file:
    cred = json.load(json_file)


class admin():

    def __init__(self):

        self.e1 = cfg["Email_Doc"].split("@")
        self.e2 = cfg["Email_Assist"].split("@")
        self.e3 = cfg["Email_Cms"].split("@")
        self.pat = cfg["Email_Patient"].split("@")
        self.arr = []

    def login(self, driver):

        uname = cred["Hos_Ad"][0]["username"]
        passwd = cred["Hos_Ad"][0]["password"]
        assert driver.current_url == cfg["URL"] + "/login"
        driver.find_element_by_id("username").send_keys(uname)
        driver.find_element_by_id("pswrd").send_keys(passwd)
        time.sleep(1)
        driver.find_element_by_class_name("login-btn").click()
        # TO CHECK THE WEBPAGE OPENED
        assert driver.current_url == cfg["URL"] + "/hospital/staff"
        assert driver.title == "Staff"
        return

    def add_staff(self, i, driver, type):

        if type == "DOCTOR":
            email = self.e1[0] + '+' + str(i) + "@" + self.e1[1]
            fname = "DocFn"
            lname = "DocLn"
        elif type == "HOSPITAL_CMS":
            email = self.e3[0] + '+' + str(i) + "@" + self.e3[1]
            fname = "CmsFn"
            lname = "CmsLn"
        else:
            email = self.e2[0] + '+' + str(i) + "@" + self.e2[1]
            fname = "AsFn"
            lname = "AsLn"

        # Clicking on the ADD STAFF button
        driver.find_element_by_xpath(
            "/html/body/div/div[1]/div[1]/div[2]/div/a/button").click()

        assert driver.current_url == cfg["URL"] + "/hospital/staff/add-staff"
        # Filling Details into the form
        driver.find_element_by_xpath(".//*[@id='firstName']").click()
        driver.find_element_by_xpath(".//*[@id='firstName']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='firstName']").send_keys(fname + str(i))

        driver.find_element_by_xpath(".//*[@id='lastName']").click()
        driver.find_element_by_xpath(".//*[@id='lastName']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='lastName']").send_keys(lname + str(i))
        time.sleep(1)
        driver.find_element_by_xpath(
            "html/body/div[1]/div/form/div/div[2]/div/div[2]/div[1]/div/button").click()
        dropdowna = Select(
            driver.find_element_by_xpath("html/body/div[1]/div/form/div/div[2]/div/div[2]/div[1]/div/select"))

        dropdowna.select_by_value(type)

        driver.find_element_by_xpath(
            ".//*[@id='hospitalIdentificationNumber']").click()
        driver.find_element_by_xpath(
            ".//*[@id='hospitalIdentificationNumber']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='hospitalIdentificationNumber']").send_keys(i)

        driver.find_element_by_xpath(".//*[@id='phoneNumber']").click()
        driver.find_element_by_xpath(".//*[@id='phoneNumber']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='phoneNumber']").send_keys(1100000000 + i)

        driver.find_element_by_xpath(".//*[@id='email']").click()
        driver.find_element_by_xpath(".//*[@id='email']").clear()
        driver.find_element_by_xpath(".//*[@id='email']").send_keys(email)

        driver.find_element_by_xpath(
            ".//*[@id='qualification-tokenfield']").click()
        driver.find_element_by_xpath(
            ".//*[@id='qualification-tokenfield']").send_keys("MBBS")
        driver.find_element_by_class_name("ui-menu-item").click()
        driver.find_element_by_xpath("//*[contains(text(), 'MBBS')]").click()

        driver.find_element_by_xpath(
            "html/body/div[1]/div/form/div/div[2]/div/div[4]/div[1]/div/input[3]").click()
        driver.find_element_by_xpath(
            "html/body/div[1]/div/form/div/div[2]/div/div[4]/div[2]/div/button").click()

        dropdownb = Select(
            driver.find_element_by_xpath("html/body/div[1]/div/form/div/div[2]/div/div[4]/div[2]/div/select"))
        if i % 4 == 0:
            dropdownb.select_by_value("Rheumatologist")
        elif i % 4 == 1:
            dropdownb.select_by_value("Orthopedic Surgeon")
        elif i % 4 == 2:
            dropdownb.select_by_value("Orthopedic")
        else:
            dropdownb.select_by_value("Surgeon")

        driver.find_element_by_xpath(".//*[@id='mciId']").click()
        driver.find_element_by_xpath(".//*[@id='mciId']").clear()
        driver.find_element_by_xpath(".//*[@id='mciId']").send_keys(i)
        time.sleep(1)

        driver.find_element_by_xpath(
            "html/body/div[1]/div/form/div/div[2]/div/a[1]/button").click()

        assert driver.current_url == cfg["URL"] + "/hospital/staff"
        assert driver.title == "Staff"

        driver.implicitly_wait(3)
        if i == 0:
            a = driver.find_element_by_xpath(
                ".//*[@id='doctors-list']/tr/td[1]")
        else:
            a = driver.find_element_by_xpath(
                ".//*[@id='doctors-list']/tr[" + str(i + 1) + "]/td[1]")
        if type == "DOCTOR":
            assert a.text == (
                "Dr." +
                ' ' +
                fname +
                str(i) +
                ' ' +
                lname +
                str(i))
        else:
            assert a.text == (fname + str(i) + ' ' + lname + str(i))

        if i == 0:
            a = driver.find_element_by_xpath(
                ".//*[@id='doctors-list']/tr/td[2]")
        else:
            a = driver.find_element_by_xpath(
                ".//*[@id='doctors-list']/tr[" + str(i + 1) + "]/td[2]")
        if type == "HOSPITAL_CMS":
            assert a.text == "CMS"
        elif type == "DOCTOR_ASSISTANT":
            assert a.text == "Doctor Assistant"
        else:
            assert a.text == "Doctor"

        if i == 0:
            a = driver.find_element_by_xpath(
                ".//*[@id='doctors-list']/tr/td[3]")
        else:
            a = driver.find_element_by_xpath(
                ".//*[@id='doctors-list']/tr[" + str(i + 1) + "]/td[3]")
        assert a.text == str(1100000000 + i)

        return

    def add_video(self, i, driver):

        if i == 1:
            driver.find_element_by_xpath(
                "html/body/nav[2]/div/div/div/div[2]/div/ul/li[3]/a").click()
        assert driver.current_url == cfg["URL"] + "/hospital/videos"
        assert driver.title == "Videos"

        driver.find_element_by_xpath(
            "html/body/div[1]/div/div[1]/div[2]/div/button").click()
        assert driver.current_url == cfg["URL"] + "/hospital/videos"
        driver.find_element_by_xpath(
            "html/body/div[2]/div/div/div/div/div/div[2]/form/div/div[1]/input").click()
        driver.find_element_by_xpath(
            "html/body/div[2]/div/div/div/div/div/div[2]/form/div/div[1]/input").clear()
        driver.find_element_by_xpath(
            "html/body/div[2]/div/div/div/div/div/div[2]/form/div/div[1]/input").send_keys("video" + str(i))
        time.sleep(1)
        driver.find_element_by_xpath(
            "html/body/div[2]/div/div/div/div/div/div[2]/form/div/div[2]/input").click()
        driver.find_element_by_xpath(
            "html/body/div[2]/div/div/div/div/div/div[2]/form/div/div[2]/input").clear()
        driver.find_element_by_xpath(
            "html/body/div[2]/div/div/div/div/div/div[2]/form/div/div[2]/input").send_keys("tag" + str(i))
        time.sleep(1)
        driver.find_element_by_xpath(
            "html/body/div[2]/div/div/div/div/div/div[2]/form/div/div[3]/input").click()
        driver.find_element_by_xpath(
            "html/body/div[2]/div/div/div/div/div/div[2]/form/div/div[3]/input").clear()
        driver.find_element_by_xpath(
            "html/body/div[2]/div/div/div/div/div/div[2]/form/div/div[3]/input").send_keys(cfg["video"])

        driver.find_element_by_xpath(
            "html/body/div[2]/div/div/div/div/div/div[2]/form/div/button[1]").click()
        time.sleep(1)
        assert driver.current_url == cfg["URL"] + "/hospital/videos"
        assert driver.title == "Videos"

        return

    def add_article(self, i, driver):

        driver.find_element_by_xpath(
            "html/body/nav/div/div/div/div[2]/div/ul/li[4]/a").click()
        #assert driver.current_url == cfg["URL"] + "/hospital/articles"
        #assert driver.title == "Articles"

        driver.find_element_by_xpath(
            "html/body/div[1]/div/div[1]/div[2]/div/a/button").click()
        #assert driver.current_url == cfg["URL"] + "/hospital/add-article"

        # driver.find_element_by_xpath(".//*[@id='article-image-preview']").click()
        # driver.find_element_by_xpath(".//*[@id='article-image-preview']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='article-image-preview']").send_keys(os.getcwd() + "/image_gallery.jpeg")

        driver.find_element_by_xpath(".//*[@id='title']").click()
        driver.find_element_by_xpath(".//*[@id='title']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='title']").send_keys(cfg["Article"])

        driver.find_element_by_xpath(
            ".//*[@id='article']/div[1]/div[2]/div[2]/div[2]/div/button").click()
        dropdowna = Select(driver.find_element_by_xpath(
            ".//*[@id='article']/div[1]/div[2]/div[2]/div[2]/div/select"))
        dropdowna.select_by_value("true")

        driver.find_element_by_xpath(
            ".//*[@id='tag-input-tokenfield']").click()
        driver.find_element_by_xpath(
            ".//*[@id='tag-input-tokenfield']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='tag-input-tokenfield']").send_keys("General Wellness")

        driver.find_element_by_xpath(".//*[@id='body']").clear()
        driver.find_element_by_xpath(
            ".//*[@id='body']").send_keys("content" + str(i))

        driver.find_element_by_xpath(
            ".//*[@id='article']/div[2]/div[2]/button[1]").click()

        #assert driver.current_url == cfg["URL"] + "/hospital/articles"
        #assert driver.title == "Articles"

        return

    def medication_info(self, i, m, driver):

        driver.find_element_by_xpath('//*[@id="new_div"]').click()

        h = i + 1
        driver.find_element_by_xpath('//*[@id="drug-name"]').send_keys('Bisacodyl')

        driver.find_element_by_xpath('//*[@id="drug-course-period"]').click()
        a = str(200) + str(h)
        driver.find_element_by_xpath('/html/body/div[18]/div[1]/div[1]/input').clear()
        driver.find_element_by_xpath('/html/body/div[18]/div[1]/div[1]/input').send_keys('23-5-' + a)
        driver.find_element_by_xpath('/html/body/div[18]/div[2]/div[1]/input').clear()
        driver.find_element_by_xpath('/html/body/div[18]/div[2]/div[1]/input').send_keys('23-6-' + a)

        aw1 = driver.find_element_by_xpath('/html/body/div[18]/div[1]/div[2]/table/tbody/tr[3]/td[1]')
        aw2 = driver.find_element_by_xpath('/html/body/div[18]/div[2]/div[2]/table/tbody/tr[3]/td[3]')
        ActionChains(driver).move_to_element(aw1).click_and_hold().perform()
        #ActionChains(driver).move_to_element(aw1).clear()
        #time.sleep(3)
        aw2 = driver.find_element_by_xpath('/html/body/div[18]/div[2]/div[2]/table/tbody/tr[3]/td[3]')
        ActionChains(driver).move_to_element(aw2).click().perform()
        driver.find_element_by_xpath('/html/body/div[18]/div[3]/div/button[1]').click()        

        driver.find_element_by_xpath('//*[@id="drug"]/div/div[3]/div[1]/div/button')
        sd1 = Select(driver.find_element_by_xpath('//*[@id="drug-type"]'))
        if i % 3 == 0:
            sd1.select_by_value("tablet")
            driver.find_element_by_xpath("//*[@id='select-div']/div/button").click()
            sd2 = Select(driver.find_element_by_xpath("//*[@id='drug-dosage']"))
            if m % 4 == 0:
                sd2.select_by_value("1 pill")
            elif m % 4 == 1:
                sd2.select_by_value("2 pills")
            elif m % 4 == 2:
                sd2.select_by_value("3 pills")
            elif m % 4 == 3:
                sd2.select_by_value("4 pills")

        elif i % 3 == 1:
            sd1.select_by_value("syrup")
            driver.find_element_by_xpath("//*[@id='select-div']/div/button").click()
            sd2 = Select(driver.find_element_by_xpath("//*[@id='drug-dosage']"))
            if m % 6 == 0:
                sd2.select_by_value("5 ml")
            elif m % 6 == 1:
                sd2.select_by_value("10 ml")
            elif m % 6 == 2:
                sd2.select_by_value("15 ml")
            elif m % 6 == 3:
                sd2.select_by_value("20 ml")
            elif m % 6 == 4:
                sd2.select_by_value("25 ml")
            elif m % 6 == 5:
                sd2.select_by_value("Others")

        elif i % 3 == 2:
            sd1.select_by_value("injection")
            driver.find_element_by_xpath("//*[@id='select-div']/div/button").click()
            sd2 = Select(driver.find_element_by_xpath("//*[@id='drug-dosage']"))
            if m % 5 == 0:
                sd2.select_by_value("1 unit")
            elif m % 5 == 1:
                sd2.select_by_value("2 units")
            elif m % 5 == 2:
                sd2.select_by_value("3 units")
            elif m % 5 == 3:
                sd2.select_by_value("4 units")
            elif m % 5 == 4:
                sd2.select_by_value("Others")

        driver.find_element_by_xpath("//*[@id='drug']/div/div[4]/div/button").click()
        sd3 = Select(driver.find_element_by_xpath("//*[@id='drug-frequency']"))
        if i % 7 == 0:
            sd3.select_by_value("1-0-0")
        elif i % 7 == 1:
            sd3.select_by_value("1-1-0")
        elif i % 7 == 2:
            sd3.select_by_value("0-1-0")
        elif i % 7 == 3:
            sd3.select_by_value("0-1-1")
        elif i % 7 == 4:
            sd3.select_by_value("0-0-1")
        elif i % 7 == 5:
            sd3.select_by_value("1-0-1")
        elif i % 7 == 6:
            sd3.select_by_value("1-1-1")

        driver.find_element_by_xpath("//*[@id='drug']/div/div[5]/div/button").click()
        sd4 = Select(driver.find_element_by_xpath("//*[@id='drug-food-intake']"))
        if i % 2 == 0:
            sd4.select_by_value("Before Food")
        else:
            sd4.select_by_value("After Food")
        d1 = driver.find_element_by_xpath("//*[@id='drug-sos']")
        if i % 2 == 0:
            d1.click()
        driver.find_element_by_xpath('//*[@id="drug-notes"]').send_keys("The drug should be taken at proper time and expiry-date should be checked")
        driver.find_element_by_xpath('//*[@id="dsaf"]').click()
        return


    def activity_info(self, i, m, driver):

        driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[5]/div[3]/ul/li/a').click()
        time.sleep(8)
        h = i + 5
        driver.find_element_by_xpath('//*[@id="activity-name"]').clear()
        driver.find_element_by_xpath('//*[@id="activity-name"]').send_keys("Ac" + Keys.TAB)

        driver.find_element_by_xpath('//*[@id="activity-course-period"]').click()
        a = str(200) + str(h)

        driver.find_element_by_xpath('/html/body/div[19]/div[1]/div[1]/input').clear()
        driver.find_element_by_xpath('/html/body/div[19]/div[1]/div[1]/input').send_keys('24-2-' + a)
        driver.find_element_by_xpath('/html/body/div[19]/div[2]/div[1]/input').clear()
        driver.find_element_by_xpath('/html/body/div[19]/div[2]/div[1]/input').send_keys('20-3-' + a)

        aw1 = driver.find_element_by_xpath('/html/body/div[19]/div[1]/div[2]/table/tbody/tr[3]/td[6]')
        aw2 = driver.find_element_by_xpath('/html/body/div[19]/div[2]/div[2]/table/tbody/tr[4]/td[3]')
        ActionChains(driver).move_to_element(aw1).click_and_hold().perform()
        time.sleep(3)
        aw2 = driver.find_element_by_xpath('/html/body/div[19]/div[2]/div[2]/table/tbody/tr[4]/td[3]')
        ActionChains(driver).move_to_element(aw2).click().perform()
        #time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[19]/div[3]/div/button[1]').click()
        d1 = Select(driver.find_element_by_xpath('//*[@id="activity-type"]'))
        if i % 6 == 0:
            d1.select_by_value("activity")
            driver.find_element_by_xpath('//*[@id="activity"]/div/div[3]/div[2]/div/button').click()
            d2 = Select(driver.find_element_by_xpath('//*[@id="activity-duration"]'))
            if m % 6 == 0:
                d2.select_by_value("10 Min")
            elif m % 6 == 1:
                d2.select_by_value("15 Min")
            elif m % 6 == 2:
                d2.select_by_value("20 Min")
            elif m % 6 == 3:
                d2.select_by_value("25 Min")
            elif m % 6 == 4:
                d2.select_by_value("30 Min")
            elif m % 6 == 5:
                d2.select_by_value("60 Min")

        elif i % 6 == 1:
            d1.select_by_value("blood_pressure")
        elif i % 6 == 2:
            d1.select_by_value("blood_sugar")
        elif i % 6 == 3:
            d1.select_by_value("temperature")
        elif i % 6 == 4:
            d1.select_by_value("weight")
        elif i % 6 == 5:
            d1.select_by_value("pulse_rate")

        driver.find_element_by_xpath('//*[@id="activity"]/div/div[4]/button').click()
        d3 = Select(driver.find_element_by_xpath('//*[@id="activity-video"]'))
        d3.select_by_value("https://www.youtube.com/watch?v=n3CZTl-l3WI")

        driver.find_element_by_xpath('//*[@id="activity"]/div/div[7]/div/button').click()
        d4 = Select(driver.find_element_by_xpath('//*[@id="activity-frequency"]'))
        if i % 7 == 0:
            d4.select_by_value("1-0-0")
        elif i % 7 == 1:
            d4.select_by_value("1-1-0")
        elif i % 7 == 2:
            d4.select_by_value("0-1-0")
        elif i % 7 == 3:
            d4.select_by_value("0-1-1")
        elif i % 7 == 4:
            d4.select_by_value("0-0-1")
        elif i % 7 == 5:
            d4.select_by_value("1-0-1")
        elif i % 7 == 6:
            d4.select_by_value("1-1-1")

        driver.find_element_by_xpath('//*[@id="activity"]/div/div[8]/div/button').click()
        return

    
    def appointment_info(self, i, m, driver):

        driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[7]/div[3]/ul/li/a').click()
        time.sleep(5)

        driver.find_element_by_xpath('//*[@id="appointment-name"]').clear()
        driver.find_element_by_xpath('//*[@id="appointment-name"]').send_keys('regarding-health-progress')
        
        driver.find_element_by_xpath('//*[@id="appointment-date"]').click()
        driver.find_element_by_xpath('/html/body/div[21]/div[1]/div[2]/table/thead/tr[1]/th[3]/i').click()
        #ActionChains(driver).move_to_element(al1).click_and_hold().perform()
        #time.sleep(10)
        aq1 = driver.find_element_by_xpath('/html/body/div[21]/div[1]/div[2]/table/tbody/tr[4]/td[2]')
        ActionChains(driver).move_to_element(aq1).click().click().perform()
        
        driver.find_element_by_xpath('//*[@id="appointment"]/div/div[3]/div/div/button').click()
        s1 = Select(driver.find_element_by_xpath('//*[@id="appointment-type"]'))
        if i % 2 == 0:
            s1.select_by_value("consultation")
        else:
            s1.select_by_value("test")


        driver.find_element_by_xpath('//*[@id="appointment-notes"]').send_keys('the medicine given are followed as per schedule . further information about medicines and tests needed')
        
        driver.find_element_by_xpath('//*[@id="appointment"]/div/div[5]/div/button').click()
        return

    
    def medical_records(self, i, m, driver):

        driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[9]/div/ul/li/a/div/i').click()

        driver.find_element_by_xpath('//*[@id="report-title"]').clear()
        driver.find_element_by_xpath('//*[@id="report-title"]').send_keys('reports for blood test')
        
        driver.find_element_by_xpath('//*[@id="reports"]/div/div[2]/div[1]/div/button').click()
        n1 = Select(driver.find_element_by_xpath('//*[@id="report-type"]'))
        if i % 5 == 0:
            n1.select_by_value('discharge_report')
        elif i % 5 == 1:
            n1.select_by_value('doctor_prescription')
        elif i % 5 == 2:
            n1.select_by_value("doctor_notes")
        elif i % 5 == 3:
            n1.select_by_value("diagnostic/pathological_eport")
        elif i % 5 == 4:
            n1.select_by_value("surgery_notes")
            

        driver.find_element_by_xpath('//*[@id="report-date"]').click()
        driver.find_element_by_xpath('/html/body/div[20]/div[1]/div[2]/table/thead/tr[1]/th[1]/i').click()
        ac1 = driver.find_element_by_xpath('/html/body/div[20]/div[1]/div[2]/table/tbody/tr[2]/td[4]')
        ActionChains(driver).move_to_element(ac1).click().click().perform()

        driver.find_element_by_xpath('//*[@id="report-provider"]').send_keys('rahul verma' + str(i))
        nx1 = driver.find_element_by_xpath("//*[@id='report-file']")
        driver.execute_script('arguments[0].removeAttribute("type"); arguments[0].style["margin-left"] = 0;', nx1)
        nx1.send_keys('/home/asus/ssad/new2/new_image.jpg')
        #self.CloseWindow()
        #image_input = driver.find_element_by_id("imagePath")
        #image_input.send_keys('/home/asus/ssad/new2/image_gallery.jpeg')        
        '''nw1 = driver.find_element_by_xpath('//*[@id="report-file-name"]')
        driver.execute_script('arguments[0].removeAttribute("type"); arguments[0].style["margin-left"] = 0;', image_input)
        nw1.send_keys('/home/asus/ssad/new2/new_image.jpg')'''
        driver.find_element_by_xpath('//*[@id="report-uload"]').click()



    def datepicker(self, driver):
        datefield = driver.find_element_by_xpath(".//*[@id='dateOfBirth']")
        datefield.click()
        a1 = Select(driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/table/thead/tr[1]/th[2]/select[1]"))
        a1.select_by_value("2")
        a2 = Select(driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/table/thead/tr[1]/th[2]/select[2]"))
        a2.select_by_value("1998")
        select_btn = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/table/tbody/tr[6]/td[3]").click()
        #ActionChains(driver).move_to_element(select_btn).click().click().perform()

    
    def datepicker1(self, driver, i):
        datefield = driver.find_element_by_xpath(".//*[@id='admissionDate']")
        datefield.click()
        driver.implicitly_wait(5)  
        a1 = Select(driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/table/thead/tr[1]/th[2]/select[1]"))
        a1.select_by_value(str(i))
        a2 = Select(driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/table/thead/tr[1]/th[2]/select[2]"))
        a2.select_by_value(str(200) + str(i))
        select_btn = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/table/tbody/tr[3]/td[4]").click()
        #ActionChains(driver).move_to_element(select_btn).click().click().perform()
    
    
    def datepicker2(self, driver, i):
        k = i + 3
        print (i)
        datefield = driver.find_element_by_xpath("//*[@id='dischargeDate']")
        datefield.click()
        a1 = Select(driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/table/thead/tr[1]/th[2]/select[1]"))
        a1.select_by_value(str(k))
        a2 = Select(driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/table/thead/tr[1]/th[2]/select[2]"))
        a2.select_by_value(str(200) + str(i))
        select_btn = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/table/tbody/tr[2]/td[6]").click()
        #ActionChains(driver).move_to_element(select_btn).click().click().perform()

    
    def datepicker3(self, driver, i):
        l = i + 2
        datefield = driver.find_element_by_xpath(".//*[@id='surgeryDate']")
        datefield.click()
        a1 = Select(driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[2]/table/thead/tr[1]/th[2]/select[1]"))
        a1.select_by_value(str(l))
        a2 = Select(driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[2]/table/thead/tr[1]/th[2]/select[2]"))
        a2.select_by_value(str(200) + str(i))
        select_btn = driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[2]/table/tbody/tr[4]/td[4]").click()
        #ActionChains(driver).move_to_element(select_btn).click().click().perform()

    
    def add_patient(self, i, m, driver):

        j = i
        pat = self.pat[0] + '+' + str(i + 10) + "@" + self.pat[1]
        driver.find_element_by_xpath("/html/body/nav[2]/div/div/div/div[2]/div/ul/li[2]/a").click()
        assert driver.current_url, cfg["URL"] + "/hospital/patients"
        assert driver.title, "Patients"
        time.sleep(2)
        
        driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[2]/div/a/button").click()
        assert driver.current_url, cfg["URL"] +"/hospital/add-patient"
        time.sleep(2)


        driver.find_element_by_xpath(".//*[@id='firstName']").click()
        driver.find_element_by_xpath(".//*[@id='firstName']").clear()
        driver.find_element_by_xpath(".//*[@id='firstName']").send_keys("PatFn" + str(i))

        driver.find_element_by_xpath(".//*[@id='lastName']").click()
        driver.find_element_by_xpath(".//*[@id='lastName']").clear()
        driver.find_element_by_xpath(".//*[@id='lastName']").send_keys("PatLn" + str(i))

        driver.find_element_by_xpath(".//*[@id='add-form']/div/div[2]/div/div[2]/div[1]/div/button").click()
        dropdowna = Select(driver.find_element_by_xpath(".//*[@id='gender']"))
        time.sleep(2)
        
        if i%3 == 0:
            dropdowna.select_by_value("male")
        elif i%3 == 1:
            dropdowna.select_by_value("female")
        else:
            dropdowna.select_by_value("unassigned")

        now = datetime.datetime.now()
        s=[]
        for inw in str(now):
            s.append(inw)
        s1=s[8]+s[9]
        self.datepicker(driver)

        driver.find_element_by_xpath(".//*[@id='phoneNumber']").click()
        driver.find_element_by_xpath(".//*[@id='phoneNumber']").clear()
        driver.find_element_by_xpath(".//*[@id='phoneNumber']").send_keys(str(cfg["Phone_Number"]) + str(i))

        driver.find_element_by_xpath(".//*[@id='email']").click()
        driver.find_element_by_xpath(".//*[@id='email']").clear()
        driver.find_element_by_xpath(".//*[@id='email']").send_keys(pat)

        driver.find_element_by_xpath(".//*[@id='UHID']").click()
        driver.find_element_by_xpath(".//*[@id='UHID']").clear()
        driver.find_element_by_xpath(".//*[@id='UHID']").send_keys(str(542) + str(i))
        time.sleep(2)

        driver.find_element_by_xpath(".//*[@id='add-form']/div/div[2]/div/div[5]/div/button").click()
        dropdownb = Select(driver.find_element_by_xpath(".//*[@id='language']"))

        if int(i) % 3 == 0:
            dropdownb.select_by_value("english")
        elif int(i) % 3 == 1:
            dropdownb.select_by_value("telugu")
        elif int(i) % 3 == 2:
            dropdownb.select_by_value("hindi")

        driver.find_element_by_xpath(".//*[@id='aadhaarCardNumber']").click()
        driver.find_element_by_xpath(".//*[@id='aadhaarCardNumber']").clear()
        driver.find_element_by_xpath(".//*[@id='aadhaarCardNumber']").send_keys(str(12345678125) + str(i))

        driver.find_element_by_xpath(".//*[@id='add-form']/div/div[2]/div/a[1]/button").click()
        #print (i)
        aq = int(i)
        av = aq + 7

        assert driver.current_url, cfg["URL"] +"/hospital/patients/av/details"

        if j%2 == 0:
            driver.find_element_by_xpath("//*[@id='alert-box']/div/ul/li[2]/a").click()
            assert driver.current_url, cfg["URL"] +"/hospital/patients/av/add-discharge"
            
            driver.find_element_by_xpath("//*[@id='episodeId']").clear()
            driver.find_element_by_xpath("//*[@id='episodeId']").send_keys(str(1000)+str(i))

            self.datepicker1(driver, j)
            self.datepicker2(driver, j)

            driver.find_element_by_xpath("//*[@id='add-form']/div/div/div[2]/div/div[2]/div[1]/div/button").click()
            b1 = Select(driver.find_element_by_xpath(".//*[@id='dischargeType']"))
            b1.select_by_value("normal")

            driver.find_element_by_xpath("//*[@id='add-form']/div/div/div[2]/div/div[2]/div[2]/div/button").click()
            b2 = Select(driver.find_element_by_xpath("//*[@id='clinicalType']"))
            if int(i)%8 == 0:
                b2.select_by_value("cardiology")
            elif int(i)%8 == 1:
                b2.select_by_value("cardiac Surgery")
            elif int(i)%8 == 2:
                b2.select_by_value("neurology")
            elif int(i)%8 == 3:
                b2.select_by_value("obs-Gyn")
            elif int(i)%8 == 4:
                b2.select_by_value("oncology")
            elif int(i)%8 == 5:
                b2.select_by_value("gastro-enterology")
            elif int(i)%8 == 6:
                b2.select_by_value("other")
            elif int(i)%8 == 7:
                b2.select_by_value("orthopedics")

            driver.find_element_by_xpath("//*[@id='add-form']/div/div/div[2]/div/div[3]/div[1]/div/button").click()
            driver.find_element_by_xpath(
                ".//*[@id='add-form']/div/div/div[2]/div/div[3]/div[1]/div/div/ul/li[2]/a/span[1]").click()

            # b3 = Select(driver.find_element_by_xpath("//*[@id='doctorName']"))
            # b3.select_by_value("49")

            self.datepicker3(driver, j)

            driver.find_element_by_xpath("//*[@id='add-form']/div/div/div[2]/div/div[4]/div[1]/div/button").click()
            b4 = Select(driver.find_element_by_xpath("//*[@id='surgeryType']"))
            if int(i) % 6 == 0:
                b4.select_by_value("TKR")
            elif int(i) % 6 == 1:
                b4.select_by_value("CABG")
            elif int(i) % 6 == 2:
                b4.select_by_value("THR")
            elif int(i) % 6 == 3:
                b4.select_by_value("ACLR")
            elif int(i) % 6 == 4:
                b4.select_by_value("Acute Ischemic Stroke")
            elif int(i) % 6 == 5:
                b4.select_by_value("Other")
            
            driver.find_element_by_xpath("//*[@id='surgeryDetails']").send_keys("the surgery was normal and secure and the patient health is good after surgery as reported by reports")
            
            time.sleep(2)

            driver.find_element_by_xpath("//*[@id='add-form']/div/div/div[2]/div/div[5]/div[1]/div/button").click()
            b5 = Select(driver.find_element_by_xpath("//*[@id='diabetic']"))
            if int(i) % 3 == 0:
                b5.select_by_value("No")
            elif int(i) % 3 == 1:
                b5.select_by_value("Pre Diabetic")
            elif int(i) % 3 == 2:
                b5.select_by_value("Post Diabetic")

            driver.find_element_by_xpath("//*[@id='add-form']/div/div/div[2]/div/div[5]/div[2]/div/button").click()
            b6 = Select(driver.find_element_by_xpath("//*[@id='hypertensive']"))
            if int(i) % 3 == 0:
                b6.select_by_value("No")
            elif int(i) % 3 == 1:
                b6.select_by_value("Pre Hypertensive")
            elif int(i) % 3 == 2:
                b6.select_by_value("Post Hypertensive")
                
            driver.find_element_by_xpath("//*[@id='sys']").send_keys("100")
            driver.find_element_by_xpath("//*[@id='dia']").send_keys("80")

            driver.find_element_by_xpath("//*[@id='bloodSugar']").send_keys("4.6")
            driver.find_element_by_xpath("//*[@id='temperature']").send_keys("98")
            driver.find_element_by_xpath("//*[@id='weight']").send_keys("67")
            driver.find_element_by_xpath("//*[@id='pulseRate']").send_keys("80")
            
            driver.find_element_by_xpath("//*[@id='diet']").send_keys("eat healthy and fresh fruits and low cholestrol vegetables")
            driver.find_element_by_xpath("//*[@id='em-instruction']").send_keys("lie in the straight position and take deep breath")
            driver.find_element_by_xpath("//*[@id='emergencyContact']").send_keys(str(100100100) + str(j))
            time.sleep(2)
            
            driver.find_element_by_xpath("//*[@id='add-form']/div/div/div[2]/div/button").click()

            s = str(driver.current_url)
            print (s[44] + s[45])
            assert driver.current_url, cfg["URL"] +"/hospital/patients/av/details"
            self.medication_info(i, m, driver)
            self.activity_info(i, m, driver)
            self.appointment_info(i, m, driver)
            #self.medical_records(i, m, driver)

            driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[13]/div/button[1]').click()
            driver.find_element_by_xpath('//*[@id="save-regimen-btn"]').click()
            #driver.find_element_by_xpath("/html/body/nav[4]/div/div/div/div[2]/div/ul/li[2]/a").click()

            assert driver.current_url, cfg["URL"] + "/hospital/patients"
            assert driver.title, "Patients"
            ss = s[44] + s[45]
            print (ss)
            sd = int(ss)
            self.arr.append(sd)
            driver.find_element_by_id(ss).click()
            assert driver.current_url, cfg["URL"] +"/hospital/patients/av/details"

            driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div/button[3]').click()
            driver.find_element_by_xpath('//*[@id="publish-regimen-btn"]').click()  

            driver.find_element_by_xpath("/html/body/nav[4]/div/div/div/div[2]/div/ul/li[2]/a").click()

            assert driver.current_url, cfg["URL"] +"/hospital/patients"
            assert driver.title, "Patients"

        elif j%2 == 1:
            driver.find_element_by_xpath(".//*[@id='alert-box']/div/ul/li[3]/a").click()
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[2]/div/a/button").click()

            assert driver.current_url, cfg["URL"] +"/hospital/patients/av/add-discharge"
            
            driver.find_element_by_xpath("//*[@id='episodeId']").clear()
            driver.find_element_by_xpath("//*[@id='episodeId']").send_keys(str(1000)+str(i))
            time.sleep(1)

            self.datepicker1(driver, j)
            self.datepicker2(driver, j)

            driver.find_element_by_xpath("//*[@id='add-form']/div/div/div[2]/div/div[2]/div[1]/div/button").click()
            b1 = Select(driver.find_element_by_xpath(".//*[@id='dischargeType']"))
            b1.select_by_value("normal")

            driver.find_element_by_xpath("//*[@id='add-form']/div/div/div[2]/div/div[2]/div[2]/div/button").click()
            b2 = Select(driver.find_element_by_xpath("//*[@id='clinicalType']"))
            if int(i)%8 == 0:
                b2.select_by_value("cardiology")
            elif int(i)%8 == 1:
                b2.select_by_value("cardiac Surgery")
            elif int(i)%8 == 2:
                b2.select_by_value("neurology")
            elif int(i)%8 == 3:
                b2.select_by_value("obs-Gyn")
            elif int(i)%8 == 4:
                b2.select_by_value("oncology")
            elif int(i)%8 == 5:
                b2.select_by_value("gastro-enterology")
            elif int(i)%8 == 6:
                b2.select_by_value("other")
            elif int(i)%8 == 7:
                b2.select_by_value("orthopedics")

            driver.find_element_by_xpath("//*[@id='add-form']/div/div/div[2]/div/div[3]/div[1]/div/button").click()
            driver.find_element_by_xpath(
                ".//*[@id='add-form']/div/div/div[2]/div/div[3]/div[1]/div/div/ul/li[2]/a/span[1]").click()
            #b3 = Select(driver.find_element_by_xpath("//*[@id='doctorName']"))
            #b3.select_by_value("49")

            self.datepicker3(driver, j)
            time.sleep(1)

            driver.find_element_by_xpath("//*[@id='add-form']/div/div/div[2]/div/div[4]/div[1]/div/button").click()
            b4 = Select(driver.find_element_by_xpath("//*[@id='surgeryType']"))
            if int(i) % 6 == 0:
                b4.select_by_value("TKR")
            elif int(i) % 6 == 1:
                b4.select_by_value("CABG")
            elif int(i) % 6 == 2:
                b4.select_by_value("THR")
            elif int(i) % 6 == 3:
                b4.select_by_value("ACLR")
            elif int(i) % 6 == 4:
                b4.select_by_value("Acute Ischemic Stroke")
            elif int(i) % 6 == 5:
                b4.select_by_value("Other")
            
            driver.find_element_by_xpath("//*[@id='surgeryDetails']").send_keys("the surgery was normal and secure and the patient health is good after surgery as reported by reports")
            
            driver.find_element_by_xpath("//*[@id='add-form']/div/div/div[2]/div/div[5]/div[1]/div/button").click()
            b5 = Select(driver.find_element_by_xpath("//*[@id='diabetic']"))
            if int(i) % 3 == 0:
                b5.select_by_value("No")
            elif int(i) % 3 == 1:
                b5.select_by_value("Pre Diabetic")
            elif int(i) % 3 == 2:
                b5.select_by_value("Post Diabetic")

            driver.find_element_by_xpath("//*[@id='add-form']/div/div/div[2]/div/div[5]/div[2]/div/button").click()
            b6 = Select(driver.find_element_by_xpath("//*[@id='hypertensive']"))
            if int(i) % 3 == 0:
                b6.select_by_value("No")
            elif int(i) % 3 == 1:
                b6.select_by_value("Pre Hypertensive")
            elif int(i) % 3 == 2:
                b6.select_by_value("Post Hypertensive")
                
            driver.find_element_by_xpath("//*[@id='sys']").send_keys("100")
            driver.find_element_by_xpath("//*[@id='dia']").send_keys("80")

            driver.find_element_by_xpath("//*[@id='bloodSugar']").send_keys("4.6")
            driver.find_element_by_xpath("//*[@id='temperature']").send_keys("98")
            driver.find_element_by_xpath("//*[@id='weight']").send_keys("67")
            driver.find_element_by_xpath("//*[@id='pulseRate']").send_keys("80")
            
            driver.find_element_by_xpath("//*[@id='diet']").send_keys("eat healthy and fresh fruits and low cholestrol vegetables")
            driver.find_element_by_xpath("//*[@id='em-instruction']").send_keys("lie in the straight position and take deep breath")
            driver.find_element_by_xpath("//*[@id='emergencyContact']").send_keys(str(100100100) + str(j))
            
            driver.find_element_by_xpath("//*[@id='add-form']/div/div/div[2]/div/button").click()


            s = str(driver.current_url)
            assert driver.current_url, cfg["URL"] +"/hospital/patients/av/details"

            self.medication_info(i, m, driver)
            time.sleep(1)
            self.activity_info(i, m, driver)
            time.sleep(1)
            self.appointment_info(i, m, driver)
            #self.medical_records(i, m, driver)
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[13]/div/button[1]').click()
            driver.find_element_by_xpath('//*[@id="save-regimen-btn"]').click()
            #driver.find_element_by_xpath("/html/body/nav[4]/div/div/div/div[2]/div/ul/li[2]/a").click()

            assert driver.current_url, cfg["URL"]+"/hospital/patients"
            assert driver.title, "Patients"

            ss = s[44] + s[45]
            print (ss)
            sd = int(ss)
            self.arr.append(sd)
            driver.find_element_by_id(ss).click()
            assert driver.current_url, cfg["URL"] +"/hospital/patients/av/details"

            driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div/button[3]').click()
            driver.find_element_by_xpath('//*[@id="publish-regimen-btn"]').click()

            driver.find_element_by_xpath("/html/body/nav[4]/div/div/div/div[2]/div/ul/li[2]/a").click()

            assert driver.current_url, cfg["URL"] +"/hospital/patients"
            assert driver.title, "Patients"
            #driver.find_element_by_xpath("/html/body/nav[4]/div/div/div/div[2]/div/ul/li[2]/a").click()

            #assert driver.current_url, "http://52.221.250.80:8082/hospital/patients"
            #assert driver.title, "Patients"

        driver.find_element_by_xpath("//*[@id='doctors-tab']").click()
        assert driver.current_url, cfg["URL"] +"/hospital/staff"
        assert driver.title, "Staff"
        return

    def select_one(self, a1, i, driver):

        l = len(a1)
        if i < l:
            x = a1[i]
            xx = str(x)
            s1 = str('//*[@id="')
            s2 = xx
            s3 = str('"]/td[4]/div/label/input')
            sd = s1 + s2 + s3
            #print (s1 + s2 + s3)
            #print ('//*[@id="66"]/td[4]/div/label/input')
            
            driver.find_element_by_xpath(sd).click()

        else:
            k = i % l
            x = a1[k]
            xx = str(x)
            s1 = str('//*[@id="')
            s2 = xx
            s3 = str('"]/td[4]/div/label/input')
            sd = s1 + s2 +s3
            #print (s1 + s2 + s3)
            #print ('//*[@id="66"]/td[4]/div/label/input')

            driver.find_element_by_xpath(sd).click()

        driver.find_element_by_xpath('//*[@id="message"]').clear()
        driver.find_element_by_xpath('//*[@id="message"]').send_keys("Get well soon" + str(i))

        driver.find_element_by_xpath('//*[@id="done"]').click()

        driver.find_element_by_xpath('//*[@id="confirm-patients-btn"]').click()
        driver.find_element_by_xpath('//*[@id="message"]').clear()
            #driver.find_element_by_xpath('//*[@id="confirm-patients"]/div/div/div/div/div/div[2]/div/button[2]').click()

        return


    def select_many(self, a1, i, driver):

        l = len(a1)
        if l % 4 == 0:
            x = a1[1]
            x1 = a1[3]
            x2 = a1[4]
            xx = str(x)
            xx1 = str(x1)
            xx2 = str(x2)

            s11 = str('//*[@id="')
            s12 = xx
            s13 = str('"]/td[4]/div/label/input')
            sd1 = s11 + s12 + s13

            s21 = str('//*[@id="')
            s22 = xx1
            s23 = str('"]/td[4]/div/label/input')
            sd2 = s21 + s22 + s23

            s31 = str('//*[@id="')
            s32 = xx2
            s33 = str('"]/td[4]/div/label/input')
            sd3 = s31 + s32 + s33

            driver.find_element_by_xpath(sd1).click()
            driver.find_element_by_xpath(sd2).click()
            driver.find_element_by_xpath(sd3).click()

        else:
            x = a1[0]
            x1 = a1[2]
            x2 = a1[5]
            xx = str(x)
            xx1 = str(x1)
            xx2 = str(x2)

            s11 = str('//*[@id="')
            s12 = xx
            s13 = str('"]/td[4]/div/label/input')
            sd1 = s11 + s12 + s13

            s21 = str('//*[@id="')
            s22 = xx1
            s23 = str('"]/td[4]/div/label/input')
            sd2 = s21 + s22 + s23

            s31 = str('//*[@id="')
            s32 = xx2
            s33 = str('"]/td[4]/div/label/input')
            sd3 = s31 + s32 + s33

            driver.find_element_by_xpath(sd1).click()
            driver.find_element_by_xpath(sd2).click()
            driver.find_element_by_xpath(sd3).click()

        driver.find_element_by_xpath('//*[@id="message"]').clear()
        driver.find_element_by_xpath('//*[@id="message"]').send_keys("Get well soon" + str(i))

        driver.find_element_by_xpath('//*[@id="done"]').click()

        if i % 4 == 0:
            driver.find_element_by_xpath('//*[@id="confirm-patients-btn"]').click()
        else:
            driver.find_element_by_xpath('//*[@id="confirm-patients"]/div/div/div/div/div/div[2]/div/button[2]').click()

        driver.find_element_by_xpath('//*[@id="message"]').clear()
        driver.find_element_by_xpath(sd1).click()
        driver.find_element_by_xpath(sd2).click()
        if driver.find_element_by_xpath(sd3).is_selected():
            driver.find_element_by_xpath(sd3).click()

        return

    def select_all(self, a1, i, driver):

        driver.find_element_by_xpath('//*[@id="select-all"]').click()

        driver.find_element_by_xpath('//*[@id="message"]').clear()
        driver.find_element_by_xpath('//*[@id="message"]').send_keys("Get well soon" + str(i))

        driver.find_element_by_xpath('//*[@id="done"]').click()

        if i % 4 == 0:
            driver.find_element_by_xpath('//*[@id="confirm-patients-btn"]').click()
        else:
            driver.find_element_by_xpath('//*[@id="confirm-patients"]/div/div/div/div/div/div[2]/div/button[2]').click()
        
        if driver.find_element_by_xpath('//*[@id="select-all"]').is_selected():
            driver.find_element_by_xpath('//*[@id="select-all"]').click()

        return 


    def message(self, i, driver):
        driver.find_element_by_xpath('/html/body/nav/div/div/div/div[2]/div/ul/li[5]/a').click()
        assert driver.current_url, cfg["URL"] +"/hospital/messages"
        assert driver.title, "Messages"
        print(self.arr[0])
        a1 = self.arr
        if i % 3 == 0:
            self.select_one(a1, i, driver)
        elif i % 3 == 1:
            self.select_many(a1, i, driver)
        else:
            self.select_all(a1, i, driver)

        driver.find_element_by_xpath("//*[@id='doctors-tab']").click()
        assert driver.current_url, cfg["URL"] +"/hospital/staff"
        assert driver.title, "Staff"

        return

    def logout(self, driver):

        # For log out
        driver.find_element_by_xpath(
            "html/body/header/div/div/div[1]/a/img").click()
        #assert driver.current_url == cfg["URL"] + "/admin/hospitals"

        driver.find_element_by_xpath(
            "html/body/header/div/div/div[2]/table/tbody/tr/td[3]/i").click()
        driver.find_element_by_xpath(
            "html/body/header/div/div/div[2]/ul/li/div[2]/a/button").click()
        return

