#!/usr/bin/env python #
"""
Transfermarkt_downloader
This script downloads player data from Transfermarkt.com.
"""
__author__ = 'Alberto Pagotto'
__copyright__ = 'Transfermarkt_downloader'
__credits__ = ['Alberto Pagotto']
__version__ = '1.0'
__maintainer__ = 'Alberto Pagotto'
__email__ = 'albertopagotto96@gmail.com'
__status__ = 'Development'

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

current_directory=os.path.dirname(os.path.realpath(__file__))
if not('data' in os.listdir(current_directory)):
    os.mkdir('data')

print(f"AUTHOR: {__author__}")
print(f"COPYRIGHT: {__copyright__}")
print(f"CREDITS: {__credits__}")
print(f"VERSION: {__version__}")
print(f"EMAIL: {__email__}")

## GENERATE THE URL TO ACCESS
season=season_fun()
transfer_window=transfer_window_fun()
position=position_fun()
age=input('What age are you interested in (all, u15-23, 23-30,o30-35)? ')
season_id=season.split('/')[0]
transfer_id=transfer_dict[transfer_window.lower()]
position_id=position_dict[position.lower()]
age_id=age_dict[age.lower()]
name_csv=f'Fees_{season_id}_{transfer_id}_{position_id}_{age_id}.csv'
if os.path.exists(f'{current_directory}\data\{name_csv}'):
    print('[WARNING] The file already exists. The script will be crashed.')
    exit()
url_season=f'https://www.transfermarkt.com/transfers/saisontransfers/statistik/top/plus/0/galerie/0?saison_id={season_id}transfers&transferfenster={transfer_id}&land_id=&ausrichtung={position_id}&spielerposition_id=&altersklasse={age}&leihe='


## SET GOOGLE CHROME TO ACCESS TRANSFERMARKT
chrome_driver_path = r"...\chromedriver.exe" #Specify the path for chromedriver.exe (if necessary, install it)
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
    error_message('Cookies not rejected: frame not found. It could be that the frame number was updated by Transfermarkt.')
except exceptions.NoSuchElementException:
    error_message('Cookies not rejected: button not found.')

driver.switch_to.default_content()

# Initialize variables
pg=1
data_transfer=[]
max_page=20 #max page number to read in case all the options are selected is 80 (not clear how to find it)

## Find market values
while (pg<=max_page):
    try:
        time.sleep(10)
        odd_players_page=driver.find_elements(by=By.CLASS_NAME,value='odd')
        even_players_page=driver.find_elements(by=By.CLASS_NAME,value='even')
        players_page=[element.text.split('\n') for element in odd_players_page+even_players_page]
        for players_element in players_page:
            data_transfer.append(players_element)
        print(f"[INFO] Players found successfully at page {pg}.")
    except exceptions.NoSuchElementException:
        error_message(f'Failed to find players at page {pg}.')
        break
    except exceptions.StaleElementReferenceException:
        error_message('Stale element')
        break
    pg+=1
    if pg>max_page:
        break
    # Go to the next page
    try:
        element_next = driver.find_element(By.CSS_SELECTOR, 'a.tm-pagination__link[title="Go to the next page"]')
    except exceptions.NoSuchElementException:
        error_message(f'Failed to go to page {pg}. Button not found. It could be that Transfermarkt changed the title or the class name.')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_next))
    driver.execute_script("arguments[0].click();", element_next)

## Closing the driver
driver.quit()
print('[INFO] Driver closed successfully.')

## CLEAN THE DATA

for index, element in enumerate(data_transfer):
    if 'loan transfer' in element:
        jj=element.index('loan transfer')
        data_transfer[index][jj]='€0m'
    elif 'free transfer' in element:
        jj=element.index('free transfer')
        data_transfer[index][jj]='€0m'
    elif 'Loan fee:' in element:
        data_transfer[index].remove('Loan fee:')
    elif ('?' in element) or (len(element)<6):
        data_transfer.remove(element)
data_transfer=[element[0:2]+element[3].split(' ')+element[4:] for element in data_transfer]

## CREATE A DATAFRAME
df=pd.DataFrame(data=data_transfer,columns=['Rank','Name','Age','Value','Team','Championship','Fee'])
df.drop('Rank',axis=1,inplace=True)

new_age=[]
for age in df['Age'].tolist():
    if age.isdigit():
        new_age.append(int(age))
    else:
        new_age.append(0)

df['Age']=new_age


new_fees=[]
for fee in df['Fee'].tolist():
    if (fee[-1]=='m' or fee[-1]=='k'):
        new_f=float(fee[1:-1])*((10**3)*(fee[-1]=='k')+(10**6)*(fee[-1]=='m'))
    new_fees.append(new_f)
df['Fee']=new_fees

new_values=[]
for fee in df['Value'].tolist():
    if fee[-1]=='m' or fee[-1]=='k':
        new_v=float(fee[1:-1])*((10**3)*(fee[-1]=='k')+(10**6)*(fee[-1]=='m'))
    new_values.append(new_v)
df['Value']=new_values

## CREATE a CSV FILE
df.to_csv(f'{current_directory}\data\{name_csv}',index=False)
print(f'[INFO] File {name_csv} written successfully.')
