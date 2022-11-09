from selenium import webdriver  # !pip install selenium
from pymongo import MongoClient  # !pip install pymongo
import time
from webdriver_manager.chrome import ChromeDriverManager
from skills.skillScript import skillScript
from chaptersData.characterScript import getChaptersData
from maps.mapScript import mapScript

#!DB Data

startTime  = time.time()

def initClient():
    return MongoClient(
        "mongodb+srv://user:pass@cluster0.x9iuu.mongodb.net/?retryWrites=true&w=majority")


def closeClient():
    cluster.close()


cluster = initClient()
db = cluster["MultiVs"]
collections = {'test': db["testCollections"],
               'characters': db["characters"], 'maps': db["maps"]}
routes = {'charactersMVS': 'https://multiversus.com/en-gb/roster',
          'wikiMain': 'https://multiversus.fandom.com/wiki/Multiversus_Wiki', 'wikiBase': 'https://multiversus.fandom.com/wiki'}

# ?Opciones de navegacion
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("----disable-dev-shm-usage")
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options
)

driver.set_window_size(1920, 1080)

CHARACTERS = collections['characters']
MAPS = collections['maps']

characterSize = db.command("collstats", "Characters")['count']
mapSize = db.command("collstats", "Maps")['count']

if not characterSize:
    print('Executing CharaterScript......')
    driver.get(routes['charactersMVS'])
    getChaptersData(driver, CHARACTERS)
    time.sleep(2)
    driver.get(routes['wikiMain'])
    skillScript(driver, CHARACTERS)

if not mapSize:    
    print('Executing maspScript......')
    driver.get(routes['wikiMain'])
    time.sleep(2)
    mapScript(driver,MAPS)

finishTime = time.time()

print(f'total time:{finishTime-startTime} seconds elapsed')
driver.close()
driver.quit()
