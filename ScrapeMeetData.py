# Python, web scraping a PL Meet's data
# Python version 3.10.4
# Requires selenium and the appropriate web driver
# The version of chrome driver in the folder is 103.0.5060.53, win-32
# The version of geckodriver (Firefox) in the folder is 0.31.0, win-64

# import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

MEET_URL = 'https://liftingcast.com/meets/m6bqe7e6d0lx/roster'
MEET_NAME = 'USAPL Nightmare Before Liftmass II'
# LIFTER_DATA = ['Team', 'Divisions', 'Weight_Class', 'Platform', 'Session', 
#                'Flight', 'Age', 'Age_Coef', 'Body_Weight', 
#                'Wilks_Coef', 'DOTS_Coef', 'Lot_Num', 
#                'Squat_Rack_Height', 
#                'Bench_Rack_Height', 'Attempts_Out']


# First step is to get the lifter data per unassigned 
# flight

# Have to wait past the load screen or else the HTML scraped won't have
# lifter data and links
# web_options = Options()
# web_options.add_argument('--headless')
driver = webdriver.Firefox()
driver.get(MEET_URL)
WebDriverWait(driver, 10).until(lambda driver: driver.title == MEET_NAME)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Grab the URL per lifter for the meet
# These data are under the
# <div class = "session-roster"> overhead, and the specifics
# are under:
# <div class = "session-content"> 
# <div class = "platform-list-wrapper">
# <ul class = "platform-list">
# Then nested into a </li> tag
platforms = soup.find_all('ul', {'class': 'platform-list'})

if len(platforms) > 0:
    print("Loaded platform list")
else:
    print("No platform list")
# n_platforms = range(len(platforms))

lifter_dict = {}
for platform in range(len(platforms)):
    lifters = platforms[platform]
    for lifter in range(1, len(lifters.find_all('a'))):
        # For now this doesn't check for if lifters have the same
        # name, but that's not a problem for now
        lifter_info = lifters.find_all('a')[lifter]
        lifter_dict[lifter_info.text] = lifter_info['href']

# Again, we have to wait for a second for the data to load per lifter

# driver = webdriver.Firefox(options = web_options)
lifter_data = {}
for lifter_name, lifter_url in list(lifter_dict.items()):
    LIFTER_URL = "https://liftingcast.com" + lifter_url + "/info"
    LIFTER_URL_TITLE = lifter_name + " - " + MEET_NAME
    driver.get(LIFTER_URL)
    WebDriverWait(driver, 5).until(lambda driver: 
                                   driver.title == LIFTER_URL_TITLE)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    data = list(soup.find_all('div', {'class': 'info-row'}))
    print("Accessing lifter data for " + lifter_name)
    data_compiled = []
    for item in range(1, len(data)):
        data_entry = data[item].text.split(":")[1].strip()
        data_compiled.append(data_entry)
    lifter_data[lifter_name] = data_compiled
    print("Processed " + lifter_name)

# LIFTER_DATA = ['Team', 'Divisions', 'Weight_Class', 'Platform', 'Session', 
#                'Flight', 'Age', 'Age_Coef', 'Body_Weight', 
#                'Wilks_Coef', 'DOTS_Coef', 'Lot_Num', 
#                'Squat_Rack_Height', 
#                'Bench_Rack_Height', 'Attempts_Out']


# print(platforms.prettify())
# print(results.prettify())


# session_div = soup.find_all('div', class_='info-row')

# results = soup.find('div', class_ = "session-content")