###########################################
# AUTHOR: Alberto Pagotto
# Starting date: 01/11/2023
# Last version: 04/11/2023

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import matplotlib.pyplot as plt
import time

def error_message(message):
    print(f"[ERROR] {message}")
    driver.quit()

## SET GOOGLE CHROME TO ACCESS TRANSFERMARKT
chrome_driver_path = r"C:\Users\A315-55G-7045\Downloads\chromedriver_win32\chromedriver.exe"
chrome_options = webdriver.ChromeOptions() # Keep the browser open if the script crashes.
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=chrome_options)
print("[INFO] Driver created successfully.")
url_transfermarkt='https://www.transfermarkt.com/statistik/saisontransfers'
driver.get(url=url_transfermarkt)
print("[INFO] Transfermarkt accessed successfully.")

## REJECT THE COOKIES
try:
    driver.switch_to.frame("sp_message_iframe_851946")
    driver.find_element(by=By.XPATH,value="//button[contains(@title,'REJECT ALL')]").click()
    print("[INFO] Cookies rejected successfully.")
    driver.switch_to.default_content()
except:
    error_message('Cookies not rejected.')
try:
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR,'a.sort-link[href="/statistik/saisontransfers?sort=abloese_wert.desc"]'))).click()
except:
    error_message('Failed to sort the players by fee.')

################################################################################################################################################################################
# Initialize variables
fees_list=[]
pg=1
max_page=80 #max page number to read
while (pg<=max_page):
## Find market values
    try:
        time.sleep(10)
        fees=driver.find_elements(by=By.CLASS_NAME,value='rechts')
        for element in fees[3:3+2*25:2]: #there are 25 results
            fees_list.append(element.text)
        print(f"[INFO] Players found successfully at page {pg}.")
    except exceptions.NoSuchElementException:
        error_message(f'Failed to find players at page {pg}.')
        break
    except exceptions.StaleElementReferenceException:
        error_message('Stale element')
        break

    # Go to the next page
    try:
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR,'a.tm-pagination__link[title="Go to next page"]'))).click()
        pg+=1
        print(f'[INFO] Page {pg} accessed successfully.')
    except:
        error_message(f'Failed to go to page {pg}.')
        break

## CLOSING THE DRIVER
driver.quit()
print('[INFO] Driver closed successfully')



## CLEANING THE LIST FROM loans and turn m and k into numbers
fees_list=[fee[1:] for fee in fees_list if ("transfer" not in fee)]
fees_list=[fee[1:] for fee in fees_list if ("fee" not in fee)]
fees_list=[float(fee[:-1])*((10**3)*(fee[-1]=='k')+(10**6)*(fee[-1]=='m')) for fee in fees_list]

# PLOTTING
sorted_data = sorted(fees_list)

N = len(sorted_data)
Q1_index = (N + 1) // 4
Q3_index = (3 * (N + 1)) // 4
Q1 = sorted_data[Q1_index - 1]  # Subtract 1 because of 0-based indexing
Q3 = sorted_data[Q3_index - 1]

data_range = max(sorted_data) - min(sorted_data)

N=len(fees_list)
bin_width = 2*(Q3-Q1)/(N**(1/3))
nr_bins = int(data_range/bin_width)
plt.hist(np.array(fees_list)/(10**5), bins=nr_bins, density=True, alpha=0.6, color='b')
plt.xlabel('Fee (million €)')
plt.ylabel('Probability density')
plt.show()
