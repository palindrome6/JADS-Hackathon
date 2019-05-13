from selenium.webdriver import Chrome
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

# Please download chromedriver for windows to this directory (scrape_data)
path = 'chromedriver.exe'
browser = Chrome(path)
browser.get('https://www.nationaalrapporteur.nl/publicaties/')


excep = 0
try:
    results = browser.find_element_by_css_selector('#content > div.common.results')
    links = results.find_elements_by_tag_name("a")


    print('Link: ', 1)
    # content > div > p
    element = browser.find_element_by_css_selector('#content > div.common.results').find_elements_by_tag_name("a")[0]
    element.click()
    browser.implicitly_wait(3)
    browser.switch_to.window(browser.window_handles[0])


    news = browser.find_elements_by_css_selector("#content > div > h1")[0].text
    meta = browser.find_elements_by_css_selector("#content > div > p")[0].text

    block = browser.find_element_by_css_selector('#content > div')
    divs = block.find_elements_by_tag_name("div")

    paras = []
    downloads = []
    intro = []
    misc = []
    downloaded_data = []
    for i in range(len(divs)):
        tex = divs[i]
        if tex.get_attribute("class") == "intro":
            intro.append(tex.text)
        elif tex.get_attribute("class") == "paragraph":
            paras.append(tex.text)
        elif tex.get_attribute("class") == "download":
            downloads.append(tex.text)
        else:
            misc.append(tex.text)
    downloaded_data.append([news, meta, intro, paras, downloads, misc])

except:
    excep = 1
    print("Exception")
    browser.close()


if excep == 0:
    browser.close()

# Save data in a pandas dataframe
df = pd.DataFrame(downloaded_data, columns=['News', 'Meta', 'Intro', 'Article', 'PDFs', 'Misc'])
print(df)