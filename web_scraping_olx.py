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
#scraping data from olx.pl
while True:
    url = f"https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/wroclaw/?page={j}"
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("h3", text="Nie znaleziono ogłoszeń"):
        break
    elif j ==25:
        break
    names = soup.find_all("h6",class_="css-v3vynn-Text eu5v0x0") #name of the offer
    names_text_temp = []
    names_text_temp.append(list(name.text for name in names))
    names_text.append(list(item for sublist in names_text_temp for item in sublist))
    
    localisations = soup.find_all("p",class_="css-p6wsjo-Text eu5v0x0") #localisation of the offer
    loc = [list(loc.text.split("-")[0].replace("Wrocław, ","").rstrip() for loc in localisations)] #remove "Wrocław, " from localisation an striping white spaces

    for l in loc[0]:
        localisations_text.append(l) #append localisation to list
    
    
    prices = soup.find_all("p",class_="css-wpfvmn-Text eu5v0x0") #price of the offer
    prices_text_temp = list(re.findall('[0-9]+', str(price.text)) for price in prices)
    prices_text.append(list("".join(sublist) for sublist in prices_text_temp  )) #join list of strings into one string to create a value of price
    
    area = soup.find_all("p",class_="css-1bhbxl1-Text eu5v0x0") #area of the offer
    areas.append([(area.text.replace("m²", "").replace(",",".").strip()) for area in area])
    
    print(len(names_text[0]),len(localisations_text),len(prices_text[0]),len(areas))
    j+=1
    print(localisations_text)
   
    
def flatten_data(tab):
    """_summary_: flatten list of lists into one list

    Args:
        tab (list): list of lists

    Returns:
        list: flatten list
    """
    return list(item for sublist in tab for item in sublist)
print(len(flatten_data(names_text)),len((localisations_text)),len(flatten_data(prices_text)),len(flatten_data(areas)))

data = pd.DataFrame({"Name": flatten_data(names_text), "Localisation": localisations_text, "Price": flatten_data(prices_text), "Area": flatten_data(areas)}) #create dataframe
data.to_csv("data_olx_scrap.csv", index=False,sep=";") #save data to csv file
