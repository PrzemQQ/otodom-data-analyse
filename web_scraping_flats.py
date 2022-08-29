from cmath import nan
import pandas as pd
import numpy as np
import seaborn as sns 
from bs4 import BeautifulSoup
import requests

j =1
names_text = []
localisations_text = []
price_and_area_data_text = []
price = []
area = []
rooms = []
while True:
    url = f"https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/wroclaw?market=ALL&ownerTypeSingleSelect=ALL&distanceRadius=0&locations=%5Bcities_6-39%5D&viewType=listing&lang=pl&searchingCriteria=wynajem&searchingCriteria=mieszkanie&searchingCriteria=cala-polska&page={j}"
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("h3", text="Nie znaleziono ogłoszeń"):
        break
    names = soup.find_all('h3', class_='css-1rhznz4 es62z2j13')
    names_text.append(list(name.text.replace("\"","") for name in names))
    localisations = soup.find_all('span', class_='css-17o293g es62z2j11')
    localisations_text.append(list(localisation.text.replace("\"","").split(",")[1] for localisation in localisations))
    
    price_and_area_data = soup.find_all('span', class_='css-s8wpzb eclomwz1')
    price_and_area_data_text.append(list(area.text for area in price_and_area_data))
    
    for infos in price_and_area_data:
        for info in infos:
            if "zł" in info or "€" in info:
                price.append(int(info.strip().replace("zł/mc","").replace("\xa0","").replace("€/mc","")))
            elif "m²" in info and "pokój" not in info:
                area.append(float(info.replace("m²", "").strip()))
            else:
                try:
                    rooms.append(int(float(info.split(" ")[0])))
                except ValueError:
                    rooms.append(nan)
                
    print(names_text)
    j+=1

names_flatten =[name for name in names_text for name in name]
localisation_flatten = [loc for loc in localisations_text for loc in loc]
df = pd.DataFrame(data={"name": names_flatten, "localisation": localisation_flatten, "price": price, "area": area, "rooms": rooms})
df.to_csv("otodom_flats_august.csv", index=False,sep=";")
df.to_excel("otodom_flats_august.xlsx", index=False)
