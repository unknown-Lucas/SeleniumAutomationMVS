from calendar import c
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .Characters import Characters, Data, UnlockPrice
import jsonpickle  # !pip install jsonpickle
import json
import time

def getChaptersData(driver,collection):
    #!Retiramos el no click
    WebDriverWait(driver, 2) \
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                           ' backgroundcliptext cssmask no-touchevents webp webpalpha webpanimation webplossless webp-alpha webp-animation webp-lossless'.replace(' ', '.')))) \
        .click()

#!Aceptamos las cookies
    WebDriverWait(driver, 3) \
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '//*[@id="onetrust-accept-btn-handler"]'))) \
        .click()

    #!Añadimos el campo de las fechas
    driver.implicitly_wait(2)
    input_age_days = driver.find_element(By.XPATH,
                                         '//*[@id="AgeGateDay"]')

    driver.implicitly_wait(2)
    input_age_days = driver.find_element(By.XPATH,
                                         '//*[@id="AgeGateMonth"]')

    input_age_month = driver.find_element(By.XPATH,
                                          '//*[@id="AgeGateDay"]')

    input_age_year = driver.find_element(By.XPATH,
                                         '//*[@id="AgeGateYear"]')

    #!Mandamos los datos a los inputs reunidos anteriormente
    input_age_days.send_keys('02')
    input_age_month.send_keys('08')
    input_age_year.send_keys('2001')

    WebDriverWait(driver, 3) \
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                           'button#SubmitBtn'))) \
        .click()

    driver.implicitly_wait(2)

    # ?recojemos en una lista todos los botones de personajes para iterarlos posteriormente
    character_div = driver.find_elements(By.CSS_SELECTOR,
                                         'button.character'.replace(' ', '.'))

    a = list()
    id = 0

    for character in character_div:
        print("Scrapping characters......")
        #!Es necesaria una espera entre el click y el espacio de busqueda de elementos ya que sino no le dara tiempo la pagina a cargar y recibiremos un none
        if (character.get_attribute('class') != 'locked character btn'):
            WebDriverWait(driver, 2)\
                .until(EC.element_to_be_clickable((character)))\
                .click()
            time.sleep(2)
            name = driver.find_element(
                By.XPATH, '//*[@id="BioPanel"]/div[2]/div[1]/div/div/h2')
            specialization = driver.find_element(
                By.XPATH, '//*[@id="BioPanel"]/div[2]/div[1]/div/div/div/span')
            title = driver.find_element(
                By.XPATH, '//*[@id="BioPanel"]/div[2]/div[2]/div/h3')
            attribute1 = driver.find_element(
                By.XPATH, '//*[@id="BioPanel"]/div[2]/div[2]/div/div[1]/div[1]')
            attribute2 = driver.find_element(
                By.XPATH, '//*[@id="BioPanel"]/div[2]/div[2]/div/div[1]/div[2]')
            attribute3 = driver.find_element(
                By.XPATH, '//*[@id="BioPanel"]/div[2]/div[2]/div/div[1]/div[4]')
            attribute4 = driver.find_element(
                By.XPATH, '//*[@id="BioPanel"]/div[2]/div[2]/div/div[1]/div[3]')
            description = driver.find_element(
                By.XPATH, '//*[@id="BioPanel"]/div[2]/div[2]/div/div[2]/p')
            image = driver.find_element(
                By.XPATH, '//*[@id="BioPanel"]/div[2]/div[1]/div/picture/img')
            
            attributes = [attribute1.text,attribute2.text,attribute3.text,attribute4.text]
            characterData = Data(name=name.text.title().replace('The Iron Giant','Iron Giant').replace('And', '&').replace(' ','-'), specialization=specialization.text.replace("-", "").replace(" ", "").title(), title=title.text, attributes=attributes, description=description.text, image=image.get_attribute('src'), unlock= UnlockPrice(gold=0,gleanium=0,ticket=0))
            character = Characters(character_id=id, data=characterData)
            a.append(character)
            id += 1

    time.sleep(2)
    characterJson = list()
    for character in a:
        frozen = jsonpickle.encode(character, unpicklable=False)
        fire = json.loads(frozen)
        characterJson.append(fire)
    
    try:
        collection.insert_many(characterJson)
    except:
        print("there was an error in character creation")
