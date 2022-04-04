import requests
from bs4 import BeautifulSoup
import re
import wordcloud

url = "https://www.tiobe.com/tiobe-index/"
res = requests.get(url)
soup = BeautifulSoup(res.text,"html.parser")
table = soup.find("table", id="top20").find("tbody").find_all("tr")
current_rand = 1
result = []
words = dict()
for item in table:
    if current_rand < 10:
        target = item.text[1:]
    else:
        target = item.text[2:]
    previous_rand = re.search(r"[0-9]+", target).group()
    language = re.search(r"(\D)+", target).group()
    ratings = re.search(r"(\d+\.([0-9]*?)%\+)|(\d+\.([0-9]*?)%-)", target).group()[:-1]
    change = re.search(r"-(.*?)%|\+(.*?)%", target).group()
    result.append((str(current_rand), previous_rand, language, ratings, change))
    words[language] = float(ratings.strip("%"))
    current_rand = current_rand + 1

f = open("result.txt", "w+")
f.write("Mar 2022  	Mar 2021  	Programming Language	Ratings	    Change\n")
for item in result:
    line = "{:<10}\t{:<10}\t{:<20}\t{:<10}\t{:<10}".format(item[0], item[1], item[2], item[3], item[4])
    f.write(line + "\n")
f.close()

w = wordcloud.WordCloud(width=1000, height=700, background_color="white")
w.generate_from_frequencies(words)
w.to_file("result.png")

