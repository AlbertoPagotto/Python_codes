###########################################
# AUTHOR: Alberto Pagotto
# Last version: 26/11/2023
# To do: make the results saved in a specific folder. At the beginning check if the resulting file is already available

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd

def error_message(message):
    print(f"[ERROR] {message}")
    driver.quit()
    exit()

def season_fun():
    season=input('Which season do you want to analyze (format xxxx/xxxx)? ')
    if not('/' in season):
        print('Input not valid. Use the indicated format.')
        return season_fun()
    elif int(season.split('/')[0])!=int(season.split('/')[1])-1:
        print('Input not valid. The indicated season does not exist.')
        return season_fun()
    elif not(int(season.split('/')[0])>1870):
        print('Input not valid. You cannot go before 1870.')
        return season_fun()
    else:
        print(f'You have selected season {season}.')
        return season

def transfer_window_fun():
    transfer_window=input('Which window are you interested in (all, summer, winter)? ')
    if not(transfer_window.lower() in transfer_dict.keys()):
        print('Input not valid (avoid spaces).')
        return transfer_window_fun()
    else:
        print(f'You have selected the following transfer window: {transfer_window}.')
        return transfer_window

def position_fun():
    position=input('Which position are you interested in (all, goalkeepers, defenders, midfielders, forwards)? ')
    if not(position.lower() in position_dict.keys()):
        print('Input not valid (avoid spaces).')
        return position_fun()
    else:
        print(f'You have selected the following position: {position}.')
        return position
def age_fun():
    age=input('Which position are you interested in (all, goalkeepers, defenders, midfielders, forwards)? ')
    if not(age.lower() in age_dict.keys()):
        print('Input not valid (avoid spaces).')
        return age_fun()
    else:
        print(f'You have selected the following age: {age}.')
        return age

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

transfer_dict={
    'all': 'alle',
    'summer': 'sommer',
    'winter': 'winter'
}
position_dict={
    'all':'',
    'goalkeepers':'Torwart',
    'defenders':'Abwehr',
    'midfielders':'Mittelfeld',
    'forward':'Sturm'
}
age_dict={
    'all':'',
    'u15':'u15',
    'u16':'u16',
    'u17':'u17',
    'u18':'u18',
    'u19':'u19',
    'u20':'u20',
    'u21':'u21',
    'u22':'u22',
    'u23':'u23',
    '23-30':'23-30',
    'o30':'o30',
    'o31':'o31',
    'o30':'o30',
    'o32':'o32',
    'o33':'o33',
    'o34':'o34',
    'o35':'o35'
}

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
    # if pg>max_page: #Okay for now, but improvable maybe with recurrence
    #     break
    try:
        element_next=driver.find_element(By.CSS_SELECTOR,'a.tm-pagination__link[title="Go to next page"]')
        #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'a.tm-pagination__link[title="Go to next page"]')))
        element_click=WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element_next))
        element_click.click() #Apparently, splitting these two lines is fundamental to avoid errors
        print(f'[INFO] Page {pg} accessed successfully.')
    except exceptions.NoSuchElementException:
        error_message(f'Failed to go to page {pg}. Button not found.')
        break
    except exceptions.ElementClickInterceptedException:
        error_message(f'Failed to go to page {pg}. Element intecepted.')
        break
## Closing the driver
driver.quit()
print('[INFO] Driver closed successfully.')

############################################################################################

## CLEAN THE DATA
odd_players=element_clean(odd_players)
even_players=element_clean(even_players)

## CREATE A DATAFRAME
data_transfer=[]
for ii in range(0,len(odd_players+even_players)):
    if ii%2==0:
        data_transfer.append(odd_players[int(ii/2)])
    else:
        data_transfer.append(even_players[int((ii-1)/2)])
df=pd.DataFrame(data=data_transfer,columns=['Rank','Name','Age','Value','Team','Championship','Fee'])
df.drop('Rank',axis=1,inplace=True)

## CREATE a CSV FILE
name_csv=f'Fees_{season_id}_{transfer_window}_{position}.csv'
df.to_csv(name_csv,index=False)
print(f'[INFO] File {name_csv} written successfully.')