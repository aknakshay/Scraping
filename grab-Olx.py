import urllib.request
import json
from bs4 import BeautifulSoup


def get_html(url):
    req = urllib.request.Request(url, headers={'User-Agent' : "Chrome Browser"}) 
    fp = urllib.request.urlopen(req, timeout=10)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    return mystr

def get_details(url):
    mystr = get_html(url)
    soup = BeautifulSoup(mystr, 'html.parser')
    head = str(soup.find("script"))
    start = head.find("language") - 2
    end = head.find(";\n</") 
    pr = head[start:end]
    price = int(json.loads(pr)["price"]) #price
    det = str(soup.findAll("table", attrs = {"class":"details fixed marginbott20 margintop5"}))
    del mystr
    ssoup = BeautifulSoup(det, 'html.parser')
    year = int(ssoup.findAll("td")[2].find("strong").text) #year
    distance = int(ssoup.findAll("td")[4].find("strong").text.replace("km","").replace(",","")) #kms
    tmp = "olx" + "," + url + "," + str(price) + "," + str(distance) + "," + str(year)
    #tmp["service"] = "olx"
    #tmp["url"] = url
    #tmp["price"] = price
    #tmp["distance"] = distance
    #tmp["year"] = year
    return(tmp)

li = []
ext_url = "https://www.olx.in/bangalore/scooters-honda/?search%5Bfilter_enum_model%5D%5B0%5D=activa&page=1"
data = get_html(ext_url)
soup = BeautifulSoup(data, 'html.parser')
pg = soup.findAll("span",attrs = {"class":"item fleft"})[len(soup.findAll("span",attrs = {"class":"item fleft"}))-1].findAll("span")[0].text
    
for page in range(13,int(pg)+1):
    ext_url = "https://www.olx.in/bangalore/scooters-honda/?search%5Bfilter_enum_model%5D%5B0%5D=activa&page=" + str(page)
    data = get_html(ext_url)
    soup = BeautifulSoup(data, 'html.parser')
    l = len(soup.findAll("table")[1].findAll("table")) #contains all the data
    for i in range(0,l):
        start = str(soup.findAll("table")[1].findAll("table")[i].findAll("a")[1]).find("href=") + 6
        end = str(soup.findAll("table")[1].findAll("table")[i].findAll("a")[1]).find(">") - 1
        li.append(str(soup.findAll("table")[1].findAll("table")[i].findAll("a")[1])[start:end])
    with open("data.csv","a+") as f:
        for url in li:
            f.write(get_details(url) + "\n")
    print("Done with page " + str(page))

print("Done")
    
