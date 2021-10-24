import time
import pandas as pd
import csv
import os
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from collections import OrderedDict
from pprint import pprint



def writebattingcsv(header, data):
    # csv_filename = 'batting_data.csv'

    if not os.path.exists('batting_data.csv'):
        with open('batting_data.csv', 'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(header)
            f.close()

    with open('batting_data.csv', 'a', newline='') as f:
        write = csv.writer(f)
        for row in data:
            write.writerow(row)



def writebowlingcsv(header, data):
    if not os.path.exists('bowling_data.csv'):
        with open('bowling_data.csv', 'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(header)
            f.close()


    with open('bowling_data.csv', 'a', newline='') as f:
        write = csv.writer(f)
        for row in data:
            write.writerow(row)


def writeumpirecsv(header, data):
    if not os.path.exists('umpire_data.csv'):
        with open('umpire_data.csv', 'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(header)
            f.close()

    with open('umpire_data.csv', 'a', newline='') as f:
        write = csv.writer(f)
        for row in data:
            write.writerow(row)


options = Options()
options.headless = True


driver = webdriver.Chrome(executable_path='C:/Users/arman/chromedriver.exe', options=options)


urls = ['bangladesh-25/', 'bangladesh-25/alpha-a', 'bangladesh-25/alpha-b', 'bangladesh-25/alpha-c', 'bangladesh-25/alpha-d', 'bangladesh-25/alpha-e',
        'bangladesh-25/alpha-f', 'bangladesh-25/alpha-g', 'bangladesh-25/alpha-h', 'bangladesh-25/alpha-i', 'bangladesh-25/alpha-j', 'bangladesh-25/alpha-k',
        'bangladesh-25/alpha-l', 'bangladesh-25/alpha-m', 'bangladesh-25/alpha-n', 'bangladesh-25/alpha-o', 'bangladesh-25/alpha-p', 'bangladesh-25/alpha-q',
        'bangladesh-25/alpha-r', 'bangladesh-25/alpha-s', 'bangladesh-25/alpha-t', 'bangladesh-25/alpha-u', 'bangladesh-25/alpha-v', 'bangladesh-25/alpha-w',
        'bangladesh-25/alpha-x', 'bangladesh-25/alpha-y', 'bangladesh-25/alpha-z']


initial_data = {}
initial_list = []
final_list = []
player_urls = []
pickle_list = []
# filename = 'pickle_list.pkl'


"""if not os.path.exists(filename):
    pickle_data = open(filename, 'wb')
    pickle.dump(pickle_list, pickle_data)
else:
    pickle_data = open(filename, 'rb')
    pickle_list = pickle.load(pickle_data)"""


for url in urls:

    driver.get('https://www.espncricinfo.com/player/team/'+url)

    # scroll to the END and retrieve
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.END)

    time.sleep(5)

    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')

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
umpire_header = []
umpire_data = []
pickle_dict = dict()
resume_list = []


filename = "player_data.pkl"


if not os.path.exists(filename):
    pickle_data = open(filename, 'wb')
    pickle.dump(pickle_dict, pickle_data)
else:
    pickle_data = open(filename, 'rb')
    pickle_dict = pickle.load(pickle_data)

    for k, v in pickle_dict.items():

        for value in v.values():
            if value == 0:
                while player_urls.index(k):
                    player_urls.pop(0)

                print(player_urls)
            else:
                continue
    print(pickle_dict)


driver = webdriver.Chrome(executable_path='C:/Users/arman/chromedriver.exe', options=options)


for url in player_urls:

    if url in pickle_dict:
        pickle_data = open(filename, 'rb')
        # print(pickle_dict)
    else:
        pickle_data = open(filename, 'wb')
        pickle_dict[url] = {}
        pickle.dump(pickle_dict, pickle_data)
    # print(pickle_dict)

    driver.get('https://www.espncricinfo.com'+url)

    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')


    for table in soup.findAll('table', attrs='table standings-widget-table text-center mb-0 border-bottom'):
        find_parent = table.parent.parent.find('h5')
        pprint(find_parent.text)
        # print(pickle_dict)


        if find_parent.text == 'Batting & Fielding':
            pickle_data = open(filename, 'wb')
            pickle_dict[url]['Batting'] = 0
            pickle.dump(pickle_dict, pickle_data)
            print(pickle_dict)


            time.sleep(3)


            if not batting_header:
                batting_header.append("Unique_ID")
                for header in table.find_all('th'):
                    batting_header.append(header.text)

            batting_and_fielding = []

            for data in table.find_all('tr')[1:]:
                td = data.find_all('td')
                r = [i.text.replace('\n', '') for i in td]
                r.insert(0, url)
                batting_and_fielding.append(r)
            # batting_and_fielding.append('\n')

            writebattingcsv(batting_header, batting_and_fielding)

            pickle_dict[url]['Batting'] = 1
            pickle.dump(pickle_dict, pickle_data)



        if find_parent.text == 'Bowling':
            pickle_dict[url]['Bowling'] = 0
            pickle.dump(pickle_dict, pickle_data)
            print(pickle_dict)

            time.sleep(3)

            if not bowling_header:
                bowling_header.append("Unique_ID")
                for header in table.find_all('th'):
                    bowling_header.append(header.text)

            bowling_data = []

            for data in table.find_all('tr')[1:]:
                td = data.find_all('td')
                r = [i.text.replace('\n', '') for i in td]
                r.insert(0, url)
                bowling_data.append(r)
            # bowling_data.append('\n')

            writebowlingcsv(bowling_header, bowling_data)

            pickle_data = open(filename, 'wb')
            pickle_dict[url]['Bowling'] = 1
            pickle.dump(pickle_dict, pickle_data)
            pickle_data.close()



        if find_parent.text == 'Umpire & Referee':
            pickle_data = open(filename, 'wb')
            pickle_dict[url]['Umpire'] = 0
            pickle.dump(pickle_dict, pickle_data)
            print(pickle_dict)


            if not umpire_header:
                umpire_header.append("Unique_ID")
                for header in table.find_all('th'):
                    umpire_header.append(header.text)

            umpire_data = []

            for data in table.find_all('tr')[1:]:
                td = data.find_all('td')
                r = [i.text.replace('\n', '') for i in td]
                r.insert(0, url)
                umpire_data.append(r)
            # bowling_data.append('\n')

            writeumpirecsv(umpire_header, umpire_data)

            pickle_dict[url]['Umpire'] = 1
            pickle.dump(pickle_dict, pickle_data)


    print(pickle_dict)
    # driver.close()
    # driver.quit()

print(batting_header)
print(batting_and_fielding)
# print(bowling_header)
# print(bowling_data)
# print(umpire_header)
# print(umpire_data)


