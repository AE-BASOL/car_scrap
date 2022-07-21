# %% import
from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

# %% HTTP request (store website in variable)
site_links = []
initLink = "https://www.arabam.com/ikinci-el/otomobil?take=50&page={}"
site_General = "https://www.arabam.com"

for i in range(1, 51, 1):
    site_links.append(initLink.format(i))

# %% HTTP REQUEST (get request)
links = []
for i in range(0, 50, 1):
    response = requests.get(site_links[i], headers=headers)
    response.status_code  # HTTP REQUEST (status code) need 200 not 429
    soup = BeautifulSoup(response.content, "html.parser")

    results = soup.find_all("tr", class_="listing-list-item")
    print(len(results))

    for result in results:
        href_tags = result.find("a")["href"]
        birlesim = site_General + href_tags
        print(birlesim)
        links.append(birlesim)

# %% GET INSIDE LINK
car_price = []
car_location = []
car_sheet = pd.DataFrame({'Inside Links': links, 'Price': car_price, 'Location': car_location})

for i in range(0, 2500, 1):
    response_inside = requests.get(links[i], headers=headers)
    soup_inside = BeautifulSoup(response_inside.content, "html.parser")
    results_inside = soup_inside.find_all("div", class_="banner-column-detail bcd-mid-extended p10 bg-white")
    print(i)

    for result_inside in results_inside:
        car_price.append(
            result_inside.find("span", {"class": "color-red4 font-default-plusmore bold fl"}).get_text().strip())
        car_location.append(result_inside.find("p", {
            "class": "one-line-overflow font-default-minus pt4 color-black2018 bold"}).get_text().strip())

        car_information = []
        data1 = result_inside.find('ul')
        for li in data1.find_all("li"): #18 kere dönücek çünkü 18 tane li var
            car_information.append(li.find_all(["span","a"]).text.strip())
            car_temp = pd.DataFrame({'data': car_information})
            T_car_temp = car_temp.T
            T_car_temp.to_excel(r'C:\Users\Ahmet.basol\Desktop\Projects\Idea\car_scrap\car_sheet.xlsx', sheet_name='car_data', columns="3", index=False, header=True)

    if len(results_inside) == 0:
        car_price.append("none")
        car_location.append("none")

car_sheet.to_excel(r'C:\Users\Ahmet.basol\Desktop\Projects\Idea\car_scrap\car_sheet.xlsx', sheet_name='car_data', index=False , header=True)

# %% INSIDE RESULTS
results_inside = soup_inside.find_all("div", class_="banner-column-detail bcd-mid-extended p10 bg-white")
print(len(results_inside))

car_information = []
data1 = results_inside[0].find('ul')

for li in data1.find_all("li"):
    car_information.append(li.find_all(["span", "a"])[0].text.strip())
    car_information.append(li.find_all(["span", "a"])[1].text.strip())

car_temp = pd.DataFrame({'data': car_information})
T_car_temp = car_temp.T

i = 0

if len(car_information) == 36:
    values = []
    for i in range(36):
        if i % 2 == 1:
            values.append(car_information[i])
        i += 1
    # SQL'e verileri at

car_deneme = pd.DataFrame({'data': car_information})



print(car_information)
print(car_information)
#T_car_temp.to_excel(r'C:\Users\Ahmet.basol\Desktop\Projects\Idea\car_scrap\car_sheet.xlsx', sheet_name='car_data', columns=["id","İlan Tarihi","Marka","Seri","Model","Yıl","Kilometre","Vites Tipi","Yakıt Tipi","Kasa Tipi","Motor Hacmi","Motor Gücü","Çekiş","Ort. Yakıt Tüketimi","Yakıt Deposu","Boya-değişen","Takasa Uygun:","Kimden"], index=False, header=True)
