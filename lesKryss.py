# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 09:33:07 2023

@author: andryg
"""

import nvdbapiv3
import pandas as pd
import numpy as np

def getData():
    vegkryss = nvdbapiv3.nvdbFagdata(37)
    vegkryss.filter({'egenskap': '11479="Sommeroppdatering 2023" AND 2080!=3478 AND 2080!=3222 AND 2080!=3226 AND 2080!=3784 AND 1788!=3475 AND 1788!=3219 AND 1788!=3223'})
    vegkryssDF = pd.DataFrame(vegkryss.to_records())
    #print(vegkryssDF.columns.values.tolist())

    test = [i for i in vegkryssDF['geometri'].apply(lambda x: x.strip("POINTZ()")[3:].split(" "))]
    
    fil = open("koordinater.txt", "w")
    for j in test:
        j.pop()
        fil.write(str(list(map(float, j)))+"\n")

getData()
