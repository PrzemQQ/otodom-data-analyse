import pandas as pd
import numpy as np
import seaborn as sns 
from bs4 import BeautifulSoup
import requests
import re

j =1
names_text = []
localisations_text = []
prices_text = []
prices = []
area = []
areas = []
rooms = []

while True:
    url = f"https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/wroclaw/?page={j}"
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("h3", text="Nie znaleziono ogłoszeń"):
        break
    elif j ==3:
        break
    names = soup.find_all("h6",class_="css-v3vynn-Text eu5v0x0")
    names_text_temp = []
    names_text_temp.append(list(name.text for name in names))
    names_text.append(list(item for sublist in names_text_temp for item in sublist))
    
    localisations = soup.find_all("p",class_="css-p6wsjo-Text eu5v0x0")
    localisations_text_temp = list(localisation.text.split(",")[1].split("-") for localisation in localisations)
    localisations_text_temp = [localisations_text_temp[i] for i in range(len(localisations_text_temp)) if i % 2 == 0]

    localisations_text.append(list(sublist[0].strip() for sublist in localisations_text_temp ))
    
    
    prices = soup.find_all("p",class_="css-wpfvmn-Text eu5v0x0")
    prices_text_temp = list(re.findall('[0-9]+', str(price.text)) for price in prices)
    prices_text.append(list("".join(substring) for sublist in prices_text_temp for substring in sublist ))
    
    area = soup.find_all("p",class_="css-1bhbxl1-Text eu5v0x0")
    areas_temp = [area.text for area in area]
    areas.append(list(area.replace("m²", "").replace(",",".").strip()) for area in areas_temp)
    print(areas)
    # print(len(names_text[0]),len(localisations_text[0]),len(prices_text),len(areas[0]))
    j+=1
   
    
    break

def flatten_data(tab):
    return list(item for sublist in tab for item in sublist)
# data = pd.DataFrame({"Name": flatten_data(names_text), "Localisation": flatten_data(localisations_text), "Price": flatten_data(prices_text), "Area": flatten_data(areas)})
# data.to_csv("data_olx.csv", index=False,sep=";")
