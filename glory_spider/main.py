import requests
from bs4 import BeautifulSoup
import openpyxl
import re

herolist = []
hero_dictionary = {}
equip_list = []
result_list = []
root_url = "https://pvp.qq.com/web201605/"
herolist_url = root_url + "herolist.shtml"
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)'}


def get_herolist():
    url = "https://pvp.qq.com/web201605/js/herolist.json"
    results = requests.get(url=url, headers=headers).json()
    for result in results:
        name = result["cname"] # 英雄名称
        link = "https://pvp.qq.com/web201605/herodetail/{}.shtml".format(result["ename"])
        herolist.append((name,link))
        hero_dictionary["{}.shtml".format(result["ename"])] = name


def get_heroinfo():
    professions = {'herodetail-sort-1': '战士',
                   'herodetail-sort-2': '法师',
                   'herodetail-sort-3': '坦克',
                   'herodetail-sort-4': '刺客',
                   'herodetail-sort-5': '射手',
                   'herodetail-sort-6': '辅助'
                   }
    for item in herolist:
        name,hero_url = item
        res = requests.get(url=hero_url, headers=headers)
        soup = BeautifulSoup(res.content.decode("gbk"), "html.parser")
        title = soup.find("h3").text  # 英雄称号
        profession = professions[soup.find(class_="herodetail-sort").find("i")["class"][0]]  # 英雄职业
        targets = soup.find(class_="cover-list").find_all("li")
        values = [re.search(r":([0-9]+%)", target.find("i")['style']).group()[1:-1] for target in targets]  # 英雄能力值
        relations = []
        # 获取英雄关系
        targets = soup.find_all(class_="hero-list hero-relate-list fl")
        for target in targets:
            temp = target.find_all("a")
            hero_one = hero_dictionary[temp[0]["href"]]
            hero_two = hero_dictionary[temp[1]["href"]]
            relations.append(hero_one+"/"+hero_two)

        print(title, name, values, hero_url)
        result_list.append((title, name, profession, values, relations, hero_url))


def get_equiplist():
    type_list = ["攻击", "法术", "防御", "移动", "打野", "", "游走"]
    url = "https://pvp.qq.com/web201605/js/item.json"
    items = requests.get(url=url, headers=headers).json()
    for item in items:
        name = item["item_name"]
        item_type = item["item_type"]
        price = item["price"]
        total_price = item["total_price"]
        attribute = item["des1"].strip("<p>").strip("</p>").replace("<br>", "")
        try:
            ability = item["des2"].strip("<p>").strip("</p>").replace("<br>", "")
        except KeyError:
            ability = ""
        equip_list.append([name, type_list[item_type-1], price, total_price, attribute, ability])


def save_excel():
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "英雄大全"
    head = ["英雄称号", "英雄名称", "英雄职业", "生存能力", "攻击伤害", "技能效果", "上手难度", "最佳搭档", "压制英雄", "被压制英雄", "链接"]
    sheet.append(head)
    for item in result_list:
        row = list()
        row.append(item[0])
        row.append(item[1])
        row.append(item[2])
        for value in item[3]:
            row.append(value)
        for group in item[4]:
            row.append(group)
        row.append(item[5])
        sheet.append(row)

    sheet = wb.create_sheet("装备大全", 1)
    head = ["装备名称", "装备类型", "售价", "总价", "属性", "技能"]
    sheet.append(head)
    for item in equip_list:
        sheet.append(item)

    wb.save('result.xlsx')
    wb.close()


if __name__ == '__main__':
    get_herolist()
    get_heroinfo()
    get_equiplist()
    save_excel()
