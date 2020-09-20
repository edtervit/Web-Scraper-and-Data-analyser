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

driver.get('https://www.horseracebase.com/v4advancequalifiers.php?tom=1')

driver.set_window_size(1920, 1080) ## makes window big enough to see all data




tomorrows_date = datetime.date.today() + datetime.timedelta(days=1)

tomorrow = tomorrows_date.strftime("%d_%m_%Y") + " Qualifiers"

driver.save_screenshot(r"E:\Dropbox\Dropbox\DAD\GeeGeez\Qualifiers\screenshot.png")

file_path = r'E:\Dropbox\Dropbox\DAD\GeeGeez\Qualifiers/'

os.rename( "E:\Dropbox\Dropbox\DAD\GeeGeez\Qualifiers\screenshot.png" , file_path + tomorrow + '.png' ) 


driver.quit()

