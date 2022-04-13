import requests
import time
from bs4 import BeautifulSoup

headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64)"}
result = []
for i in range(10):
    url = f"https://movie.douban.com/top250?start={i*25}"
    res = requests.get(url=url, headers=headers)
    if res.status_code != 200:
        print("访问异常")
        break
    soup = BeautifulSoup(res.text, "html.parser")
    targets = soup.find("ol",class_="grid_view").find_all("div", class_="info")
    for target in targets:
        head = target.find("div", class_="hd")
        title = head.find("span", class_="title").text # 标题
        link = head.find("a")["href"] # 链接
        body = target.find("div", class_="bd")
        temp = body.find("p").text.strip().split("\n") # 切割
        person = "".join(temp[0].strip().split("\xa0")).strip() # 人员信息
        form = "".join(temp[1].strip().split("\xa0")).strip()   # 电影分类
        try:
            quote = body.find_all("p")[1].text.strip()
        except:
            quote = "无评语"
        points = body.find("div", class_="star").text.strip().split()[0]
        result.append((title, form, person, points, quote, link))
    print(url)
    time.sleep(1)

f = open("./result.txt", "w+")
for items in result:
    print(items)
    for item in items:
        f.write(item+"\t\t")
    f.write("\n")
f.close()
