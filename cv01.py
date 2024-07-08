"""
fml
"""

#div id=content
    #div id=space_a
        #h1
        #class opener
    #div id=space_b
        #div data-io-article-url
        #div id= art-text

from bs4 import BeautifulSoup
import requests
import json
from pathlib import Path


file_path = Path("D:\TUL\TPB\Scraping.json")
file_stats = file_path.stat()

# python check file size
file_size_bytes = file_stats.st_size
print(file_size_bytes)

pg=8790 #5225
arch= requests.get("https://www.idnes.cz/zpravy/archiv/"+str(pg)+"?datum=&idostrova=idnes",timeout=60)
while file_size_bytes < 1100000000:
    art=0
    archSoup = BeautifulSoup(arch.content, 'html.parser')
    prep = archSoup.select("p[class=perex]")
    prep2 = archSoup.select("a[class=art-link]")
    while art < len(prep):
        #print(art)
        if (not(prep[art].text.lstrip().startswith("Premium")) and not(prep2[art].get("href").endswith("/foto"))):
            try:
                page = requests.get(prep2[art].get("href"),timeout=60) # Getting page HTML through request
                soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup
                header = soup.select("h1") # Selecting all of the anchors with titles
                date = soup.select("span[class=time-date]")
                perex=soup.select("div[class=opener]")
                main=soup.select("div[id=art-text]")
                images=soup.select("div[class=art-full] img")
                comments=soup.select("ul[class=art-community] > li[class=community-discusion] > a[id=moot-linkin] > span")
                tags=soup.select("div[id=art-tags] > a")
                try:
                    h= header[0].text.strip() # Display the innerText of each anchor
                except:
                    h=""
                try:
                    d=date[0].text.strip()
                except:
                    d=""
                try:
                    p=perex[0].text.strip()
                except:
                    p=""
                try:
                    m=main[0].text.strip()
                except:
                    m=""
                try:
                    c= comments[0].text.strip()
                    c=int(c[1:len(c)-11])
                except:
                    c=0
                i=len(images)
                t=[]
                for tag in tags:
                    t.append(tag.text.strip())
                dictionary = {
                    "header": h,
                    "date": d,
                    "perex": p,
                    "text": m,
                    "comments": c,
                    "images": i,
                    "tags": t
                }
                json_object = json.dumps(dictionary, indent=4,ensure_ascii=False)
                try:
                    with open("Scraping.json", "a",encoding='utf8') as outfile:
                        outfile.write(json_object)
                except:
                    print("fuckedUpText")
            except:
                print("chybaTimeout-in")
        art+=1
    pg+=1
    try:
        arch=requests.get("https://www.idnes.cz/zpravy/archiv/"+str(pg)+"?datum=&idostrova=idnes",timeout=60)
    except:
        pg-=1
        print("chybaTimeout")
    file_stats = file_path.stat()
    file_size_bytes = file_stats.st_size
    print(str(pg-1)+" "+str(file_size_bytes))
