from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests


client = MongoClient('localhost', 27017)
db = client.dbhomework_week1_test

driver = webdriver.Chrome('./chromedriver')

url = "https://m.map.naver.com/search2/search.naver?query=%EC%95%A0%EA%B2%AC%20%EC%9C%A0%EC%B9%98%EC%9B%90&sm=shistory&style=v5"

driver.get(url)
time.sleep(5)

for i in range(10):
    try:
        btn_more = driver.find_element_by_css_selector("#foodstar-front-location-curation-more-self > div > button")
        btn_more.click()
        time.sleep(5)
    except NoSuchElementException:
        break

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')

places = soup.select("#ct > div.search_listview._content._ctList > ul > li")
#ct > div.search_listview._content._ctList > ul > li

# print(places)

for place in places:
    try:
        title = place.select_one("#ct > div.search_listview._content._ctList > ul > li > div.item_info > a.a_item.a_item_distance._linkSiteview > div > strong").text
        address = place.select_one("#ct > div.search_listview._content._ctList > ul > li > div.item_info > div.item_info_inn > div > a").contents[1]
        # image = place.select_one("#ct > div.search_listview._content._ctList > ul > li > div.item_info > a.item_thumb._itemThumb > img")
        category = place.select_one("#ct > div.search_listview._content._ctList > ul > li > div.item_info > a.a_item.a_item_distance._linkSiteview > div > em").text
        # show, episode = place.select_one("div.box_module_cont > div > div > div.mil_inner_tv > span.il_text").text.rsplit(" ", 1)
        phone = place.select_one("#ct > div.search_listview._content._ctList > ul > li > div.item_btn > a.btn_phone2.sp_map")["href"]
    except TypeError:
        pass
    # print(title, address, category,phone)

    headers = {
        "X-NCP-APIGW-API-KEY-ID": "va9dugepnd",
        "X-NCP-APIGW-API-KEY": "19elOrPT3s9FZzfmjFf8raXwxU0sX2lhya2f5Kam"
    }
    r = requests.get(f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}", headers=headers)
    response = r.json()
    if response["status"] == "OK":
        if len(response["addresses"]) > 0:
            x = float(response["addresses"][0]["x"])
            y = float(response["addresses"][0]["y"])
            print(title, address, category,phone, x, y)
            doc = {
                "title": title,
                "address": address,
                "category": category,
                "phone": phone,
                # "image": image,
                # "show": show,
                # "episode": episode,
                "mapx": x,
                "mapy": y}
            db.matjips.insert_one(doc)


        else:
            print(title, "좌표를 찾지 못했습니다")