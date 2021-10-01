import time
import pandas as pd
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from collections import OrderedDict
from pprint import pprint


options = Options()
options.headless = True


urls = ['bangladesh-25/', 'bangladesh-25/alpha-a', 'bangladesh-25/alpha-b', 'bangladesh-25/alpha-c', 'bangladesh-25/alpha-d',
        'bangladesh-25/alpha-e', 'bangladesh-25/alpha-f', 'bangladesh-25/alpha-g', 'bangladesh-25/alpha-h', 'bangladesh-25/alpha-i',
        'bangladesh-25/alpha-j', 'bangladesh-25/alpha-k', 'bangladesh-25/alpha-l', 'bangladesh-25/alpha-m', 'bangladesh-25/alpha-n',
        'bangladesh-25/alpha-o', 'bangladesh-25/alpha-p', 'bangladesh-25/alpha-q', 'bangladesh-25/alpha-r', 'bangladesh-25/alpha-s',
        'bangladesh-25/alpha-t', 'bangladesh-25/alpha-u', 'bangladesh-25/alpha-v', 'bangladesh-25/alpha-w', 'bangladesh-25/alpha-x',
        'bangladesh-25/alpha-y', 'bangladesh-25/alpha-z']


initial_data = {}
initial_list = []
final_list = []
player_urls = []


for url in urls:

    driver = webdriver.Chrome(executable_path='C:/Users/arman/chromedriver.exe', options=options)
    driver.get('https://www.espncricinfo.com/player/team/'+url)

    # scroll to the END and retrieve
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.END)

    time.sleep(10)

    content = driver.page_source
    soup = BeautifulSoup(content)

    for elems in soup.findAll('div', {'class': ['index-data p-3', 'index-data p-3 grid-span-2']}):
        name = elems.find('p', attrs='player-index-role')
        age = elems.find(attrs='player-index-age')
        profile_link = elems.find('a', href=True)

        initial_data['Name'] = name.text
        initial_data['Age'] = age.text[5:]
        initial_data['URL'] = profile_link['href']

        initial_list.append(initial_data.copy())

        for k, v in initial_data.copy().items():
            if (k == 'URL') and (v not in player_urls):
                player_urls.append(v)

    driver.close()

pprint(player_urls)

# check and remove duplicate dict values and append to list
for list in initial_list:
    if list not in final_list:
        final_list.append(list)

pprint(final_list, sort_dicts=False)

try:
    columns = ['Name', 'Age', 'URL']
    with open('player_names.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for data in final_list:
            writer.writerow(data)
except IOError:
    print("I/O error")



bowling_header = []
bowling_data = []
batting_header = []
batting_and_fielding = []

for url in player_urls:

    driver = webdriver.Chrome(executable_path='C:/Users/arman/chromedriver.exe', options=options)
    driver.get('https://www.espncricinfo.com'+url)

    content = driver.page_source
    soup = BeautifulSoup(content)

    for table in soup.findAll('table', attrs='table standings-widget-table text-center mb-0 border-bottom'):
        find_parent = table.parent.parent.find('h5')
        pprint(find_parent.text)

        if find_parent.text == 'Batting & Fielding':
            if not batting_header:
                for header in table.find_all('th'):
                    batting_header.append(header.text)

            for data in table.find_all('tr')[1:]:
                td = data.find_all('td')
                r = [i.text.replace('\n', '') for i in td]
                batting_and_fielding.append(r)
            batting_and_fielding.append('\n')

        if find_parent.text == 'Bowling':
            if not bowling_header:
                for header in table.find_all('th'):
                    bowling_header.append(header.text)

            for data in table.find_all('tr')[1:]:
                td = data.find_all('td')
                r = [i.text.replace('\n', '') for i in td]
                bowling_data.append(r)
            bowling_data.append('\n')

driver.close()
driver.quit()

"""print(batting_header)
print(batting_and_fielding)
print(bowling_header)
print(bowling_data)"""

with open('batting_data.csv', 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(batting_header)
    for row in batting_and_fielding:
        write.writerow(row)

with open('bowling_data.csv', 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(bowling_header)
    for row in bowling_data:
        write.writerow(row)
