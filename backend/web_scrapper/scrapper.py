from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
# browser = webdriver.Chrome(executable_path="./drivers/chromedriver")
# browser.get('https://docs.jivox.com/jivox-documentation/about-jivox-iq-platform')
# html = browser.find_element(By.TAG_NAME, 'html').get_attribute('innerHTML')
# print(html)
# browser.quit()

import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# We don't want to open the webpage in a real browser, but in a headless browser.
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path="./drivers/chromedriver")

# Now we use the driver to render the JavaScript webpage.
driver.get("https://docs.jivox.com/jivox-documentation/about-jivox-iq-platform")
# page_source stores the HTML markup of the webpage, not the JavaScript code.
page_source = driver.page_source

# And we can then parse the rendered HTML markup as usual.
tree = html.fromstring(page_source)
# from selenium import webdriver
# from os import getcwd

buyers = tree.xpath('//*[@id="title-28071"]/text()')
# driver = webdriver.PhantomJS(executable_path=getcwd() + "/phantomjs")

print(buyers)

# driver.get("https://docs.jivox.com/jivox-documentation/about-jivox-iq-platform")
# p_element = driver.find_element_by_id(id_='index-scrollbar')
# print(p_element.text)