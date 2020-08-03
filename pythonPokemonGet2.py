# !/usr/bin/python
# coding:utf-8

import requests
from bs4 import BeautifulSoup
import io
import time
import json

def sleeptime(hour, min, sec):
    return hour*3600 + min*60 + sec

for number in range(1, 808):
    # -----------------------------
    if number < 10:
        link = "https://hk.portal-pokemon.com/play/pokedex/00" + str(number)
    elif number < 100:
        link = "https://hk.portal-pokemon.com/play/pokedex/0" + str(number)
    else:
        link = "https://hk.portal-pokemon.com/play/pokedex/" + str(number)

    # 將此頁面的HTML GET下來
    r = requests.get(link)  
    soup = BeautifulSoup(r.text, "html.parser")

    # ----------------------------Geting data ----------------------------
    # ID/名字
    poke_id = soup.find("p", class_="pokemon-slider__main-no size-28")
    poke_name = soup.find("p", class_="pokemon-slider__main-name size-35")

    # 身高/體重
    poke_height = soup.select("div.pokemon-info__height span")
    poke_wieght = soup.select("div.pokemon-info__weight span")

    # 分類
    poke_category = soup.select("div.pokemon-info__category span")

    # 特性
    poke_abilities = soup.select("div.pokemon-info__abilities span")
    poke_ability = poke_abilities[1].text.strip()

    # 描述
    poke_des = soup.find("p", class_="pokemon-story__body size-14")
    poke_description = poke_des.text.strip()

    # 属性
    poke_type = soup.select("div.pokemon-type span")

    poke_gender = soup.select("div.pokemon-info__gender img")

    # 進化/退化
    poke_evolution_img = soup.select("div.pokemon-evolution-contents img")
    poke_evolution = soup.select("div.pokemon-evolution-contents p")

    # ----------------------------------processing------------------------------------
    male = False
    female = False
    gender = ""
    # Checking male/female image
    for x in poke_gender:
        if "/play/resources/pokedex/img/icon_male.png" == x["src"]:
            male = True
        elif "/play/resources/pokedex/img/icon_female.png" == x["src"]:
            female = True

    if male & female:
        gender = "男/女"
    elif male:
        gender = "男"
    elif female:
        gender = "女"
    else:
        gender = "無性別"

    # --------------------------------------evolution-------------------------------
    # Checking 
    arrow_number = 0
    for x in poke_evolution_img:
        if "/play/resources/pokedex/img/arrow_down.png" == x["src"]:
            arrow_number += 1

    j = 0
    poke_evolution_list = []
    for x in poke_evolution:
        if (j % 3 == 0):
            poke_evolution_list.append(x.text)
        j += 1

    evolution = []
    degradation = ""

    # evolution number: 0
    if arrow_number == 0:
        evolution.append("無進化")
        degradation = "無退化"

    # evolution number: 1
    elif arrow_number == 1:
        if poke_evolution_list.index(poke_id.text) == 0:
            count = len(poke_evolution_list) 
            # print(count)
            for i in range(1, count):
                evolution.append(poke_evolution_list[i])
                
            degradation = "無退化"
        else:
            evolution.append("無進化")
            degradation = poke_evolution_list[0]

    # evolution number: 2
    elif arrow_number == 2:
        if poke_evolution_list.index(poke_id.text) == 0:
            evolution.append(poke_evolution_list[1])
            degradation = "無退化"
        elif poke_evolution_list.index(poke_id.text) == 1:
            count = len(poke_evolution_list) 
            for i in range(2, count):
                if poke_evolution_list[i] in evolution:
                    continue
                evolution.append(poke_evolution_list[i])
            degradation = poke_evolution_list[0]
        else:
            evolution.append("無進化")
            degradation = poke_evolution_list[1]


    # ----------------------------------print-------------------------------
    attribute = ""
    i = 0
    for s in poke_type:
        if i == 0:
            attribute += s.text
            i += 1
        else:
            attribute += ", " + s.text
    # print("------------------")
    # print("編號：" + poke_id.text)
    # print("名字" + poke_name.text)
    # print("身高：" + poke_height[1].text)
    # print("體重：" + poke_wieght[1].text)
    # print("分類：" + poke_category[1].text)
    # print("能力：" + poke_ability)
    # print("描述：" + poke_description)
    # print("性別：" + gender)

    # print("身高：" + str(poke_height.text))

    # print("屬性：" + attribute)
    # print("進化 層數：" + str(arrow_number))
    # print("進化: " + str(evolution))
    # print("退化: " + degradation)

    # print("-------------------")
    #-----------------------------------data to dict-----------------------------
    poke_dict = {'id': poke_id.text,
                 'name': poke_name.text,
                 'height': poke_height[1].text,
                 'weight': poke_wieght[1].text,
                 'category': poke_category[1].text,
                 'ablities': poke_ability,
                 'description': poke_description,
                 'gender': gender,
                 'attribute': attribute,
                 'evolutions': evolution,
                 'degradation': degradation}

    #---------------------------------Genearate json-----------------------------
    def write_json(data, filename='poke_data.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    with open('poke_data.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

        temp = data['pokemon']

        temp.append(poke_dict)
    write_json(data)
    print(poke_name.text + "：成功")

    # Delay
    time.sleep(sleeptime(0, 0, 2))



