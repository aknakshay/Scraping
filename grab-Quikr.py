import urllib.request
import json
from bs4 import BeautifulSoup
import random

li = []
count = 0

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
    return soup

for page in range(1,6): 
    soup = get_details("https://www.quikr.com/bikes-scooters/used+Honda+Activa+bikes-scooters+bangalore+w264vbc?page=" + str(page))
    for i in range(1,37):
        try:
            # Distance
            distance = soup.findAll("div",attrs={'data-adindex':i})[0].find("ul").find("li").text.replace(",","").replace(" kms","")
            # Price
            price = int(str(soup.findAll("div",attrs={'data-adindex':i})[0].findAll("div",attrs={'class':'col-xs-12 price-txt'}))[64:].replace('</i>','').replace(',','').replace('</div>]',''))
            # Url
            start = str(soup.findAll("div",attrs={'data-adindex':i})[0].find('a')).find("//") + 2
            end = str(soup.findAll("div",attrs={'data-adindex':i})[0].find('a')).find('" rel')
            url = str(soup.findAll("div",attrs={'data-adindex':i})[0].find('a'))[start:end]
            # Year
            st_year = soup.findAll("div",attrs={'data-adindex':i})[0].findAll('a')[1].text.strip().find("– ") + 2 
            year = soup.findAll("div",attrs={'data-adindex':i})[0].findAll('a')[1].text.strip()[st_year:]
            tmp = "quikr" + "," + url + "," + str(price) + "," + str(distance) + "," + str(year)
            li.append(tmp)
            print(tmp)
            count = count + 1
            with open("data-quikr.csv","a+") as f:
                for url in li:
                    f.write(tmp + "\n")
        except:
            print("No " + str(i) + " element")
    print("Done with page " + str(page))
    print("Total elements added yet : " + str(count))


        
