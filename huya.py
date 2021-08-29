import os
import requests
from bs4 import BeautifulSoup


class Huya:
    def get_pictures(self):
        i = 1

        url = "https://www.huya.com/g/2168"

        response = requests.get(url=url).content

        soup = BeautifulSoup(response, "html.parser")

        imgs = soup.find_all(name='img', class_="pic")

        if not os.path.exists("虎牙妹子"):
            os.makedirs("虎牙妹子")

        for img in imgs:
            img_url = img['data-original']
            img_urlrec = img_url.split("?")[0]
            img_namerec = img['alt'].split('的')[0]
            print("正在下载" + img_namerec)
            img_rec = requests.get(img_urlrec).content
            with open("虎牙妹子/%s.%s.jpg" % (str(i), img_namerec), 'wb') as f:
                f.write(img_rec)
                i = i + 1
