from selenium.webdriver import Chrome
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

# Please download chromedriver for windows to this directory (scrape_data)
path = 'chromedriver.exe'
browser = Chrome(path)
browser.get('https://www.nationaalrapporteur.nl/publicaties/')

# Save data in a pandas dataframe
df = pd.DataFrame(columns=['News', 'Meta', 'Intro', 'Article', 'PDFs'])
excep = 0
try:
    results = browser.find_element_by_css_selector('#content > div.common.results')
    links = results.find_elements_by_tag_name("a")

    for i in range(len(links)):
        print('Link: ', i+1)
        element = browser.find_element_by_css_selector('#content > div.common.results').find_elements_by_tag_name("a")[i]
        element.click()
        browser.implicitly_wait(3)
        browser.switch_to.window(browser.window_handles[0])
        new_element = browser.find_element_by_css_selector('#content > div > div.intro > p')
        print(new_element.text)
        browser.back()
        print('===============================================================')

except:
    excep = 1
    print("Exception")
    browser.close()


if excep == 0:
    browser.close()