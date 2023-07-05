# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 08:42:18 2023

@author: andryg
"""

import json
from pathlib import Path
import nvdbapiv3
import pandas as pd
from datetime import date
import datetime

downloads_path = str(Path.home() / "Downloads")
values = open(str(downloads_path + "/kanalisering.txt"), "r")
data = values.read()
values.close()
temp_data_list = data.replace('\n', ' ').split("],[")
data_list = []
for i in temp_data_list:
    i = i.replace('[[', '')
    i = i.replace(']]', '')
    i = i.split(",")
    i = [eval(j) for j in i]

    data_list.append(i)
#print(data_list)

vegkryss = nvdbapiv3.nvdbFagdata(37)
vegkryss.filter({'egenskap': '11479="Sommeroppdatering 2023" AND 2080!=3478 AND 2080!=3222 AND 2080!=3226 AND 2080!=3784 AND 1788!=3475 AND 1788!=3219 AND 1788!=3223 AND 1114!=3137 AND 1114!=3138 AND 1114!=3139 AND 1114!=3140 AND 1114!=3141'})
vegkryssDF = pd.DataFrame(vegkryss.to_records())
print(vegkryssDF.columns.values.tolist())
#print(vegkryssDF[vegkryssDF.nvdbId.isin([data_list[0][0]])].loc[:,'relativPosisjon'])
#print(vegkryssDF.loc[vegkryssDF['nvdbId'] == data[0][0], 'relativPosisjon'])

#print(vegkryssDF[vegkryssDF.nvdbId.isin([data_list[0][0]])].loc[:,'startdato'].to_numpy())#str(date.today()))

def createDict(i):
    kanalisering = ["Ingen", "Malt", "Fysisk m kantstein", "Ulik kanalisering"]
    return {
        "gyldighetsperiode": {
            "startdato": vegkryssDF[vegkryssDF.nvdbId.isin([data_list[i][0]])].loc[:,'startdato'].to_numpy()[0]#str(date.today())
            },
        "validering": {
            "lestFraNvdb": str(datetime.datetime.now()).replace(" ", "T").split(".")[0]
            },
        "typeId": 37,
        "nvdbId": data_list[i][0],
        "versjon": int(vegkryssDF[vegkryssDF.nvdbId.isin([data_list[i][0]])].loc[:,'versjon']),
        "egenskaper": [
            {
            "typeId": 2080,
            "verdi": [
                kanalisering[int(data_list[i][1])]
                ],
            "operasjon": "oppdater"
            },
            {
            "typeId": 1788,
            "verdi": [
                kanalisering[int(data_list[i][2])]
                ],
            "operasjon": "oppdater"
            }
            ]
        }

jsons = []
for i, v in enumerate(data_list):
    jsons.append(createDict(i))
    
json_dict = {
    "delvisKorriger": {
        "vegobjekter": jsons
        },
    "datakatalogversjon": "2.33"
    }
#print(json_dict)
fil = open("kanalisering.json", "w")
fil.write(json.dumps(json_dict, indent=4))
fil.close()
