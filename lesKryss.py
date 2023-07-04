# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 09:33:07 2023

@author: andryg
"""

import nvdbapiv3
import pandas as pd
import numpy as np
import json

def getData():
    vegkryss = nvdbapiv3.nvdbFagdata(37)
    vegkryss.filter({'egenskap': '11479="Sommeroppdatering 2023" AND 2080!=3478 AND 2080!=3222 AND 2080!=3226 AND 2080!=3784 AND 1788!=3475 AND 1788!=3219 AND 1788!=3223'})
    vegkryssDF = pd.DataFrame(vegkryss.to_records())
    #print(vegkryssDF.columns.values.tolist())

    test = [i for i in vegkryssDF['geometri'].apply(lambda x: x.strip("POINTZ()")[3:].split(" "))]
    
    """
    koordinater = []
    for j in test:
        j.pop()
        koordinater.append((list(map(float, j))))
    a = {}
    a.update({"koordinater":koordinater})
    with open("koordinater.json", 'w') as fp:
        json.dump(a, fp, sort_keys=True, indent=4)
    
    
    """
    fil = open("koordinater.js", "w")
    fil.write("const koordinater = [")
    for j in test:
        j.pop()
        fil.write(str(list(map(float, j)))+",")
    fil.write("];")

getData()
