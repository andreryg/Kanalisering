# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 08:42:18 2023

@author: andryg
"""

import json
from pathlib import Path
import nvdbapiv3
import pandas as pd
import datetime

downloads_path = str(Path.home() / "Downloads")
values = open(str(downloads_path + "/armer.txt"), "r")
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

vegkryss = nvdbapiv3.nvdbFagdata(37)
vegkryss.filter({'egenskap': '11479="Sommeroppdatering 2023" AND 1114=3136 AND 12681!="VD5"'})
vegkryssDF = pd.DataFrame(vegkryss.to_records())
#print(vegkryssDF.columns.values.tolist())

def createDict(i):
    """
    Lager dictionary på riktig format i henhold til nvdb skriv api. 
    """
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
            "typeId": 1789,
            "verdi": [
                int(data_list[i][1])
                ],
            "operasjon": "oppdater"
            },
            {
            "typeId": 12681,
            "verdi": [
                "VD5"
                ],
            "operasjon": "oppdater"
            },
            {
            "typeId": 12680,
            "verdi": [
                datetime.datetime.today().strftime('%Y-%m-%d')
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
fil = open("armer.json", "w")
fil.write(json.dumps(json_dict, indent=4))
fil.close()
