"""
fml
"""
import json
from datetime import datetime,date
import locale
# for German locale
locale.setlocale(locale.LC_TIME, "cs_CZ") 
search_text = "}{"
replace_text = "},{"
data=""
with open("D:/TUL/TPB/ScrapingFix1000.json", 'r',encoding='utf8') as file:
    data = file.read()
#data = data.replace(search_text, replace_text)
jsonList = json.loads(data)
#jsonList[0]["date"]
print("loaded")

for i, jsonObj in enumerate(jsonList):
    jsonObj["date"]=jsonObj["date"].replace("ledna","leden")
    jsonObj["date"]=jsonObj["date"].replace("února","únor")
    jsonObj["date"]=jsonObj["date"].replace("března","březen")
    jsonObj["date"]=jsonObj["date"].replace("dubna","duben")
    jsonObj["date"]=jsonObj["date"].replace("května","květen")
    jsonObj["date"]=jsonObj["date"].replace("června","červen")
    jsonObj["date"]=jsonObj["date"].replace("července","červenec")
    jsonObj["date"]=jsonObj["date"].replace("srpna","srpen")
    jsonObj["date"]=jsonObj["date"].replace("října","říjen")
    jsonObj["date"]=jsonObj["date"].replace("listopadu","listopad")
    jsonObj["date"]=jsonObj["date"].replace("prosince","prosinec")
    try:
        jsonObj["date"]= str(date.fromtimestamp(datetime.strptime(jsonObj["date"],"%d. %B %Y").timestamp()))
    except:
        jsonObj["date"]= ""
print("swapped")
with open("D:/TUL/TPB/ScrapingFix1020.json", 'w',encoding='utf8') as file:
    file.write(json.dumps(jsonList, indent=4,ensure_ascii=False))
print("saved")
