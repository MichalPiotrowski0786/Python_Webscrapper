import requests as req
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

#'https://www.otomoto.pl/osobowe'
#e1b25f6f7 ooa-1whalr8-Text eu5v0x0
#ooa-1nvnpye e1b25f6f5
#pierwszy element <li>
#^[^0-9]$

def zapisz_do_csv(df_):
    df_.to_csv('otomoto_statystyka.csv',index=False,sep=';',decimal=',')

def znajdz_element_singleloop(array,type,class_name,regex):
    for x in soup.find_all(type, {'class': class_name}):
        final_string = re.search(regex, x.text)
        if final_string is not None: array.append(final_string.string)

def znajdz_element_doubleloop(array,type,class_name,type_2,regex):
    for x in soup.find_all(type, {'class': class_name}):
        for y in x.find_all(type_2):
            final_string = re.search(regex, y.text)
            if final_string is not None: array.append(final_string.string)

def show_and_save(df_,x_label,y_label,kind_,zapisz):
    df_ = df_.rename(columns={'index':x_label,'ilosc':y_label})
    df_.plot(x=x_label, y=y_label, kind=kind_)

    if zapisz is True: zapisz_do_csv(df_)

    plt.tight_layout()    
    plt.show()

array = []
for i in range(2):
    html_doc = req.get(f'https://www.otomoto.pl/osobowe?page={i+1}')
    soup = BeautifulSoup(html_doc.content, 'html.parser')

    #znajdz_element_doubleloop(array,'div','ooa-1nvnpye e1b25f6f5','li','^[0-9 ]*$')
    znajdz_element_singleloop(array,'span','ooa-epvm6 e1b25f6f8',' PLN')

array.sort()
df = pd.DataFrame.from_dict(Counter(array),orient='index',columns={'ilosc'}).reset_index()

show_and_save(df,'cena','liczba','bar',False)
