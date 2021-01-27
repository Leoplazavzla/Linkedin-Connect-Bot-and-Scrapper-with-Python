import os
import random
import sys
import time
from urllib.parse import urlparse
from selenium.common.exceptions import ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd

# Open Webdriver
browser = webdriver.Chrome('chromedriver.exe')

# LinkedIn login page
browser.get('https://www.linkedin.com/uas/login')

# Getting login details
file = open('config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]

# Insert Username
elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

# Insert Password
elementID = browser.find_element_by_id('password')
elementID.send_keys(password)

# Submit
elementID.submit()

# Reading excel file with LinkedIn Accounts
dataLocation = "accounts.xlsx"
df = pd.read_excel(dataLocation)

# Check number of rows
rows = len(df)

# Looking for each account
for row in range(rows):
    studentAccount = df.loc[row][0]
    searchURL = studentAccount
    browser.get(searchURL)

    # scrolling to the bottom and top again
    scrollPauseTime = 3
    lastHeight = browser.execute_script("return document.body.scrollHeight")

    for i in range(1):
        # Scroll to the middle of the page
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight/2); ")
        time.sleep(scrollPauseTime)
        # Scroll to the bottom of the page
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight); ")
        # Scroll to the top of the page
        browser.execute_script("window.scrollTo(0, 0); ")
        time.sleep(scrollPauseTime)
        newHeight = browser.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight

        # Getting connection type for student
        sourceCode = BeautifulSoup(browser.page_source)
        connection = sourceCode.find(
            'span', {'class': 'dist-value'}).get_text()
        print(connection)

        # Extract data for each student

        # 1st CONNECTION
        if (connection == '1st'):
            # Get company Name
            companyName = sourceCode.find('span', {
                                          'class': 'text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view'}).get_text()
            print(companyName)
            # Get job title
            jobTitle = sourceCode.find(
                'h3', {'class': 't-16 t-black t-bold'}).get_text()
            print(jobTitle)
            # Get student email
            contactDetails = browser.find_element_by_link_text('Contact info')
            contactDetails.click()
            time.sleep(scrollPauseTime)
            sourceCode2 = BeautifulSoup(browser.page_source)
            studentEmailSec = sourceCode2.find(
                'section', {'class': 'pv-contact-info__contact-type ci-email'})
            studentEmailDiv = studentEmailSec.find_all(
                'a', {'class': 'pv-contact-info__ci-container t-14'})
            studentEmail = studentEmailSec.a.get_text()
            print(studentEmail)
            browser.back()
            # Get company Link
            companyLink = sourceCode.find(
                'a', {'class': 'full-width ember-view'})
            fullLink = 'https://www.linkedin.com' + companyLink['href']
            print(companyLink['href'])
            time.sleep(scrollPauseTime)
            # Append data to Excell
            df.loc[row, 'company'] = companyName
            df.loc[row, 'email'] = studentEmail
            df.loc[row, 'companylink'] = fullLink
            df.loc[row, 'jobtitle'] = jobTitle
            df.to_excel(dataLocation, index=False)
        # 2nd CONNECTION
        elif (connection == '2nd'):
            # Get company Name
            companyName = sourceCode.find('span', {
                                          'class': 'text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view'}).get_text()
            print(companyName)
            # Get company Link
            companyLink = sourceCode.find(
                'a', {'class': 'full-width ember-view'})
            fullLink = 'https://www.linkedin.com' + companyLink['href']
            print(companyLink['href'])
            time.sleep(scrollPauseTime)
            # Get job Title
            jobTitle = sourceCode.find(
                'h3', {'class': 't-16 t-black t-bold'}).get_text()
            print(jobTitle)
            # Check if FOLLOW BUTTON exists
            followButton = browser.find_element_by_class_name(
                'pv-s-profile-actions--follow')
            is_non_empty = bool(followButton)
            if is_non_empty == True:
                try:
                    time.sleep(scrollPauseTime)
                except ElementNotInteractableException:
                    print('I´m a dick')
                    time.sleep(scrollPauseTime-1)
                    sourceCode5 = BeautifulSoup(browser.page_source)
                    time.sleep(scrollPauseTime-1)
                    connectButton = browser.find_element_by_class_name(
                        'pv-s-profile-actions--connect')
                    time.sleep(scrollPauseTime-1)
                    connectButton.click()
                    sourceCode6 = BeautifulSoup(browser.page_source)
                    time.sleep(scrollPauseTime)
                    studentConnect = browser.find_element_by_class_name('ml1')
                    studentConnect.click()

                else:
                    print('youre screwed')
                    sourceCode4 = BeautifulSoup(browser.page_source)
                    menuButton = browser.find_element_by_class_name(
                        'pv-s-profile-actions__overflow')
                    time.sleep(scrollPauseTime)
                    menuButton.click()
                    time.sleep(scrollPauseTime-1)
                    sourceCode5 = BeautifulSoup(browser.page_source)
                    time.sleep(scrollPauseTime-1)
                    thirdConnect = browser.find_element_by_class_name(
                        'pv-s-profile-actions--connect')
                    time.sleep(scrollPauseTime-1)
                    thirdConnect.click()
                    sourceCode6 = BeautifulSoup(browser.page_source)
                    time.sleep(scrollPauseTime)
                    studentConnect = browser.find_element_by_class_name('ml1')
                    studentConnect.click()

            # Append data to Excell
            time.sleep(scrollPauseTime)
            connected = 'yes'
            df.loc[row, 'company'] = companyName
            df.loc[row, 'companylink'] = fullLink
            df.loc[row, 'jobtitle'] = jobTitle
            df.loc[row, 'connected'] = connected
            df.to_excel(dataLocation, index=False)
        else:
            # Get company Name
            companyName = sourceCode.find('span', {
                                          'class': 'text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view'}).get_text()
            print(companyName)
            # Get company Link
            companyLink = sourceCode.find(
                'a', {'class': 'full-width ember-view'})
            fullLink = 'https://www.linkedin.com' + companyLink['href']
            print(companyLink['href'])
            time.sleep(scrollPauseTime)
            # Get job Title
            jobTitle = sourceCode.find(
                'h3', {'class': 't-16 t-black t-bold'}).get_text()
            print(jobTitle)
            sourceCode4 = BeautifulSoup(browser.page_source)
            # Find and click MENU BUTTON
            menuButton = browser.find_element_by_class_name(
                'pv-s-profile-actions__overflow')
            time.sleep(scrollPauseTime)
            menuButton.click()
            time.sleep(scrollPauseTime-1)
            sourceCode5 = BeautifulSoup(browser.page_source)
            time.sleep(scrollPauseTime-1)
            thirdConnect = browser.find_element_by_class_name(
                'pv-s-profile-actions--connect')
            # print(thirdConnect)
            time.sleep(scrollPauseTime-1)
            thirdConnect.click()
            sourceCode6 = BeautifulSoup(browser.page_source)
            time.sleep(scrollPauseTime)
            studentConnect = browser.find_element_by_class_name('ml1')
            studentConnect.click()

            # Append data to Excell
            connected = 'yes'
            df.loc[row, 'company'] = companyName
            df.loc[row, 'companylink'] = fullLink
            df.loc[row, 'jobtitle'] = jobTitle
            df.loc[row, 'connected'] = connected
            df.to_excel(dataLocation, index=False)
