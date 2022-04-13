import requests

headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64)"}
params = {
    "channel_id": "3189398996",
    "min_behot_time": "1649822510",
    "refresh_count": "3",
    "category": "pc_profile_channel",
    "aid": "24",
    "app_name": "toutiao_web",
    "_signature": "_02B4Z6wo00101lpfs4gAAIDDycxytizPE35ae7cAAPTQfdPdBniixGRckbmmoCyxFb.vpLjZK1OlKmIWDx87Kf.MWg4wUeXaPq.eULBrlBPj8d39ecjDuxkHRc8gSlXtTfnmUMSiNiubOx9rc1"
}
url = "https://www.toutiao.com/api/pc/list/feed"
res = requests.get(url=url, headers=headers,params=params)
items = res.json()["data"]

f = open("result.txt","w+")
for item in items:
    title = item["title"]
    link = item["article_url"]
    abstract = item["Abstract"]
    media = item["media_name"]
    f.write(f"{title}\t{link}\t{media}\t{abstract}\n")
    print(title)
f.close()



