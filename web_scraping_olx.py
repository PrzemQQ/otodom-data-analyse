import pandas as pd
import numpy as np
import seaborn as sns 
from bs4 import BeautifulSoup
import requests

j =1
names_text = []
localisations_text = []
prices_text = []
prices = []
area = []
rooms = []

while True:
    url = f"https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/wroclaw/?page={j}"
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("h3", text="Nie znaleziono ogłoszeń"):
        break
    elif j ==20:
        break
    names = soup.find_all("h6",class_="css-v3vynn-Text eu5v0x0")
    names_text.append(list(name.text for name in names))
    
    localisations = soup.find_all("p",class_="css-p6wsjo-Text eu5v0x0")
    localisations_text.append(list(localisation.text for localisation in localisations))
    
    prices = soup.find_all("p",class_="css-wpfvmn-Text eu5v0x0")
    prices_text.append(list(price.text for price in prices))
    
    area = soup.find_all("p",class_="css-1bhbxl1-Text eu5v0x0")
    print(names_text)
    j+=1


