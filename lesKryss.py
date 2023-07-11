# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 09:33:07 2023

@author: andryg
"""

import nvdbapiv3
import pandas as pd
import numpy as np

def getData():
    """
    Henter ut data fra nvdb, skriver det i en javascript fil som lager et 2d array med id og geometri til hvert uthentet
    objekt. 
    """
    vegkryss = nvdbapiv3.nvdbFagdata(37) #37 = vegkryss
    #Filtrerer dataen basert på prosjektreferanse, ikke plankryss og manglende verdier for kanalisering.
    vegkryss.filter({'egenskap': '11479="Sommeroppdatering 2023" AND 1114=3136 AND 12681!="VD5"'})
    vegkryssDF = pd.DataFrame(vegkryss.to_records())
    #print(vegkryssDF.columns.values.tolist())
    
    test = [i for i in vegkryssDF['geometri'].apply(lambda x: x.strip("POINTZ()")[3:].split(" "))]
    test = np.hstack((test,np.reshape(vegkryssDF['nvdbId'].to_numpy(), (-1,1))))
    print(test.shape)
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
    for i,j in enumerate(test):
        j = np.delete(j, 2)
        fil.write(str(list(map(float, j)))+",")
    fil.write("];")
getData()