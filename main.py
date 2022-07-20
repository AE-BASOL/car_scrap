# %% import
from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl

# %% HTTP request (store website in variable)
arabamCom_CarSales = "https://www.arabam.com/ikinci-el/otomobil/fiat?take=50&page=1"
arabamCom_website = "https://www.arabam.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

# %% HTTP REQUEST (get request)
response = requests.get(arabamCom_CarSales, headers=headers)

# %% HTTP REQUEST (status code) need 200 not 429
response.status_code

# %% SOUP OBJECT
soup = BeautifulSoup(response.content, "html.parser")
soup

# %% RESULTS
results = soup.find_all("tr", class_="listing-list-item")
print(len(results))
links = []

for result in results:
    href_tags = result.find("a")["href"]
    birlesim = arabamCom_website + href_tags
    print(birlesim)
    links.append(birlesim)

print(links)

#%% WRITE TXT
with open(r'car_links.txt', 'w') as fp:
    for item in links:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')

# %% GET INSIDE LINK
response_inside = requests.get(birlesim, headers=headers)
print(response_inside.status_code)

soup_inside = BeautifulSoup(response_inside.content, "html.parser")
soup_inside

# %% INSIDE RESULTS
results_inside = soup_inside.find_all("div", class_="banner-column-detail bcd-mid-extended p10 bg-white")
print(len(results_inside))

# %% GET VARIABLES
car_price = results_inside[0].find("div", {"class": "df df-center w50"}).get_text().strip()
car_location = results_inside[0].find("p", {
"class": "one-line-overflow font-default-minus pt4 color-black2018 bold"}).get_text().strip()

car_list = []
data1 = results_inside[0].find('ul')

for li in data1.find_all("li"):
    car_list.append(li.find_all(["span", "a"])[1].text.strip())

car_list.insert(0, car_location)
car_list.insert(0, car_price)
print(car_list)
