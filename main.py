# %% import
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import pandas as pd

f = open("Car_Info.tsv", "w")

# %% HTTP request (store website in variable)
arabamCom_CarSales = "https://www.arabam.com/ikinci-el/otomobil/fiat?take=50&page=1"
arabamCom_website = "https://www.arabam.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

# %% Assign car adverts links to set
wantedlinks = []

for i in range(1, 51, 1):
    response = requests.get(arabamCom_CarSales,
                            headers=headers)  # https://www.arabam.com/ikinci-el/otomobil/fiat?take=50&page=1
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find_all("tr", class_="listing-list-item")
    for result in results:
        href_tags = result.find("a")["href"]
        birlesim = arabamCom_website + href_tags
        wantedlinks.append(birlesim)

car_dealer = pd.DataFrame({'links':wantedlinks})
print(car_dealer)

# %% GET INSIDE LINK
detailedCodes = []

for i in wantedlinks:
    response_inside = requests.get(str(i), headers=headers)
    print(response_inside.status_code)
    soup_inside = BeautifulSoup(response_inside.content, features="html.parser")
    detailedCodes.append(soup_inside)
    print(i)

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
