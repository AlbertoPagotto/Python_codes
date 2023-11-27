###########################################
# AUTHOR: Alberto Pagotto
# Last version: 26/11/2023
# To do: make the results saved in a specific folder. At the beginning check if the resulting file is already available

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from transfermarkt_fun import *
import os
import time
import pandas as pd

def error_message(message):
    print(f"[ERROR] {message}")
    driver.quit()
    exit()

def element_clean(players):
    for element in players:
        if 'loan transfer' in element:
            jj=element.index('loan transfer')
            element[jj]='€0m'
        elif 'free transfer' in element:
            jj=element.index('free transfer')
            element[jj]='€0m'
        elif 'Loan fee:' in element:
            element.remove('Loan fee:')

    return [element[0:2]+element[3].split(' ')+element[4:] for element in players]

current_directory=os.getcwd()
## GENERATE THE URL TO ACCESS
# season=season_fun()
# transfer_window=transfer_window_fun()
# position=position_fun()
# age=input('What age are you interested in (all, u15-23, 23-30,o30-35)? ')
season='2022/2023'
transfer_window='all'
position='all'
age='all'
season_id=season.split('/')[0]
transfer_id=transfer_dict[transfer_window.lower()]
position_id=position_dict[position.lower()]
age_id=age_dict[age.lower()]
name_csv=f'Fees_{season_id}_{transfer_id}_{position_id}_{age_id}.csv'
url_season=f'https://www.transfermarkt.com/transfers/saisontransfers/statistik/top/plus/0/galerie/0?saison_id={season_id}transfers&transferfenster={transfer_id}&land_id=&ausrichtung={position_id}&spielerposition_id=&altersklasse={age}&leihe='


## SET GOOGLE CHROME TO ACCESS TRANSFERMARKT
chrome_driver_path = r"C:\Users\A315-55G-7045\Downloads\chromedriver_win32\chromedriver.exe"
chrome_options = webdriver.ChromeOptions() # Keep the browser open if the script crashes.
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=chrome_options)
print("[INFO] Driver created successfully.")
driver.get(url=url_season)
print("[INFO] Transfermarkt accessed successfully.")

## Reject the cookies
try:
    driver.switch_to.frame("sp_message_iframe_939800")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//button[contains(@title,'Accept and continue')]"))).click()
    print("[INFO] Cookies accepted successfully.")
except exceptions.NoSuchFrameException:
    error_message('Cookies not rejected: button not found.')
except exceptions.NoSuchElementException:
    error_message('Cookies not rejected: button not found.')

driver.switch_to.default_content()

# Initialize variables
pg=1
odd_players=[]
even_players=[]
max_page=80 #max page number to read in case all the options are selected (not clear how to find it)

## Find market values
while (pg<=max_page):
    try:
        time.sleep(10)
        odd_players_page=driver.find_elements(by=By.CLASS_NAME,value='odd')
        odd_players_page=[element.text.split('\n') for element in odd_players_page]
        for odd_players_element in odd_players_page:
            odd_players.append(odd_players_element)
        even_players_page=driver.find_elements(by=By.CLASS_NAME,value='even')
        even_players_page=[element.text.split('\n') for element in even_players_page]
        for even_players_element in even_players_page:
            even_players.append(even_players_element)
        print(f"[INFO] Players found successfully at page {pg}.")
    except exceptions.NoSuchElementException:
        error_message(f'Failed to find players at page {pg}.')
        break
    except exceptions.StaleElementReferenceException:
        error_message('Stale element')
        break
    # Go to the next page
    pg+=1
    if pg>max_page: #Okay for now, but improvable maybe with recurrence
        break
    for attempt in range(9):
        try:
            element_next = driver.find_element(By.CSS_SELECTOR, 'a.tm-pagination__link[title="Go to next page"]')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_next))
            driver.execute_script("arguments[0].click();", element_next)
            break
        except exceptions.ElementClickInterceptedException:
            print(f"Click intercepted on attempt {attempt + 1}")
            time.sleep(1)
        except exceptions.NoSuchElementException:
            error_message(f'Failed to go to page {pg}. Button not found.')
            break
    #error_message(f'Failed to go to page {pg}. Element intecepted.')

## Closing the driver
driver.quit()
print('[INFO] Driver closed successfully.')

############################################################################################

## CLEAN THE DATA
odd_players=element_clean(odd_players)
even_players=element_clean(even_players)
data_transfer=odd_players+even_players

## CREATE A DATAFRAME
# data_transfer=[]
# for ii in range(0,len(odd_players+even_players)):
#     if ii%2==0:
#         data_transfer.append(odd_players[int(ii/2)])
#     else:
#         data_transfer.append(even_players[int((ii-1)/2)])
df=pd.DataFrame(data=data_transfer,columns=['Rank','Name','Age','Value','Team','Championship','Fee'])
df.drop('Rank',axis=1,inplace=True)

## CREATE a CSV FILE
df.to_csv(name_csv,index=False)
print(f'[INFO] File {name_csv} written successfully.')