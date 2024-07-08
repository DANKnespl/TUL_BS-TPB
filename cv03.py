"""
reader
"""
import json
import matplotlib.pyplot as plt
from dateutil.parser import parse
from datetime import datetime

data=""
with open("D:/TUL/TPB/cv02/ScrapingFix1020.json", 'r',encoding='utf8') as file:
    data = file.read()
jsonList = json.loads(data)

rounding=2
histEnum={}
histAvg={}
histLengths={}
lengthXcomments=[]
artInDays={}
artInWeek={}
artInYear={}
cumArtInYear={}
categories={}
categoriesPostFilter={}
categoriesCount=0
cwords={}
vwords={}

for i,jsonObj in enumerate(jsonList):
    try:
        lengthXcomments.append([len(jsonObj["text"]), int(jsonObj["comments"])])
    except Exception:
        print("PEPEK")
    try:
        jsonObj["date"]=datetime.strptime(jsonObj["date"], "%Y-%m-%d")
    except Exception:
        jsonObj["date"]=None

    if len(jsonObj["text"].split(" ")) in histEnum:
        histEnum[len(jsonObj["text"].split(" "))]+=1
    else:
        histEnum[len(jsonObj["text"].split(" "))]=1
    for i,word in enumerate(jsonObj["text"].split(" ")):
        if len(word) in histLengths:
            histLengths[len(word)]+=1
        else:
            histLengths[len(word)]=1
    if round(len(jsonObj["text"])/len(jsonObj["text"].split(" ")),rounding) in histAvg:
        histAvg[round(len(jsonObj["text"])/len(jsonObj["text"].split(" ")),rounding)]+=1
    else:
        histAvg[round(len(jsonObj["text"])/len(jsonObj["text"].split(" ")),rounding)]=1
    if jsonObj["date"] is not None:
        if "koronavirus" in jsonObj["header"].lower():
            if jsonObj["date"] in cwords:
                cwords[jsonObj["date"]]+=1
            else:
                cwords[jsonObj["date"]]=1
        else:
            if jsonObj["date"] not in cwords:
                cwords[jsonObj["date"]]=0
        if "vakcína" in jsonObj["header"].lower():
            if jsonObj["date"] in vwords:
                vwords[jsonObj["date"]]+=1
            else:
                vwords[jsonObj["date"]]=1
        else:
            if jsonObj["date"] not in vwords:
                vwords[jsonObj["date"]]=0

        if jsonObj["date"] in artInDays:
            artInDays[jsonObj["date"]]+=1
        else:
            artInDays[jsonObj["date"]]=1
        if jsonObj["date"].year in artInYear:
            artInYear[jsonObj["date"].year]+=1
        else:
            artInYear[jsonObj["date"].year]=1
        if jsonObj["date"].weekday() in artInWeek:
            artInWeek[jsonObj["date"].weekday()]+=1
        else:
            artInWeek[jsonObj["date"].weekday()]=1
    for tag in jsonObj["tags"]:
        if tag in categories:
            categories[tag]+=1
        else:
            categories[tag]=1
    #categoriesCount+=len(jsonObj["tags"])

histEnum=dict(sorted(histEnum.items(), key=lambda x:x[1],reverse=True))
histAvg=dict(sorted(histAvg.items(), key=lambda x:x[1],reverse=True))
histLengths=dict(sorted(histLengths.items(), key=lambda x:x[1],reverse=True))

categories=dict(sorted(categories.items(),key=lambda x:x[1],reverse=True))


artInYear=dict(sorted(artInYear.items(), key=lambda x: parse(str(x[0]))))
artInDays=dict(sorted(artInDays.items(), key=lambda x: parse(str(x[0]))))

tmp=0
for key,value in artInDays.items():
    if isinstance(key,int):
        print("what")
    else:
        tmp=tmp+value
        cumArtInYear[key]=tmp
#categoryMin=list(categories.items())[0][1]/4 #value to show in list
for i, tag in enumerate(categories.items()):
    if i < 10:
        categoriesCount+=tag[1]
        categoriesPostFilter[tag[0]]=tag[1]
for i, tag in enumerate(categoriesPostFilter.items()):
    categoriesPostFilter[tag[0]]=tag[1]/categoriesCount


sizesCategories=[]
labelsCategories=[]
for x, y in categoriesPostFilter.items():
    labelsCategories.append(x)
    sizesCategories.append(y)



plot_cumulative_change=plt.figure(1)
ax1=plt.subplot()
plt.title("křivka zobrazující přidávání článků v čase")
ax1.set_ylabel("počet článků")
ax1.set_xlabel("rok")
plt.plot(*zip(*list(cumArtInYear.items())))



bar_yearly_change=plt.figure(2)
ax2=plt.subplot()
plt.title("Počet článků v letech")
ax2.set_ylabel("počet článků")
ax2.set_xlabel("rok")
plt.bar(*zip(*list(artInYear.items())))


scatter_length_comments=plt.figure(3)
ax3=plt.subplot()
plt.title("Závislost délky článku a počtem komentářů")
ax3.set_ylabel("počet komentářů")
ax3.set_xlabel("délka článku [znaky]")
plt.scatter(*zip(*lengthXcomments))



pie_categories=plt.figure(4)
ax4=plt.subplot()
plt.title("Top 10 kategorií")
plt.pie(sizesCategories, labels=labelsCategories, autopct='%1.1f%%', startangle=0)
ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.




bar_histogram_enum=plt.figure(5)
ax5=plt.subplot()
plt.title("Počet slov v článcích")
ax5.set_ylabel("počet slov")
ax5.set_xlabel("počet článků")
plt.bar(*zip(*list(histEnum.items())))

bar_histogram_average=plt.figure(6)
ax6=plt.subplot()
plt.title("Délka slov v článcích")
ax6.set_ylabel("počet článků")
ax6.set_xlabel("délka slov")
plt.bar(*zip(*list(histLengths.items())))

bar_histogram_average=plt.figure(9)
ax9=plt.subplot()
plt.title("Průměrná délka slova v článku")
ax9.set_ylabel("počet článků")
ax9.set_xlabel("délka slov")
plt.bar(*zip(*list(histAvg.items())),width=0.02)

plot_cvWords=plt.figure(7)
ax7=plt.subplot()
plt.title("Covid a vakcína")
plt.plot(*zip(*sorted(cwords.items(), key=lambda x: parse(str(x[0])))))
plt.plot(*zip(*sorted(vwords.items(), key=lambda x: parse(str(x[0])))))
plt.figlegend(["covid","vakcína"])

bar_weekly=plt.figure(8)
ax8=plt.subplot()
ax8.set_ylabel("počet článků")
ax8.set_xlabel("den v týdnu")
ax8.set_xticklabels(["","pondělí","úterý","středa","čtvrtek","pátek","sobota","neděle"])
plt.title("články ve dnech týdnu")
plt.bar(*zip(*sorted(artInWeek.items())))

plt.show()

"""
GET /idnes_report/1

GET /idnes_report/_count

GET /idnes_report/_search
{
  "querry":{
    "match":{
      "date":"2022"
    }
  }
}



"""
