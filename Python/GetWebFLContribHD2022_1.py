import os
import shutil
import time
import csv
from csv import DictReader
from csv import DictWriter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#import sys
#sys.path.append('F:\SOEData\Scripts\TAB2CSV')
#import tab2csv as TABCSV

#################################################
# Get FL HD contributions by candidate
#################################################
wrksp = "/workspaces/vscode-remote-try-python/DATA/State Races"
ElectionYear = "2022"
districtType = "HD"
office = 'State Representative                              '
#office = 'State Senator                                     '
dirContributions =os.path.join(wrksp, ElectionYear + districtType)
candidateFile = "2022HDCandidates.csv"
os.chdir(wrksp)

print(os.getcwd())
if (not os.path.exists(dirContributions)) :
    os.mkdir(dirContributions)

TAB = "\t"
EOL = '\n'
#chromeDriver = r"C:\Python27\chromedriver_win32\chromedriver.exe" # old method
# set download path for Chrome driver
Downloads = "/workspaces/vscode-remote-try-python/DATA/Downloads"
options = webdriver.ChromeOptions()
prefs = {}
prefs["profile.default_content_settings.popups"]=0
prefs["download.default_directory"]=Downloads
options.add_experimental_option("prefs", prefs)
#print("Laoding Chrome Driver from: " + chromeDriver)
browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
# browser = webdriver.Chrome(executable_path=chromeDriver) # deprecated



#########################################
# for each candidate, pull Contributions from FL Campaign Finance Database
# https://dos.elections.myflorida.com/campaign-finance/contributions/
#########################################
fileNameCandidates = os.path.join(wrksp, candidateFile)
with open(fileNameCandidates, 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:
        
        district = row["District"]
        lastName = row["LastName"]
        firstName = row["FirstName"]
        party = row["Party"]
        won = row["Status"]
        searchType = row["MatchType"]
        print("Get Contributions for: " + districtType + district + " " + lastName + " " + party)

        browser.get('https://dos.elections.myflorida.com/campaign-finance/contributions/')

        elem = browser.find_element(By.NAME, 'election')
        # Set to  General Election
        electionXpath = "//select[@name='election']/option[text()='" + ElectionYear + " Election']"
        browser.find_element(By.XPATH,electionXpath).click()

        #browser.find_element(By.NAME,'CanFName').send_keys(firstName)
        browser.find_element(By.NAME,'CanLName').send_keys(lastName)

        if ("Contains" == searchType) :
            radioCanNameSrch = browser.find_element(By.XPATH,"//*[@name='CanNameSrch'][@value='1']")
        else :
            radioCanNameSrch = browser.find_element(By.XPATH,"//*[@name='CanNameSrch'][@value='2']")

        # end searchType
        radioCanNameSrch.click();
        
        browser.find_element(By.XPATH,"//select[@name='office']/option[text()='" + office + "']").click()
        browser.find_element(By.NAME,'cdistrict').send_keys(district)

        elem = browser.find_element(By.NAME,'rowlimit')
        elem.clear()
        elem.send_keys("25000")


        elem = browser.find_element(By.CSS_SELECTOR,"input[type='radio'][name='queryformat'][value='2']")
        elem.click()
        #if (elem.is_selected()) :
            #    print('Value 2 is_selected')

        elem = browser.find_element(By.NAME,'Submit').click()

        # gets downloaded as 'Contrib.txt' note it includes the ' around the name
        contribFile = os.path.join(Downloads, "'Contrib.txt'")
        while not os.path.exists(contribFile):
            time.sleep(1)

        firstName = firstName.replace(' ','-').replace('.',"").replace('"',"")
        lastName = lastName.replace(' ','-').replace('.',"").replace('"',"")
        tempFileName = districtType + district + "_" + party + '_' + firstName + '_' + lastName + '_contrib'
        tab_file = os.path.join(Downloads, tempFileName + '.tab')
        print("Renaming to: " + tab_file)
        os.replace(contribFile, tab_file)
        #print("Converting from TAB to CSV")
        #TABCSV.convertTAB2CSV(tab_file,True)        
        #tab_file = tab_file.replace(".tab",".csv")
        #csv_file = os.path.join(dirContributions, tempFileName + '.csv')
        csv_file = os.path.join(dirContributions, tempFileName + '.tab')
        print("Moving to: " + csv_file)
        shutil.move(tab_file, csv_file)
   
    #end for each row
# end read csv


browser.close()
browser.quit()
del browser

