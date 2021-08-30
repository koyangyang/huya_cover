import requests
import re
from bs4 import BeautifulSoup


url = 'https://www.huya.com/g'

res = requests.get(url).text

responce = BeautifulSoup(res,"html.parser")

lis = responce.find_all(name='li',class_="g-gameCard-item")


for li in lis:
    reg1='title="[^\x00-\xff]+"'
    reg2='g/[a-zA-Z0-9]+'
    try:
        name = re.search(reg1,str(li)).group().split("=")[1].strip('"')
        id = re.search(reg2,str(li)).group().split("/")[1]
        print(name+":"+id)
    except BaseException:
        pass