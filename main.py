# %% import
import pandas
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import glob

import openpyxl

from sklearn.preprocessing import OneHotEncoder

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


# %% HTTP request (store website in variable)
def request_module(initLink):
    site_links = []
    for i in range(1, 51, 1):
        site_links.append(initLink.format(i))
    return site_links

# %% HTTP REQUEST (get request)
def inner_request_module(page_link):
    links = []
    site_general = "https://www.arabam.com"

    for i in range(0, 50, 1):
        response = requests.get(page_link[i], headers=headers)
        response.status_code  # HTTP REQUEST (status code) need 200 not 429

        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("tr", class_="listing-list-item")

        for result in results:
            href_tags = result.find("a")["href"]
            birlesim = site_general + href_tags
            print(birlesim)
            links.append(birlesim)

    return links

# %% GET INSIDE LINK
def getData_module(banner_link):
    car_price = []
    car_location = []
    car_info = []

    ch = "/"
    ch_2 = "."

    for i in range(0, 2500, 1):
        response_inside = requests.get(banner_link[i], headers=headers)
        soup_inside = BeautifulSoup(response_inside.content, "html.parser")
        results_inside = soup_inside.find("div", {"class": "banner-column-detail bcd-mid-extended p10 bg-white"})
        print("\t{}".format(i))

        if results_inside:
            li = results_inside.find("ul").find_all("li")  # kaç tane li var?
            if len(li) == 18:
                car_information_18 = []
                for j in li:
                    # li içinde <a> tagını bul
                    a_link = j.find("a", {"class": "bli-particle semi-bold"})
                    if a_link:
                        car_information_18.append(a_link.get_text().strip())

                    # li içinde <span> tagını bul
                    span = j.find_all("span")
                    if len(span) >= 0:
                        count = 0
                        for k in span:
                            if count % 2 == 1:
                                car_information_18.append(k.get_text().strip())
                            count += 1
                car_info.append(car_information_18)

                car_price.append(
                    results_inside.find("span",{"class": "color-red4 font-default-plusmore bold fl"}).get_text().strip())

                car_location.append(results_inside.find("p", {
                    "class": "one-line-overflow font-default-minus pt4 color-black2018 bold"}).get_text().strip().split(ch,1)[0])

    return car_price,car_location,car_info

