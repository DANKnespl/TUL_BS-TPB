"""
reader
"""
import json
from datetime import datetime,date

data=""
with open("D:/TUL/TPB/cv02/ScrapingFix280.json", 'r',encoding='utf8') as file:
    data = file.read()
jsonList = json.loads(data)
jsonDict = {}
months=["leden","únor","březen","duben","květen","červen","červenec","srpen","září","říjen","listopad","prosinec"]
dupes=0
maxComsID=0
minDateID=0
totalComms=0
maxFotos=0
lowestTimestampID=0
wordsInArts=0
lettersInArts=0
mmarticle=[0, 0]
articlesByMonths={}
artInYear={}
categories={}
wordsIn2021={}
wordsAll={}
cWord = [0, 0, 0]

for item in jsonList:
   name = item['header']
   jsonDict[name] = item
for i,jsonObj in enumerate(jsonList):
    #počet komentářů, min/max slova, nejvíce komentářů, nejvíce fotek 
    totalComms+=int(jsonObj["comments"])
    if len(jsonList[mmarticle[0]]["text"].split(" "))>len(jsonObj["text"].split(" ")):
        mmarticle[0]=i
    if len(jsonList[mmarticle[1]]["text"].split(" "))<len(jsonObj["text"].split(" ")):
        mmarticle[1]=i
    if (int(jsonObj["comments"])>int(jsonList[maxComsID]["comments"])):
        maxComsID=i
    if (int(jsonObj["images"])>maxFotos):
        maxFotos=int(jsonObj["images"])

    #slovník hlavního textu + počet slova
    tmpCword=jsonObj["text"].lower().count("covid")
    if tmpCword > jsonList[cWord[2]]["text"].lower().count("covid"):
        if tmpCword > jsonList[cWord[1]]["text"].lower().count("covid"):
            if tmpCword > jsonList[cWord[0]]["text"].lower().count("covid"):
                cWord[2]=cWord[1]
                cWord[1]=cWord[0]
                cWord[0]=i
            else:
                cWord[2]=cWord[1]
                cWord[1]=i
        else:
            cWord[2]=i
    for word in jsonObj["text"].lower().split():
        if word in wordsAll:
            wordsAll[word]+=1
        else:
            wordsAll[word]=1
    #kategorie + počet využití
    for tag in jsonObj["tags"]:
        if tag in categories:
            categories[tag]+=1
        else:
            categories[tag]=1
    #nejstarší, v letech, v měsících
    if jsonObj["date"]!="":
        if datetime.strptime(jsonList[lowestTimestampID]["date"],"%Y-%m-%d").timestamp() > datetime.strptime(jsonObj["date"],"%Y-%m-%d").timestamp():
            lowestTimestampID=i
        if jsonObj["date"].split("-")[0] in artInYear:
            artInYear[jsonObj["date"].split("-")[0]]+=1
        else:
            artInYear[jsonObj["date"].split("-")[0]]=1
        if jsonObj["date"].split("-")[1] in articlesByMonths:
            articlesByMonths[jsonObj["date"].split("-")[1]]+=1
        else:
            articlesByMonths[jsonObj["date"].split("-")[1]]=1
    #slova v nadpise 2021
    if "2021" in jsonObj["date"]:
        for word in jsonObj["header"].lower().split(" "):
            if word in wordsIn2021:
                wordsIn2021[word]+=1
            else:
                wordsIn2021[word]=1




print("Počet článků: "+str(len(jsonList)))
print("Počet duplicitních článků: "+ str(len(jsonList)-len(jsonDict)))
print("Nejstarší datum: " + jsonList[lowestTimestampID]["date"])
print("Nejvícce komentářů: "+ jsonList[maxComsID]["header"] + " - komentářů: "+ str(jsonList[maxComsID]["comments"]))
print("Nejvíce fotek: ", str(maxFotos),"\n")

print("Počet článků v letech:")
artInYear=dict(sorted(artInYear.items(), key=lambda x:x[1],reverse=True))
for key, value in artInYear.items():
    print("     ", key, ":", value)

print("\nUnikátní kategorie: " +str(len(categories)))
print("Kategorie (top 5): ")
n = 0
categories=dict(sorted(categories.items(), key=lambda x:x[1],reverse=True))
for key, value in categories.items():
    print("     ", key, ":", value)
    if n>=5:
        break
    n+=1

print("\nSlova roku 2021 (top 5): ")
wordsIn2021 = list(sorted(wordsIn2021.items(), key=lambda x:x[1],reverse=True))
for i in range(5):
    print("     ", wordsIn2021[i][0],":", wordsIn2021[i][1])

print("\nNapsaných komentářů:", str(totalComms))

n = 0
wordsAll=dict(sorted(wordsAll.items(), key=lambda x:x[1],reverse=True))
bonus01=""
for key, value in wordsAll.items():
    if n<8 and len(key)>5:
        bonus01+="      "+ str(key) + " : " + str(value) + "\n"
        n+=1
    wordsInArts+=value
    lettersInArts+=value*len(key)

print("Slov ve článcích: ", str(wordsInArts), "\n")
print("-------------------BONUS---------------")
print("Nejčastější slova (top 8): ")

print(bonus01)
print("Články s Covidem:")
for i in range(3):
    print("     ", jsonList[cWord[i]]["header"], ":", jsonList[cWord[i]]["text"].lower().count("covid"))    

print("\nNejkratší článek: ", jsonList[mmarticle[0]]["header"],"\nNejdelší článek: ",jsonList[mmarticle[1]]["header"], "\n")
print("Průměrně znaků ve slově: "+str(lettersInArts/float(wordsInArts)))

articlesByMonths=sorted(articlesByMonths.items(), key=lambda x:x[1],reverse=True)
print("Nejaktivnější měsíc: ", months[int(articlesByMonths[0][0])-1],"\nNejméně aktivní měsíc: ",months[int(articlesByMonths[len(articlesByMonths)-1][0])-1], "\n")
