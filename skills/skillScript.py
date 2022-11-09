
from collections import OrderedDict
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import jsonpickle  # !pip install jsonpickle
import json
import time
from chaptersData.Characters import *
from skills.skillClass import Skill 

def extractData(driver,collection,charactersNameList):
        name = driver.find_element(By.CSS_SELECTOR,'#firstHeading').text.title().replace('James','').replace(' ','-').replace('Lebron-', 'Lebron')
            
        if name in charactersNameList:
    
            print(name)
    
            releaseDate = driver.find_element(By.CSS_SELECTOR,'#mw-content-text > div > aside > section:nth-child(5) > div:nth-child(3) > div').text
        
            unlock = driver.find_element(By.CSS_SELECTOR,'#mw-content-text > div > aside > section:nth-child(5) > div:nth-child(4) > div').text    
        
            voiceActor = driver.find_element(By.CSS_SELECTOR,'#mw-content-text > div > aside > section:nth-child(6) > div > div').text 
            
            universe =  driver.find_element(By.CSS_SELECTOR,'#mw-content-text > div > aside > section:nth-child(4) > div:nth-child(2) > div').text
        
            unlockToArr = unlock.split('\n')
        
            unlockPrice = UnlockPrice(gold = unlockToArr[0], gleanium=unlockToArr[1],ticket=unlockToArr[2])
            
            skillButtons = driver.find_elements(By.CSS_SELECTOR,'#mw-content-text > div > div.tabber.wds-tabber > div.wds-tabs__wrapper.with-bottom-border > ul')
            
            attackFinal = list()
            
            skillFinal = list()
            
            if skillButtons:
                button = skillButtons[0].find_elements(By.CSS_SELECTOR,'li.wds-tabs__tab') 
                passives = button[-1]
                skillsList = list()
                attacksList = list()
                button.pop(-1)
            else:
                button = list()
            
            for i in button:
                if i.get_attribute('class') != 'wds-tabs__tab wds-is-current':
                    print('skill label')
                    WebDriverWait(driver, 2)\
                    .until(EC.element_to_be_clickable((i)))\
                    .click()
                    time.sleep(1)
                    table = driver.find_element(By.CSS_SELECTOR,'#mw-content-text > div > div.tabber.wds-tabber > div.wds-tab__content.wds-is-current > table')
                    rows = table.find_elements(By.TAG_NAME,'tr')
                    rows.pop(0)
                    for row in rows:
                        skillsList = list()
                        rowsa = row.find_elements(By.XPATH,'*')
                        for rowData in rowsa:
                            skillsList.append(rowData.text)       
                        skillFinal.append(Skill(direction=skillsList[0],ground=skillsList[1],air=skillsList[2]))
               
                else:
                    print('attacks label')
                    table = driver.find_element(By.CSS_SELECTOR,'#mw-content-text > div > div.tabber.wds-tabber > div.wds-tab__content.wds-is-current > table')                    
                    rows = table.find_elements(By.TAG_NAME,'tr')
                    rows.pop(0)
                    for row in rows:
                        attacksList = list()
                        rowsa = row.find_elements(By.XPATH,'*')
                        for rowData in rowsa:
                            attacksList.append(rowData.text)                               
                        attackFinal.append(Skill(direction=attacksList[0],ground=attacksList[1],air=attacksList[2]))      
            
            attackFinal = jsonpickle.encode(attackFinal,unpicklable=False)
            attackFinal = json.loads(attackFinal)
            skillFinal = jsonpickle.encode(skillFinal,unpicklable=False)
            skillFinal = json.loads(skillFinal)
            unlockPrice = jsonpickle.encode(unlockPrice,unpicklable=False)
            unlockPrice = json.loads(unlockPrice)
            collection.find_one_and_update({'data.name':name},{"$set":{'data.unlock':unlockPrice , 'data.voiceActor':voiceActor, 'universe':universe, 'attacks':attackFinal, 'skills':skillFinal}})

def skillScript(driver,collection):
    charactersNameListDB = collection.find({},{"data.name":1,"_id":0})
    charactersNameList = list()
    
    for i in (charactersNameListDB):
        charactersNameList.append(i['data']['name'])
    
    charactersUrl = list()
    
    WebDriverWait(driver, 2) \
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '/html/body/div[9]/div/div/div[2]/div[2]'))) \
        .click()
    
    charactersUrl = driver.find_elements(By.CSS_SELECTOR,'#gallery-0 > div > div.lightbox-caption > a')
    
    urls = list()
    
    for i in charactersUrl:
        urls.append(i.get_attribute('href'))
        
    for url in urls:
        driver.get(url)
        extractData(driver,collection,charactersNameList)
        
   
                
                    
        
        