# %% Dataframe
def dataFrame_module(price, location, info):

    space = " "

    car_sheet = pd.DataFrame({'Info': info})
    split_df = pd.DataFrame(car_sheet['Info'].tolist())
    split_df.columns = ["id", "İlan Tarihi", "Marka", "Seri", "Model", "Yıl", "Kilometre", "Vites Tipi", "Yakıt Tipi",
                        "Kasa Tipi", "Motor Hacmi", "Motor Gücü", "Çekiş", "Ort. Yakıt Tüketimi", "Yakıt Deposu",
                        "Boya-değişen", "Takasa Uygun", "Kimden"]

    car_main = pd.DataFrame({'Price': price, 'Location': location})
    car_dataframe = pd.concat([car_main, split_df], axis=1)

    #car_dataframe['Price'] = car_dataframe['Price'].str.replace('tl', '')
    #car_dataframe['Price'] = car_dataframe['Price'].str.replace('TL', '')
    #car_dataframe['Price'] = car_dataframe['Price'].str.replace('tL', '')
    #car_dataframe['Price'] = car_dataframe['Price'].str.replace('Tl', '')
    car_dataframe['Price'] = car_dataframe['Price'].str.replace('.', '')
    car_dataframe['Price'] = car_dataframe['Price'].str.split(' ').str[0]
    car_dataframe['Price'] = car_dataframe['Price'].str.replace('-', '')

    car_dataframe['Yıl'] = car_dataframe['Yıl'].str.replace('-', '')

    car_dataframe['İlan Tarihi'] = car_dataframe['İlan Tarihi'].str.replace('Ocak', '01')
    car_dataframe['İlan Tarihi'] = car_dataframe['İlan Tarihi'].str.replace('Şubat', '02')
    car_dataframe['İlan Tarihi'] = car_dataframe['İlan Tarihi'].str.replace('Mart', '03')
    car_dataframe['İlan Tarihi'] = car_dataframe['İlan Tarihi'].str.replace('Nisan', '04')
    car_dataframe['İlan Tarihi'] = car_dataframe['İlan Tarihi'].str.replace('Mayıs', '05')
    car_dataframe['İlan Tarihi'] = car_dataframe['İlan Tarihi'].str.replace('Haziran', '06')
    car_dataframe['İlan Tarihi'] = car_dataframe['İlan Tarihi'].str.replace('Temmuz', '07')
    car_dataframe['İlan Tarihi'] = car_dataframe['İlan Tarihi'].str.replace('Ağustos', '08')
    car_dataframe['İlan Tarihi'] = car_dataframe['İlan Tarihi'].str.replace('Eylül', '09')
    car_dataframe['İlan Tarihi'] = car_dataframe['İlan Tarihi'].str.replace('Ekim', '10')
    car_dataframe['İlan Tarihi'] = car_dataframe['İlan Tarihi'].str.replace('Kasım', '11')
    car_dataframe['İlan Tarihi'] = car_dataframe['İlan Tarihi'].str.replace('Aralık', '12')
    car_dataframe['İlan Tarihi'] = car_dataframe['İlan Tarihi'].str.replace(' ', '/')
    car_dataframe['İlan Tarihi'] = car_dataframe['İlan Tarihi'].str.replace('-', '/')

    #car_dataframe['Kilometre'] = car_dataframe['Kilometre'].str.replace('km', '')
    #car_dataframe['Kilometre'] = car_dataframe['Kilometre'].str.replace('KM', '')
    #car_dataframe['Kilometre'] = car_dataframe['Kilometre'].str.replace('Km', '')
    #car_dataframe['Kilometre'] = car_dataframe['Kilometre'].str.replace('kM', '')
    car_dataframe['Kilometre'] = car_dataframe['Kilometre'].str.replace('.', '')
    car_dataframe['Kilometre'] = car_dataframe['Kilometre'].str.split(' ').str[0]
    car_dataframe['Kilometre'] = car_dataframe['Kilometre'].str.replace('-', '')

    #car_dataframe['Motor Hacmi'] = car_dataframe['Motor Hacmi'].str.replace('cc', '')
    #car_dataframe['Motor Hacmi'] = car_dataframe['Motor Hacmi'].str.replace('CC', '')
    #car_dataframe['Motor Hacmi'] = car_dataframe['Motor Hacmi'].str.replace('Cc', '')
    #car_dataframe['Motor Hacmi'] = car_dataframe['Motor Hacmi'].str.replace('cC', '')
    car_dataframe['Motor Hacmi'] = car_dataframe['Motor Hacmi'].str.replace(',', '.')
    car_dataframe['Motor Hacmi'] = car_dataframe['Motor Hacmi'].str.split(' ').str[0]
    car_dataframe['Motor Hacmi'] = car_dataframe['Motor Hacmi'].str.replace('-', '')

    #car_dataframe['Motor Gücü'] = car_dataframe['Motor Gücü'].str.replace('hp', '')
    #car_dataframe['Motor Gücü'] = car_dataframe['Motor Gücü'].str.replace('HP', '')
    #car_dataframe['Motor Gücü'] = car_dataframe['Motor Gücü'].str.replace('Hp', '')
    #car_dataframe['Motor Gücü'] = car_dataframe['Motor Gücü'].str.replace('hP', '')
    car_dataframe['Motor Gücü'] = car_dataframe['Motor Gücü'].str.replace(',', '.')
    car_dataframe['Motor Gücü'] = car_dataframe['Motor Gücü'].str.split(' ').str[0]
    car_dataframe['Motor Gücü'] = car_dataframe['Motor Gücü'].str.replace('-', '')

    #car_dataframe['Ort. Yakıt Tüketimi'] = car_dataframe['Ort. Yakıt Tüketimi'].str.replace('lt', '')
    #car_dataframe['Ort. Yakıt Tüketimi'] = car_dataframe['Ort. Yakıt Tüketimi'].str.replace('LT', '')
    #car_dataframe['Ort. Yakıt Tüketimi'] = car_dataframe['Ort. Yakıt Tüketimi'].str.replace('Lt', '')
    #car_dataframe['Ort. Yakıt Tüketimi'] = car_dataframe['Ort. Yakıt Tüketimi'].str.replace('lT', '')
    car_dataframe['Ort. Yakıt Tüketimi'] = car_dataframe['Ort. Yakıt Tüketimi'].str.replace(',', '.')
    car_dataframe['Ort. Yakıt Tüketimi'] = car_dataframe['Ort. Yakıt Tüketimi'].str.split(' ').str[0]
    car_dataframe['Ort. Yakıt Tüketimi'] = car_dataframe['Ort. Yakıt Tüketimi'].str.replace('-', '')

    #car_dataframe['Yakıt Deposu'] = car_dataframe['Yakıt Deposu'].str.replace('lt', '')
    #car_dataframe['Yakıt Deposu'] = car_dataframe['Yakıt Deposu'].str.replace('LT', '')
    #car_dataframe['Yakıt Deposu'] = car_dataframe['Yakıt Deposu'].str.replace('Lt', '')
    #car_dataframe['Yakıt Deposu'] = car_dataframe['Yakıt Deposu'].str.replace('lT', '')
    car_dataframe['Yakıt Deposu'] = car_dataframe['Yakıt Deposu'].str.replace(',', '.')
    car_dataframe['Yakıt Deposu'] = car_dataframe['Yakıt Deposu'].str.split(' ').str[0]
    car_dataframe['Yakıt Deposu'] = car_dataframe['Yakıt Deposu'].str.replace('-', '')




    return car_dataframe

