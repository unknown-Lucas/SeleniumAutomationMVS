from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .Maps import Data, Layout, Maps
import jsonpickle  # !pip install jsonpickle
import json
import time




def mapScript(driver, collection):
    
    cookies = driver.find_elements(By.CSS_SELECTOR,
                                   'body > div:nth-child(17) > div > div > div._1r08nyekFdI7_2d8r3AIBf > div.NN0_TB_DIsNmMHgJWgT7U.XHcr6qf5Sub2F2zBJ53S_')
    
    if(cookies):
        WebDriverWait(driver, 4) \
            .until(EC.element_to_be_clickable((By.XPATH,
                                           '/html/body/div[9]/div/div/div[2]/div[2]'))) \
            .click()
    
    time.sleep(1)
    
    mapsRoutes = driver.find_elements(By.CSS_SELECTOR,'#gallery-1 > div > div.lightbox-caption > a')
    
    url = list()
    
    for i in mapsRoutes:
        url.append(i.get_attribute('href'))
    
    maps = list()
    
    i =0
    
    for mapUrl in url:
        maps.append(extractMapData(driver, mapUrl,i))
        i += 1
    
    mapsJson = list();
    
    for map in maps:
        print(f"map {map.map_id} to BD......")
        frozen = jsonpickle.encode(map, unpicklable=False)
        fire = json.loads(frozen)
        mapsJson.append(fire)
    
    try:
        collection.insert_many(mapsJson)
    except:
        print("there was an error in character creation")

        
def extractMapData(driver,mapRoute,id):
    driver.get(mapRoute)
    time.sleep(1)
    
    mapname = driver.find_element(By.CSS_SELECTOR,
                                   '#firstHeading')
    
    mapImage = driver.find_element(By.CSS_SELECTOR,
                                   'img.pi-image-thumbnail')
    
    universe = driver.find_element(By.XPATH,
                                   '//*[@id="mw-content-text"]/div/aside/section/div[1]/div/i/a')
    
    print(universe.text)
    
    npcs = driver.find_elements(By.XPATH,
                                '//*[@id="mw-content-text"]/div/aside/section/div[2]/div')
    
    if (bool(npcs)):
        npcs = npcs[0].text.split('\n')
    
    originP1 = driver.find_elements(By.XPATH,
                                '//*[@id="mw-content-text"]/div/p[5]')[0].text
    
    originP2 = driver.find_elements(By.XPATH,
                                '//*[@id="mw-content-text"]/div/p[6]')[0].text
    
    origin = originP1 + "\n" + originP2
    
    layouts = driver.find_element(By.XPATH,
                                      '//*[@id="mw-content-text"]/div/h2[2]')

    layoutsData = sectionIterator(layouts)
    
    data = Data(mapname.text,origin,mapImage.get_attribute('src'),layoutsData,npcs)
    
    return Maps(id,universe.text,data)

def sectionIterator(htmlElement):
    siblings = True
    resultData = list()
    print('sectionIterator onGoing......')
    mixSiblings = {'title': '', 'description':''}
    while siblings:
        htmlElement = htmlElement.find_element(By.XPATH,
                             'following-sibling::*')
        if(htmlElement.tag_name == 'h3'):
            mixSiblings['title'] = htmlElement.text

        if(htmlElement.tag_name == 'p'):
            mixSiblings['description'] = htmlElement.text
            resultData.append(Layout(mixSiblings['title'],mixSiblings['description']))    
        
        if(htmlElement.tag_name == 'h2'):
           siblings = False
                      
    return resultData

    