import re

def toLine(source,dest):
    json_data=""
    with open(source, "r",encoding="utf-8") as f:
        json_data=f.read()

    json_data=json_data.replace("\n","")
    json_data=json_data.replace("}{","},{")
    json_data=json_data.strip()
    json_data=re.sub(r"\s*\}\s*","}",json_data)
    json_data=re.sub(r"\s*\{\s*","{",json_data)
    json_data=re.sub(r"\s+"," ",json_data)
    json_data=re.sub(r"\}\s*,\s*\{","}\n{",json_data)
    open(dest, 'w').close()
    with open(dest, 'a',encoding="utf-8") as outfile:
        outfile.write(json_data)

if __name__=="__main__":
    toLine("D:/Elastic/OG.json","D:/Elastic/OGL.json")
    toLine("D:/Elastic/Incomplete.json","D:/Elastic/IncompleteL.json")
