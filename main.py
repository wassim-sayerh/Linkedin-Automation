#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 21:38:53 2019

@author: wassim
"""

#%%
#Import libraries

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#from editJobName import editJobName
from selectCV import selectCV

from time import sleep
import time
import datetime

from langdetect import detect


#Get data from user

keywords = input("Please input search keywords> ")
country = input("Please input a country> ")

datePosted = 0
while datePosted not in [1, 2, 3, 4]:
    datePosted = int(input("Date Posted:\n1 - Past 24 Hours\n2 - Past Week\n3 - Past Month\n4 - Any Time\n> "))

#Get to page and sign in

browser = webdriver.Firefox(executable_path='/Users/Wassim/geckodriver')
browser.maximize_window()


browser.get("https://www.linkedin.com/login?fromSignIn=true&session_redirect=https%3A%2F%2Fwww.linkedin.com%2Fjobs&trk=guest_homepage-jobseeker_nav-header-signin")


from inputs import email as userEmail
from inputs import password as userPassword

username = browser.find_element_by_id('username')
username.send_keys(userEmail)

password = browser.find_element_by_id('password')
password.send_keys(userPassword)

login = browser.find_element_by_class_name('btn__primary--large')
login.click()

#Fill in search

keyword_field = browser.find_element_by_xpath("//input[@aria-label='Search jobs']")
keyword_field.send_keys(keywords)

country_field = browser.find_element_by_xpath("//input[@aria-label='Search location']")
country_field.send_keys(country)

submit = browser.find_element_by_class_name('jobs-search-box__submit-button')
submit.click()

#Select only Easy Apply

try:
    linkedinFeatures = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-controls='linkedin-features-facet-values']")))
    linkedinFeatures.click()
    
    easyApply = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='f_LF-f_AL']")))
    easyApply.click()    
    
    applyLinkedinFeatures = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='linkedin-features-facet-values']//button[@class='facet-collection-list__apply-button ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")))
    applyLinkedinFeatures.click()  

except:
    input("Could not select Linkedin Features. Please do it directly on the browser and press Enter >")

#Select Experience Level: Entry-Level & Associate

try:
    experienceLevel = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-controls='experience-level-facet-values']")))
    experienceLevel.click()
    
    entryLevel = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='f_E-2']")))
    entryLevel.click()    
    
    associateLevel = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='f_E-3']")))
    associateLevel.click()
    
    applyExperienceLevel = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='experience-level-facet-values']//button[@class='facet-collection-list__apply-button ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")))
    applyExperienceLevel.click()

except:
    input("Could not select Experience Level. Please do it directly on the browser and press Enter >")
    
#Select Date Posted

try:
    datePostedButton = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-controls='date-posted-facet-values']")))
    datePostedButton.click()
    
    datePostedSelectedDictionary = {
        1: 'f_TPR-r86400',
        2: 'f_TPR-r604800',
        3: 'f_TPR-r2592000',
        4: 'f_TPR-'}

    
    applyDatePosted = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='date-posted-facet-values']//button[@class='facet-collection-list__apply-button ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")))
    applyDatePosted.click()

except:
    input("Could not select Experience Level. Please do it directly on the browser and press Enter >")
    
#%%
#Loop through jobs

baseURL = browser.current_url

try:
    pageList = WebDriverWait(browser, 2).until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='artdeco-pagination__pages artdeco-pagination__pages--number']/li")))
    lastPage = int(pageList[-1].text)
except:
    lastPage = 1


totalJobs = 0

file = open('Jobs - ' + str(datetime.date.today()) + ' - ' + time.strftime("%H-%M-%S", time.localtime()) + '.csv', 'a')
file.write('Company, Job Name, Location, Link, Date, Time\n')

#%%
for page in range(lastPage):
# for page in range(10):
    
    #Query job list page
    if page != 0:
        browser.get(baseURL + '&start=' + str(25 * page))
    
    #Query all job list within page
    for i in range(8):
        browser.execute_script("document.querySelector('.jobs-search-results').scrollTop =" + str((i+1)*500))
        sleep(1)
    #Save jobs listen within the page into a list variable
    jobList = browser.find_elements_by_xpath("//ul[@class='jobs-search-results__list artdeco-list']/li")
    
    # browser.execute_script("document.querySelector('.jobs-search-results').scrollTop = 0")

    #For each job within the list        
    for job in jobList:

        
        try:
            #Scroll to Job Div
            jobDivPosition = browser.execute_script("arguments[0].offsetTop", job)
            browser.execute_script("document.querySelector('.jobs-search-results').scrollTop = arguments[0]", jobDivPosition)
            
            # Open Job Page
            try:
                jobLink = WebDriverWait(job, 10)
                jobLink = jobLink.until(EC.element_to_be_clickable((By.XPATH, ".//div/artdeco-entity-lockup/artdeco-entity-lockup-content/h3")))
                jobLink.click()
            except:
                input("Could not select open job page. Please do it directly on the browser and press Enter >")
    
            # jobLink = job.find_element_by_xpath(".//div/artdeco-entity-lockup/artdeco-entity-lockup-content/h3")
            # jobLink.click()
            
            appliedStatus = 0
            
            while True:
                try:
                    browser.find_element_by_link_text("See application")
                except:
                    try:
                        browser.find_element_by_xpath("//button[@class='jobs-apply-button artdeco-button artdeco-button--3 artdeco-button--primary ember-view']")
                    except:
                        pass
                    else:
                        break
                else:
                    appliedStatus = 1
                    break
                
                                                                 
                # seeApplication = WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.LINK_TEXT, "See application")))
    
            
            if appliedStatus == 0:
    
                #Gettinging & Cleaning job name
                removeList = ['promoted', 'h/f', 'h-f', '(h/f)', '(h-f)', 'f/h', 'f-h', '(f/h)', '(f-h)', 'm/f', 'm-f', '(m/f)', '(m-f)', 'f/m', 'f-m', '(f/m)', '(f-m)', '(cdi)', 'cdi', 'confirmé']
                jobNameWords = job.text.split("\n")[0].split()
                
                jobNameWords  = [word for word in jobNameWords if word.lower() not in removeList]
                jobNameStripped = ' '.join(jobNameWords).strip()
                
                if jobNameStripped[-1] == '-':
                    jobNameStripped = jobNameStripped[:-1].strip()
                if jobNameStripped[0] == '-':
                    jobNameStripped = jobNameStripped[1:].strip()
                if jobNameStripped.islower() or jobNameStripped.isupper():
                    jobNameStripped = jobNameStripped.title()
                    
                jobNameStripped = jobNameStripped.split(' - ')[0]
                
                #Getting company name
                jobCompany = job.text.split('\n')[1]
        
                #Getting city, country
                jobLocation = job.text.split('\n')[2].replace(",", " -")
                
                #Detect job offer language
                try:
                    jobDescription = browser.find_element_by_xpath("//div[@id='job-details']/span").text.replace("\n", " ")
                    jobLanguage = detect(jobDescription)
                except:
                    jobLanguage = 'en'
                
                if jobLanguage == 'fr':
                    languageFileCode = "FR"
                elif jobLanguage == 'es':
                    languageFileCode = "ES"
                else:
                    languageFileCode = "EN"
                
                #Click on Easy Apply
                try:
                    EasyApplyButton = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='jobs-apply-button artdeco-button artdeco-button--3 artdeco-button--primary ember-view']")))
                    # EasyApplyButton = browser.find_element_by_xpath("//button[@class='jobs-apply-button artdeco-button artdeco-button--3 artdeco-button--primary ember-view']")
                    EasyApplyButton.click()
                except:
                    input("Could not click on Easy Apply button. Please do it directly on the browser and press Enter >")
    
                
                #Prepare CV
                # CVPath = editJobName(jobNameStripped, languageFileCode, country)
                CVPath = selectCV(languageFileCode, country)
                                
                while browser.find_elements_by_xpath("//button[@data-control-name='submit_unify']") == []:
    
                    #Detect if CV page
                    if browser.find_elements_by_xpath("//button[@aria-label='Remove uploaded document']") != []:
                        
                        #Remove current CV
                        removeCVButton = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Remove uploaded document']")))
                        removeCVButton.click()        
                
                        #Add CV
                        uploadCVButton = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@data-control-name='upload_document']")))
                        uploadCVButton.send_keys(CVPath)
                        WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Remove uploaded document']")))
 
                    #Detect if additional questions page
                    if browser.find_elements_by_xpath("//div[@class='jobs-easy-apply-form__groupings']/div/div") != []:
                    
                        for question in browser.find_elements_by_xpath("//div[@class='jobs-easy-apply-form__groupings']/div/div"):
                            
                            #Keyword lists definition
                            howManyList = ["combien", "how many", "cuántos"]
                            ITskills = ["excel", "python", "html", "css", "php", "sql", "tableau", "scrum", "agile", "agil", "ágil", "data", "technologies", "technology", "information" , "IT"]                        
                            speakList = ["speak", "parlez", "hablas", "habla"]
                            languagesSpokenList = ["english", "anglais", "ingles", "français", "francés", "french", "spanish", "español", "espagnol", "arabic", "arabe", "árabe"]
                            degreeList = ["degree", "bachelor", "master", "diplome", "diplôme", "diploma", "graduado"]
                            workPermitList = ["work permit", "autorisé à travailler", "allowed to work", "authorized to work"]
                            relocationList = ["desplazarte", "déplacer", "relocate", "commuting", "sponsorship", "werkvisum"]
                            
                            #If question is about years of experience
                            try:
                                if any(word in question.find_element_by_xpath(".//div/label/span").text.lower() for word in howManyList):
                                    answerField = question.find_element_by_xpath(".//div/div/div/input")
                                    if answerField.get_attribute("value") == '': #If field is empty
                                        if any(word in question.find_element_by_xpath(".//div/label/span").text.lower() for word in ITskills): #If in skills list > 2 years of experiencex
                                            answerField.send_keys("2")
                                        else: #If not in skills list > 1 year of experience
                                            answerField.send_keys("1")
                            except:
                                pass
                            #If question is about language
                            try:
                                if any(word in question.find_element_by_xpath(".//fieldset/legend/span").text.lower() for word in speakList):
                                    if not(any(radiobox.is_selected() for radiobox in question.find_elements_by_xpath(".//input"))):
                                        if any(word in question.find_element_by_xpath(".//fieldset/legend/span").text.lower() for word in languagesSpokenList):
                                            radioBoxYes = question.find_element_by_xpath(".//fieldset/div/div/label")
                                            radioBoxYes.click()
                            except:
                                pass
                                
                            #If question is about degree
                            try:
                                if any(word in question.find_element_by_xpath(".//fieldset/legend/span").text.lower() for word in degreeList):
                                    if not(any(radiobox.is_selected() for radiobox in question.find_elements_by_xpath(".//input"))):
                                        radioBoxYes = question.find_element_by_xpath(".//fieldset/div/div/label")
                                        radioBoxYes.click()
                            except:
                                pass
                            
                            #If question is about relocation
                            try:
                                if any(word in question.find_element_by_xpath(".//fieldset/legend/span").text.lower() for word in relocationList):
                                    if not(any(radiobox.is_selected() for radiobox in question.find_elements_by_xpath(".//input"))):
                                        radioBoxYes = question.find_element_by_xpath(".//fieldset/div/div/label")
                                        radioBoxYes.click()
                            except:
                                pass
                                
                            #If question is about work permit
                            try:
                                if any(word in question.find_element_by_xpath(".//fieldset/legend/span").text.lower() for word in workPermitList):
                                    if not(any(radiobox.is_selected() for radiobox in question.find_elements_by_xpath(".//input"))):
                                        radioBoxNo = question.find_element_by_xpath(".//fieldset/div/div[1]/label")
                                        radioBoxNo.click()
                            except:
                                pass                        
                    
                    #Click on Next or Review  
                    nextButton = browser.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
                    nextButton.click()
                    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")))
                        
                #Detect if CV page
                if browser.find_elements_by_xpath("//button[@aria-label='Remove uploaded document']") != []:
                    
                    #Remove current CV
                    removeCVButton = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Remove uploaded document']")))
                    removeCVButton.click()        
            
                    #Add CV
                    uploadCVButton = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@data-control-name='upload_document']")))
                    uploadCVButton.send_keys(CVPath)
                    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//button[@data-control-name='preview_document']")))
                
                #Uncheck Follow company
                try:
                    followCompanyCheckbox = browser.find_element_by_xpath("//label[@for='follow-company-checkbox']")
                    followCompanyCheckbox.click()
                except:
                    pass
    
                
                #Submit application
                submitApplicationButton = browser.find_element_by_xpath("//button[@data-control-name='submit_unify']")
                submitApplicationButton.click()
                
                #Log application
                file.write(jobCompany + ',' + jobNameStripped + ',' + jobLocation + ',' + browser.current_url + ',' + str(datetime.date.today()) + ',' + time.strftime("%H:%M:%S", time.localtime()) + '\n')
                totalJobs += 1
                
                #Dismiss application sent notification
                try:
                    dismissButton = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Your application is on its way')]")))
                    dismissButton.click()
                except:
                    pass
                
        except: #if there is any issue with this job, continue to the next job - don't interrupt the program
            continue

file.close()
