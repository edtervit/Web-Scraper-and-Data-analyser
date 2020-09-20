import config
import os
import datetime

import requests as r
import time
from bs4 import BeautifulSoup as bs
from seleniumrequests import Chrome

import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import csv

import pickle



#checks the excel to see if the trainer and track are correct
def check_jp11(track,trainer):
    
    df = pd.read_csv('system11.csv')
    #for each row in the CSV check if the trainer and the track are there if they are return true
    for row in df.itertuples(index=False):
        if row.Trainer == str(trainer) and row.Track == str(track):
            return True
            
        else:
            pass
    return False        

    


def check_male(track,trainer):
    df = pd.read_csv('system208.csv')

    for row in df.itertuples(index=False):
        gender = 'Male'
        if row.Trainer == trainer and row.Course == track and row.Gender == gender:
            return True
            
        else:
            pass
    return False

def check_female(track,trainer):    
    df = pd.read_csv('system208.csv')

    for row in df.itertuples(index=False):
        gender = 'Female'
        if row.Trainer == trainer and row.Course == track and row.Gender == gender:
            return True
            
        else:
            pass
    return False


def run_script():
    ## makes selenium headless and shows where the driver file is.
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True

    driver = Chrome('E:\Dropbox\Dropbox\Dev\HRB\chromedriver.exe', options=chrome_options)


    ## call website to create selenium cookie session

    driver.get('https://www.horseracebase.com/v4builder.php')

    s = r.session()

    login_url = 'https://www.horseracebase.com/horsebase1.php'

    ##Get CSRF token for login payload 

    get_cookies = s.get(login_url)

    cookie_list = []

    for cookie in list(s.cookies):
        cookie_list.append(cookie.value) 
        

    CSRF = cookie_list[0] 


    ##Log in 


    payload = config.payload
    payload.update(CSRFtoken = CSRF)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}

    login = s.post(login_url, data=payload, headers=headers)

    ## check if login worked

    login_status = True if ('Hi unclened' in login.text) else False 

    if login_status == True:
        print("Login succesful")
    if login_status == False:
        print('Login failed, exiting in 5 seconds')
        time.sleep(5)
        exit()

    ## Get system page cookies 

    sys_url = 'https://www.horseracebase.com/v4builder.php'

    get_cookies_again = s.get(sys_url)

    ## add cookies to selenium

    for cookie in s.cookies:
        driver.add_cookie({
            'name': cookie.name, 
            'value': cookie.value,
            'path': '/',
            'domain': cookie.domain,
        })

    ##reloads page now logged in 
    driver.get(sys_url)


    ####################################################################################                                                                     
    ####################################################################################
    ####################################################################################
    ####################################################################################
    ###### From this point the browser is logged in and ready to extract data ##########
    ####################################################################################                                                                     
    ####################################################################################
    ####################################################################################                                                                     
    ####################################################################################
    ####################################################################################                                                                     
    ####################################################################################
    




    #loads page with info
    driver.get('https://www.horseracebase.com/v4advancequalifiers.php')

    html_source = driver.page_source

    df = pd.read_html(html_source)

    #goes to table on page with info
    correct_table = df[16]

    
    #empty list where I'll be adding results
    results_jp =[]
    results_Male = []
    results_Female = []
    #_1 = system name 
    #_2 = race time
    #row._3 = Track
    #_5 = horse name
    #_7 = Trainer

    #checks table for info 
    for row in correct_table.itertuples(index=False):
        
        #if system 11 
        if row._1 == '(11) checkresultsNEW excel':
            #checks if the track and trainer is in the excel file
            print('Found something to check')
            if check_jp11(row._3, row._7):
                results_jp.append('Horse: ' + str(row._5) + ' at track: ' + str(row._3) + ' at time: ' +str(row._2) + ' ')

            else:
                
                pass
            

        #if system  8 CheckExcel Track MALE 1strun2yo
        elif row._1 == '(8) CheckExcel Track MALE 1strun2yo':
            if check_jp11(row._3, row._7):
                results_jp.append('Horse: ' + str(row._5) + ' at track: ' + str(row._3) + ' at time: ' +str(row._2) + ' ')

            else:
                
                pass

        #if system  20 CheckExcel Track FEMALE 1strun2yo
        elif row._1 == '(20) CheckExcel Track FEMALE 2yo1st':
            if check_jp11(row._3, row._7):
                results_jp.append('Horse: ' + str(row._5) + ' at track: ' + str(row._3) + ' at time: ' +str(row._2) + ' ')

            else:
                
                pass
         

    return results_jp, results_Female, results_Male
    




results_jp, results_Female, results_Male = run_script() 


print(results_jp)
print(results_Male)
print(results_Female)
# driver.quit()

