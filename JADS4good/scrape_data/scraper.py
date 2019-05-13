from selenium.webdriver import Chrome
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

# Please download chromedriver for windows to this directory (scrape_data)
path = 'chromedriver.exe'
browser = Chrome(path)
browser.get('https://www.nationaalrapporteur.nl/publicaties/')

# page_num = 1
#
# while page_num <= 10:
#     if page_num != 1:
#
# results = browser.find_elements_by_class_name('article')
excep = 0
try:
    results = browser.find_element_by_css_selector('#content > div.common.results')
    links = results.find_elements_by_tag_name("a")

    for i in range(len(links)):
        print('Link: ', i+1)
        element = browser.find_element_by_css_selector('#content > div.common.results').find_elements_by_tag_name("a")[i]
        element.click()
        print('Clicked')
        browser.implicitly_wait(3)
        print('Waited')
        browser.switch_to.window(browser.window_handles[0])
        print('Switched to child')
        new_element = browser.find_element_by_css_selector('#content > div > div.intro > p')
        print(new_element.text)
        browser.back()
        print('===============================================================')

except:
    excep = 1
    print("Exception")
    browser.close()

#content > div.common.results > a:nth-child(1)
#content > div.common.results

if excep == 0:
    browser.close()