import requests as req
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

def zapisz_do_csv(df_,name):
    df_.to_csv(f'{name}.csv',index=False,sep=';',decimal=',')

def znajdz_element_singleloop(html,array,type,class_name,regex):
    for x in html.find_all(type, {'class': class_name}):
        final_string = re.search(regex, x.text)
        if final_string is not None: array.append(final_string.string)

def znajdz_element_doubleloop(html,array,type,class_name,type_2,regex):
    for x in html.find_all(type, {'class': class_name}):
        for y in x.find_all(type_2):
            final_string = re.search(regex, y.text)
            if final_string is not None: array.append(final_string.string)

def compute(url,num):
    for i in range(num):
        html_doc = req.get(url+f'{i}')
        soup = BeautifulSoup(html_doc.content, 'html.parser')

        znajdz_element_doubleloop(soup,array,'div','ooa-1nvnpye e1b25f6f5','li','^[0-9 ]*$')
        #znajdz_element_singleloop(soup,array,'span','ooa-epvm6 e1b25f6f8',' PLN')

def show_and_save(df_,x_label,y_label,kind_,fname_):
    df_ = df_.rename(columns={'index':x_label,'ilosc':y_label})
    df_.plot(x=x_label, y=y_label, kind=kind_)

    if fname_ != '': zapisz_do_csv(df_,fname_)

    plt.tight_layout()    
    plt.show()

array = []
compute('https://www.otomoto.pl/osobowe?page=',5)

array.sort()
df = pd.DataFrame.from_dict(Counter(array),orient='index',columns={'ilosc'}).reset_index()

show_and_save(df,'rok','liczba','bar','')