# %% One Hot Encoding
def oneHot_module(main_df):

    #df_1 = pd.get_dummies(main_df["Vites Tipi"])
    #df_2 = pd.get_dummies(main_df["Yakıt Tipi"])
    #df_3 = pd.get_dummies(main_df["Kasa Tipi"])
    #df_4 = pd.get_dummies(main_df["Çekiş"])
    #df_5 = pd.get_dummies(main_df["Takasa Uygun"])
    #df_6 = pd.get_dummies(main_df["Kimden"])
    #main_df.drop('Vites Tipi', inplace=True, axis=1)
    #main_df.drop('Yakıt Tipi', inplace=True, axis=1)
    #main_df.drop('Kasa Tipi', inplace=True, axis=1)
    #main_df.drop('Çekiş', inplace=True, axis=1)
    #main_df.drop('Takasa Uygun', inplace=True, axis=1)
    #main_df.drop('Kimden', inplace=True, axis=1)
    #concat_df = pd.concat([main_df, df_1], axis=1)
    #concat_df = pd.concat([concat_df, df_2], axis=1)
    #concat_df = pd.concat([concat_df, df_3], axis=1)
    #concat_df = pd.concat([concat_df, df_4], axis=1)
    #concat_df = pd.concat([concat_df, df_5], axis=1)
    #concat_df = pd.concat([concat_df, df_6], axis=1)

    main_df['İlan Tarihi'] = pd.to_datetime(main_df['İlan Tarihi'],dayfirst=True)
    main_df['Price'] = pd.to_numeric(main_df['Price'])
    main_df['Yıl'] = pd.to_numeric(main_df['Yıl'])
    main_df['Kilometre'] = pd.to_numeric(main_df['Kilometre'])
    main_df['Motor Hacmi'] = pd.to_numeric(main_df['Motor Hacmi'])
    main_df['Motor Gücü'] = pd.to_numeric(main_df['Motor Gücü'])
    main_df['Ort. Yakıt Tüketimi'] = pd.to_numeric(main_df['Ort. Yakıt Tüketimi'])
    main_df['Yakıt Deposu'] = pd.to_numeric(main_df['Yakıt Deposu'])

    return main_df

# %% Merge Csv's
def csvMerge_module(path_csv):
    all_files = glob.glob(path_csv + "/*.csv")

    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.to_csv(r'C:\Users\Ahmet.basol\Desktop\Projects\Idea\car_scrap\final_df.csv', encoding="utf-8", index=None,
                 header=True)

# %%
initLink = ["https://www.arabam.com/ikinci-el/otomobil/fiat?searchText=otomobil&take=50&page={}","https://www.arabam.com/ikinci-el/otomobil/renault?take=50&page={}","https://www.arabam.com/ikinci-el/otomobil/hyundai?take=50&page={}","https://www.arabam.com/ikinci-el/otomobil/ford?take=50&page={}", "https://www.arabam.com/ikinci-el/otomobil/honda?take=50&page={}", "https://www.arabam.com/ikinci-el/otomobil/bmw?take=50&page={}","https://www.arabam.com/ikinci-el/otomobil/mercedes-benz?take=50&page={}","https://www.arabam.com/ikinci-el/otomobil/opel?take=50&page={}","https://www.arabam.com/ikinci-el/otomobil/peugeot?take=50&page={}","https://www.arabam.com/ikinci-el/otomobil/toyota?take=50&page={}"]
path = r'C:\Users\Ahmet.basol\Desktop\Projects\Idea\car_scrap' # use your path

for i in range(10,10,1):
    page_link = []
    banner_link = []
    price = []
    location = []
    info = []
    main_df = pd.DataFrame()
    oneHotCar_df = pd.DataFrame()

    page_link = request_module(initLink[i])
    print("{}.1 phase başarılı".format(i+1))
    banner_link = inner_request_module(page_link)
    print("{}.2 phase başarılı".format(i+1))
    price, location, info = getData_module(banner_link)
    print("{}.3 phase başarılı".format(i+1))
    main_df = dataFrame_module(price, location, info)
    print("{}.4 phase başarılı".format(i+1))
    oneHotCar_df = oneHot_module(main_df)
    print("{}.5 phase başarılı".format(i+1))
    oneHotCar_df.to_csv(r'C:\Users\Ahmet.basol\Desktop\Projects\Idea\car_scrap\car_sheet{}.csv'.format(i+1), encoding="utf-8", index=None, header=True)

csvMerge_module(path)

# %%
